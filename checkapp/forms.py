from django import forms
from .models import Account

LIVING_AREA_CHOICES = [
    ("北九州", "北九州"),
    ("福岡", "福岡"),
    ("大分", "大分"),
    ("熊本", "熊本"),
    ("長崎", "長崎"),
    ("佐世保", "佐世保"),
]


class AccountRegisterForm(forms.Form):

    name = forms.CharField(
        label="氏名",
        max_length=50,
    )

    region = forms.ChoiceField(
        label="生活地区",
        choices=LIVING_AREA_CHOICES,
    )

    login_id = forms.CharField(
        label="社員番号（ログインID）",
        min_length=6,
        max_length=6,
        widget=forms.TextInput(
            attrs={
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "placeholder": "例：012345"
            }
        ),
    )

    birth_date = forms.DateField(
        label="生年月日",
        input_formats=["%Y%m%d"],
        widget=forms.TextInput(
            attrs={
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "maxlength": "8",
                "placeholder": "例：19901213",
            }
        ),
    )

    password1 = forms.CharField(
        label="パスワード",
        min_length=4,
        max_length=4,
        widget=forms.PasswordInput(
            attrs={
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "placeholder": "4桁"
            }
        ),
    )

    password2 = forms.CharField(
        label="パスワード（確認）",
        min_length=4,
        max_length=4,
        widget=forms.PasswordInput(
            attrs={
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "placeholder": "4桁"
            }
        ),
    )
    def clean_login_id(self):

        login_id = self.cleaned_data["login_id"]

        if Account.objects.filter(login_id=login_id).exists():
            raise forms.ValidationError(
                "この社員番号は既に登録されています。"
            )

        return login_id

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("パスワードが一致しません。")

        return cleaned_data
    
    
class LoginForm(forms.Form):

    login_id = forms.CharField(
        label="社員番号",
        max_length=6,
    )

    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
    )