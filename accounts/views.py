# from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import SignupForm

User = get_user_model()


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)  # 遷移先の指定

    def form_valid(self, form):  # form_valid関数のオーバーライド
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password1 = form.cleaned_data["password1"]  # passwordはキーに存在しないためpassword1にする
        user = authenticate(self.request, username=username, password=password1)
        login(self.request, user)
        return response


class UserProfileView(LoginRequiredMixin, TemplateView):
    # LoginRequiredMixinを継承するとログインしていないユーザーがprofile画面へ飛ぼうとするとログインページに遷移するようになる
    template_name = "accounts/user_profile.html"

    #  遷移先のテンプレートを指定するための変数。全てのTemplateViewクラスで設定可能
    # fields = ["username"]
    # フォームに表示するフィールドを指定する
    def get_context_data(self, **kwargs):
        # super().get_context_data(**kwargs)で親クラスの.get_context_dataを呼び出し、contextに格納
        context = super().get_context_data(**kwargs)
        # 親クラスの**kwargsで得られた辞書型のデータを一部書き換える
        context["username"] = self.kwargs["username"]
        return context
    model = User
    # レコード更新をかけるモデルを指定するための変数。
    #  ここで指定したモデルに関しては、モデル名をスネークケースに変換したものが自動的にcontextに追加される(例：Bookモデルであればcontext["book"]に格納される)。
    #  後述のform_classにてModelFormクラスを指定している場合であっても、この変数の設定は必須。
