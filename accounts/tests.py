from django.conf import settings
from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):  # 200 OK；GETメソッドではリソースが読み込まれ、メッセージ本文で転送された事を示す。
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, 200
        )  # ステータスコードが200かどうかを確かめるために、assertEqualという関数を使う。
        # 第１引数==第２引数であればTrueとなる
        self.assertTemplateUsed(response, "accounts/signup.html")
        # responseで使われているhtmlが第２引数に入れたhtmlと一致しているかを確かめています。一致すればtrueとなりテスト成功となる

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, valid_data)
        # self.client.post(ページのURL, 保存したいデータ)
        # ユーザーがフォームにデータを打ち込んでユーザー登録ボタンを押した操作を表している
        # self.client.postのメソッドは、第１引数にurlを、第２引数にdict型でデータを入れることでpostができる。
        # 1の確認 = tweets/homeにリダイレクトすること
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,  # リクエストされたリソースの URI が 一時的に 変更されたことを示す
            target_status_code=200,  # target_codeはリダイレクト先の画面がきちんと表示されているかどうかを見るものとなる
        )
        # 引数	    意味
        # response	GET/POSTしたレスポンス
        # expected_url	最終的にリダイレクトされるURL
        # status_code	はじめに返ってくるHTTPのレスポンスコード
        # target_status_code	最終的に返ってくるHTTPのレスポンスコード
        # 2の確認 = ユーザーが作成されること
        self.assertTrue(User.objects.filter(username=valid_data["username"]).exists())
        # User.objects；データベースにアクセス
        # 3の確認 = ログイン状態になること
        self.assertIn(SESSION_KEY, self.client.session)
        # self.client.sessionにSESSION_KEYが含まれていればTrueとなりテスト成功になる

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]  # データの抽出        print(form.errors)
        # response.contextというのは、responseで表示されているhtml等の情報が全て入っている
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )  # usernameが空になっていることのテスト
        self.assertFalse(
            form.is_valid()
        )  # .is_valid()が参照されるとフォームのfull_clean()メソッドが実行されフォームのバリデーションが行われる
        self.assertIn("このフィールドは必須です。", form.errors["username"])

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]  # データの抽出
        # response.contextというのは、responseで表示されているhtml等の情報が全て入っている
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        # usernameが空になっていることのテスト
        self.assertFalse(
            form.is_valid()
        )  # .is_valid()が参照されるとフォームのfull_clean()メソッドが実行されフォームのバリデーションが行われる
        self.assertIn("このフィールドは必須です。", form.errors["email"])

    def test_failure_post_with_empty_post(self):

        invalid_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]  # データの抽出
        # response.contextというのは、responseで表示されているhtml等の情報が全て入っている
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email=invalid_data["email"]).exists())
        self.assertFalse(
            form.is_valid()
        )  # .is_valid()が参照されるとフォームのfull_clean()メソッドが実行されフォームのバリデーションが行われる
        self.assertIn("このフィールドは必須です。", form.errors["username"])

    def test_failure_post_with_empty_password(self):

        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]  # データの抽出
        # response.contextというのは、responseで表示されているhtml等の情報が全て入っている
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(password=invalid_data["password1"]).exists()
        )  # usernameが空になっていることのテスト
        self.assertFalse(
            form.is_valid()
        )  # .is_valid()が参照されるとフォームのfull_clean()メソッドが実行されフォームのバリデーションが行われる
        self.assertIn("このフィールドは必須です。", form.errors["password1"])

    def test_failure_post_with_duplicated_user(self):
        User.objects.create(username="testuser", password="testpassword")
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertFalse(User.objects.filter(email=invalid_data["email"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("同じユーザー名が既に登録済みです。", form.errors["username"])

    def test_failure_post_with_invalid_email(self):
        invalid_data = {
            "username": "testuser",
            "email": "test",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertFalse(User.objects.filter(email=invalid_data["email"]).exists())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("有効なメールアドレスを入力してください。", form.errors["email"])

    def test_failure_post_with_too_short_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpas",
            "password2": "testpas",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]  # データの抽出
        # response.contextというのは、responseで表示されているhtml等の情報が全て入っている
        #  print(form.errors)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"], email=invalid_data["email"]).exists())
        self.assertFalse(form.is_valid())
        #  print(form.errors["password1"])
        self.assertIn("このパスワードは短すぎます。最低 8 文字以上必要です。", form.errors["password2"])

    def test_failure_post_with_password_similar_to_username(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testuser",
            "password2": "testuser",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]  # データの抽出
        # response.contextというのは、responseで表示されているhtml等の情報が全て入っている
        #  print(form.errors)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn("このパスワードは ユーザー名 と似すぎています。", form.errors["password2"])

    def test_failure_post_with_only_numbers_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "83945798",
            "password2": "83945798",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]  # データの抽出
        # response.contextというのは、responseで表示されているhtml等の情報が全て入っている
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(password=invalid_data["password1"]).exists())
        self.assertFalse(form.is_valid())
        #  print(form.errors["password1"])
        self.assertIn("このパスワードは数字しか使われていません。", form.errors["password2"])

    def test_failure_post_with_mismatch_password(self):
        invalid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpasswords",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]  # データの抽出
        # response.contextというのは、responseで表示されているhtml等の情報が全て入っている
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"], email=invalid_data["email"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("確認用パスワードが一致しません。", form.errors["password2"])


class TestLoginView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:login")
        User.objects.create_user(username="testuser", password="password1")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_success_post(self):
        valid_data = {"username": "testuser", "password": "password1"}
        response = self.client.post(self.url, valid_data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),  # 変数で指定したほうが一貫性が保てる
            status_code=302,  # リクエストされたリソースの URI が 一時的に 変更されたことを示す
            target_status_code=200,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        invalid_data = {"username": "testuserss", "password": "password1"}
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn(
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
            form.errors["__all__"],
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        invalid_data = {"username": "testuser", "password": ""}
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("このフィールドは必須です。", form.errors["password"])
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:logout")
        User.objects.create_user(username="testuser", password="password1")
        self.client.login(username="testuser", password="password1")

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,  # リクエストされたリソースの URI が 一時的に 変更されたことを示す
            target_status_code=200,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


# class TestUserProfileView(TestCase):
#     def test_success_get(self):


# class TestUserProfileEditView(TestCase):
#     def test_success_get(self):

#     def test_success_post(self):

#     def test_failure_post_with_not_exists_user(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestFollowView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_user(self):

#     def test_failure_post_with_self(self):


# class TestUnfollowView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_incorrect_user(self):


# class TestFollowingListView(TestCase):
#     def test_success_get(self):


# class TestFollowerListView(TestCase):
#     def test_success_get(self):
