import os
import requests
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, View, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins

class LoginView(mixins.VisitorsOnlyView, View):

    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'users/login.html', {'form':form})
    
    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email    = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user     = authenticate(request, username=email, password=password)
            if user is not None: 
                login(request, user)
                messages.success(request, f"{user.first_name}님 돌아오신 것을 환영합니다.")
                return redirect(reverse('core:home'))
        return render(request, 'users/login.html', {'form':form})

def log_out(request):
    messages.info(request, "다음에 또 봐요~")
    logout(request)
    return redirect(reverse('core:home'))

class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class    = forms.SignUpForm
    success_url   = reverse_lazy('core:home')

    def form_valid(self, form):
        form.save()
        email    = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user     = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

def github_login(request):
    client_id = os.environ.get('GitHub_ID')
    redirect_uri = 'http://127.0.0.1:8000/users/login/github/callback'
    return redirect(f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user')

class GithubException(Exception):
    pass

def github_callback(request):
    try:
        client_id     = os.environ.get('GitHub_ID')
        client_secret = os.environ.get('GitHub_SECRET')
        code          = request.GET.get('code', None)
        if code is not None:
            token_request = requests.post(
                f'https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}',
                headers={'Accept': 'application/json'},
            )
            token_json = token_request.json()
            error      = token_json.get('error', None)
            if error is not None:
                raise GithubException()
            else:
                access_token    = token_json.get('access_token')
                profile_request = requests.get(
                    'https://api.github.com/user',
                    headers={
                        'Authorization': f'token {access_token}',
                        'Accept': 'application/json',
                    },
                )
                profile_json = profile_request.json()
                username     = profile_json.get('login', None)
                if username is not None: 
                    name = profile_json.get('name')
                    if name is None: 
                        name  = username
                        email = profile_json.get('email')
                    if email is None: 
                        email = username
                        bio   = profile_json.get('bio')
                    if bio is None: 
                        bio = ""

                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email        = email,
                            first_name   = name,
                            username     = email,
                            bio          = bio,
                            login_method = models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse('core:home'))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except Exception:
        return redirect(reverse('users:login'))


def kakao_login(request):
    client_id    = os.environ.get('Kakao_ID')
    redirect_uri = 'http://127.0.0.1:8000/users/login/kakao/callback'
    return redirect(f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code')

class KakaoException(Exception):
    pass

def kakao_callback(request):
    try:
        code          = request.GET.get('code')
        client_id     = os.environ.get('Kakao_ID')
        redirect_uri  = 'http://127.0.0.1:8000/users/login/kakao/callback'
        token_request = requests.get(
            f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}'
        )
        token_json = token_request.json()
        error      = token_json.get('error', None)
        if error is not None:
            raise KakaoException("인증코드를 가져올 수 없습니다.")
        access_token    = token_json.get('access_token')
        profile_request = requests.get('https://kapi.kakao.com//v2/user/me', headers={'Authorization': f'Bearer {access_token}'},)
        profile_json    = profile_request.json()
        email           = profile_json.get('kakao_account', None).get('email')
        if email is None:
             raise KakaoException("당신의 이메일이 필요합니다.")
        properties    = profile_json.get('properties')
        nickname      = properties.get('nickname')
        profile_image = properties.get('profile_image')
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"{user.login_method}으로 이미 가입되어 있습니다. {user.login_method}로 로그인 해주세요!")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email        = email,
                username     = email,
                first_name   = nickname,
                avatar       = profile_image,
                login_method = models.User.LOGIN_KAKAO,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(f'{nickname}-avatar',ContentFile(photo_request.content))
        login(request, user)
        messages.success(request, f"{user.first_name}님 돌아오신 것을 환영합니다.")
        return redirect(reverse('core:home'))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse('users:login'))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"    # UserProfileView에서 특정 변수명을 지정해주기 위해서 만듬

class UpdateProfileView(mixins.MembersOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update_profile.html"
    fields = [
        "first_name",
        "last_name",
        "avatar",
        "bio",
        "birthdate",
        "language",
        "currency",
    ]
    success_message = "프로필 수정 완료"

    def get_object(self, queryset=None):
        # profile = self.request.user.id
        # profile = get_object_or_404(models.User, pk=profile)
        # print(self.request.user.id)
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "이름"}
        form.fields["last_name"].widget.attrs = {"placeholder": "성"}
        form.fields["bio"].widget.attrs = {"placeholder": "소개"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "생일 xxxx-xx-xx"}
        return form

class UpdatePasswordView(
    mixins.EmailLoginOnlyView,
    mixins.MembersOnlyView,
    SuccessMessageMixin,
    PasswordChangeView
):
    
    template_name = "users/update_password.html"
    success_message ="비밀번호 수정 완료"
    

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "현재비밀번호"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "변경할 비밀번호"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "변경할 비밀번호 확인"}
        return form
    
    def get_success_url(self):
        return self.request.user.get_absolute_url()
    
@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))
