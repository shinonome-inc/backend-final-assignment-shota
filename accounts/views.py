# from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):  # form_valid関数のオーバーライド
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password1 = form.cleaned_data["password1"]  # passwordはキーに存在しないためpassword1にする
        user = authenticate(self.request, username=username, password=password1)
        login(self.request, user)
        return response
