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
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "ひらがなで入力してください",
            }
        ),
    )

    region = forms.ChoiceField(
        label="生活地区",
        choices=LIVING_AREA_CHOICES,
    )

    login_id = forms.CharField(
        label="社員番号",
        min_length=6,
        max_length=6,
        widget=forms.TextInput(
            attrs={
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "placeholder": "6桁",
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
                "placeholder": "例：19600910",
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
                "placeholder": "4桁",
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
                "placeholder": "4桁",
            }
        ),
    )
    agree_health = forms.BooleanField(
    label="健康チェック・緊急生存確認への協力に同意します",
    required=True,
    )

    agree_sns = forms.BooleanField(
    label="組合から提供される情報をSNS等へ掲載しないことに同意します",
    required=True,
    )

    def clean_login_id(self):
        login_id = self.cleaned_data["login_id"]

        if not login_id.isdigit():
            raise forms.ValidationError(
                "社員番号は6桁の数字で入力してください。"
            )

        if Account.objects.filter(login_id=login_id).exists():
            raise forms.ValidationError(
                "この社員番号は既に登録されています。"
            )

        return login_id

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and not password1.isdigit():
            self.add_error(
                "password1",
                "パスワードは4桁の数字で入力してください。"
            )

        if password1 != password2:
            raise forms.ValidationError(
                "パスワードが一致していません。"
            )

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