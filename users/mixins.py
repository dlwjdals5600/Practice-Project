from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class EmailLoginOnlyView(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.login_method == "email"
    
    def handle_no_permission(self):
        messages.error(self.request, "이동 할 수 없는 페이지 입니다.")
        return redirect("core:home")

class VisitorsOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page not found" # 로그인 했으면 VisitorsOnlyView로 이동

    def test_func(self):
        return not self.request.user.is_authenticated # true 값 반환 , 여기서 true값은 유저는 인증이 되지 않았다는 것을 의미 ,익명의 유저 의미
    
    def handle_no_permission(self):
        messages.error(self.request, "이동 할 수 없는 페이지 입니다.")
        return redirect("core:home")
    

class MembersOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
