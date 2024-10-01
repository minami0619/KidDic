from django.shortcuts import render, redirect
from django.views import View
from app.forms import SignupForm, LoginForm, AccountInfoForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

class PortfolioView(View):
    def get(self, request):
        return render(request, "portfolio.html")

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", context={
            "form": form
        })
    def post(self, request):
        print(request.POST)
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, "signup.html", context={
            "form": form
        })

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect("home")
        return render(request, "login.html", context={
            "form": form
        })    

class HomeView(View):
    def get(self, request):
        return render(request, "home.html")

class AccountInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user  # 現在のユーザーを取得
        form = AccountInfoForm(initial={
            'username': user.username,
            'email': user.email
        })  # フォームに現在のユーザー情報を渡す
        return render(request, "account_info.html", {
            "form": form
        })

    def post(self, request):
        user = request.user  # 現在のユーザーを取得
        form = AccountInfoForm(request.POST)  # フォームにユーザー情報を渡す

        if form.is_valid():
            # フォームからのデータをユーザーに設定
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()  # ユーザー情報を保存

            # パスワードの変更
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('password1')

            if current_password and new_password:
                if user.check_password(current_password):  # 現在のパスワードが正しいか確認
                    user.set_password(new_password)  # 新しいパスワードを設定
                    user.save()  # ユーザー情報を保存
                    messages.success(request, "パスワードが変更されました。")
                else:
                    messages.error(request, "現在のパスワードが正しくありません。")

            return redirect("home")

        return render(request, "account_info.html", {
            "form": form
        })



# class AccountInfoView(LoginRequiredMixin, View):
#     def get(self, request):
#         form = AccountInfoForm(initial={
#             'username': request.user.username,
#             'email': request.user.email,
#         })
#         return render(request, "account_info.html", {'form': form})

#     def post(self, request):
#         form = AccountInfoForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             current_password = form.cleaned_data['current_password']
#             password1 = form.cleaned_data['password1']
#             password2 = form.cleaned_data['password2']

#             # 現在のパスワードを確認
#             user = authenticate(username=request.user.username, password=current_password)
#             if user is not None:
#                 # ユーザー情報を更新
#                 request.user.username = username
#                 request.user.email = email

#                 # パスワードが一致する場合は更新
#                 if password1 == password2:
#                     request.user.set_password(password1)  # パスワードをハッシュ化して保存
#                     request.user.save()  # ユーザー情報を保存
#                     messages.success(request, 'アカウント情報が更新されました。')
#                     return redirect('home')  # リダイレクト先を指定
#                 else:
#                     messages.error(request, '新しいパスワードが一致しません。')
#             else:
#                 messages.error(request, '現在のパスワードが正しくありません。')
#         return render(request, "account_info.html", {'form': form})


# class AccountInfoView(LoginRequiredMixin, View):
#     def get(self, request):
#         form = AccountInfoForm(initial={
#             'username': request.user.username,
#             'email': request.user.email,
#         })
#         return render(request, "account_info.html", {'form': form})

#     def post(self, request):
#         form = AccountInfoForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             current_password = form.cleaned_data['current_password']
#             password1 = form.cleaned_data['password1']
#             password2 = form.cleaned_data['password2']

#             # 現在のパスワードを確認
#             user = authenticate(username=request.user.username, password=current_password)
#             if user is not None:
#                 # ユーザー情報を更新
#                 request.user.username = username
#                 request.user.email = email

#                 # パスワードが一致する場合は更新
#                 if password1 == password2 and password1:
#                     request.user.set_password(password1)  # パスワードをハッシュ化して保存
#                     request.user.save()  # ユーザー情報を保存
#                     update_session_auth_hash(request, request.user)  # セッションを更新
#                     messages.success(request, 'アカウント情報が更新されました。')
#                     return redirect('home')  # リダイレクト先を指定
#                 elif password1 != password2:
#                     messages.error(request, '新しいパスワードが一致しません。')
#                 else:
#                     messages.info(request, 'パスワードは変更されませんでした。')
#             else:
#                 messages.error(request, '現在のパスワードが正しくありません。')
        
#         return render(request, "account_info.html", {'form': form})

