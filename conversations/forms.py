from django import forms

class AddCommentForm(forms.Form):

    message = forms.CharField(required=True, widget=forms.Textarea(attrs={"placeholder": "보낼 메세지를 적으세요"}))