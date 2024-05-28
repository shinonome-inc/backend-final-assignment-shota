from django.contrib.auth import views as auth_views
from django.urls import path

# 同じディレクトリ(今回はaccounts)からviews.pyをimportしている
from . import views  # .（ピリオド1つ）が同じディレクトリを表す

app_name = "accounts"

urlpatterns = [
    path(
        "signup/", views.SignupView.as_view(), name="signup"
    ),  # 第三引数のnameはパターンネームといい、signup.htmlでビューを呼び出すために記述される
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    # auth_views.UserLoginViewでviews.pyの UserLoginView を呼び出している
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("<str:username>/", views.UserProfileView.as_view(), name="user_profile"),
    # path(“アドレス/<値の種類: 値の引数>/”, view関数);
    # path('<str:username>/follow/', views.FollowView.as_view(), name='follow'),
    # path('<str:username>/unfollow/', views.UnFollowView, name='unfollow'),
    # path('<str:username>/following_list/', views.FollowingListView.as_view(), name='following_list'),
    # path('<str:username>/follower_list/', views.FollowerListView.as_view(), name='follower_list'),
]
