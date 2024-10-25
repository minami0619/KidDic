from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from app.forms import SignupForm, LoginForm, AccountInfoForm, ChildForm, QuoteForm, CommentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from app.models import Child, Quote, Comment, Category, Family
from django.utils.timezone import now
from django.db import IntegrityError
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import QuoteForm
from .models import Child, Quote, Category
from django.utils import timezone
from django.urls import reverse

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
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return post_login_redirect(user)  # 共通のリダイレクト関数を使用
        return render(request, "signup.html", context={
            "form": form
        })

def post_login_redirect(user):
    """子ども情報が登録済みかを確認し、適切な画面にリダイレクト"""
    if not Child.objects.filter(family=user.family).exists():
        return redirect("child_add")  # 子ども情報未登録の場合
    return redirect("home")  # 子ども情報が登録済みの場合


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", context={
            "form": form
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            return post_login_redirect(user)  # 共通のリダイレクト関数を使用
        return render(request, "login.html", context={
            "form": form
        })



class HomeView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, *args, **kwargs):
        # ユーザーが認証されていない場合、公開状態の名言のみ表示
        if not request.user.is_authenticated:
            quotes = Quote.objects.filter(public=True)
            family = None
            children = None
        else:
            family = request.user.family
            # ユーザーのファミリーに関連する名言を取得
            quotes = Quote.objects.filter(child__family=family).order_by('-created_at')
            children = Child.objects.filter(family=family)

        # フィルタリング条件を取得
        keyword = request.GET.get('keyword')
        year_month = request.GET.get('year_month')
        category = request.GET.get('category')
        speaker = request.GET.get('speaker')

        if keyword:
            quotes = quotes.filter(content__icontains=keyword)
        if year_month:
            year, month = year_month.split('-')
            quotes = quotes.filter(start_date__year=year, start_date__month=month)
        if category:
            quotes = quotes.filter(category__id=category)
        if speaker:
            quotes = quotes.filter(child__nickname__icontains=speaker)

        # ソート順の取得
        sort_order = request.GET.get('sort_order', 'newest')

        if sort_order == 'newest':
            quotes = quotes.order_by('-created_at')
        elif sort_order == 'oldest':
            quotes = quotes.order_by('created_at')
        elif sort_order == 'alphabet':
            quotes = quotes.order_by('content')

        # すべてのカテゴリを取得
        categories = Category.objects.all()

        # フォームの設定
        form = QuoteForm() if request.user.is_authenticated else None

        # テンプレートにデータを渡してレンダリング
        return render(request, 'home.html', {
            'quotes': quotes,
            'children': children,
            'categories': categories,
            'form': form,
        })

    def post(self, request):
        form = QuoteForm(request.POST, request.FILES)
        print("Form data:", request.POST) 
        if form.is_valid():
            quote = form.save(commit=False)
            quote.start_date = form.cleaned_data.get('start_date')
            quote.end_date = form.cleaned_data.get('end_date')
            quote.child = form.cleaned_data.get('child')
            quote.description = form.cleaned_data.get('description')
            quote.category = form.cleaned_data.get('category')
            quote.user = request.user
            print("Public field:", form.cleaned_data.get('public'))  # デバッグ用
            
            # publicフィールドの処理: 'on' か 'off' をチェック
            if request.POST.get('public') == 'on':
                quote.public = True
            else:
                quote.public = False
            quote.save()
            return redirect('home')

        # エラー時のレンダリング
        family = request.user.family
        children = Child.objects.filter(family=family)
        quotes = Quote.objects.filter(child__family=family)
        categories = Category.objects.all()
        return render(request, "home.html", {
            'form': form,
            'children': children,
            'quotes': quotes,
            'categories': categories,
        })




class AccountInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user  # 現在のユーザーを取得
        form = AccountInfoForm(initial={
            'username': user.username,
            'email': user.email,
            'current_user': user  # 現在のユーザーを initial に設定
        })
        return render(request, "account_info.html", {"form": form})

    def post(self, request):
        user = request.user  # 現在のユーザーを取得
        form = AccountInfoForm(request.POST, initial={'current_user': user})  # フォームにユーザー情報を渡す

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

        return render(request, "account_info.html", {"form": form})    

class ChildCreateView(View):
    def get(self, request):
        return render(request, 'child_form.html', {'today_date': now().date()})

    def post(self, request):
        if request.user.family is None:
            family = Family.objects.create(invite_url="example_invite_url")
            request.user.family = family
            request.user.save()

        nicknames = request.POST.getlist('nickname')
        birthdates = request.POST.getlist('birthdate')
        errors = []

        for nickname, birthdate in zip(nicknames, birthdates):
            try:
                child = Child(
                    nickname=nickname,
                    birthdate=birthdate,
                    family=request.user.family
                )
                child.save()
            except IntegrityError as e:
                errors.append(f"Error saving {nickname}: {e}")

        if errors:
            return render(request, 'child_form.html', {
                'today_date': now().date(),
                'errors': errors
            })

        return redirect('home')

class ChildListView(View):
    def get(self, request):
        children = Child.objects.filter(family=request.user.family)
        return render(request, 'child_list.html', {'children': children})

class ChildEditView(View):
    def get(self, request, child_id):
        # 特定の子供を取得し、フォームに渡す
        child = get_object_or_404(Child, id=child_id, family=request.user.family)
        form = ChildForm(instance=child)  # 子供の情報をフォームに初期表示
        return render(request, 'child_edit.html', {'form': form, 'child': child})

    def post(self, request, child_id):
        print(child_id)
        # 特定の子供を取得し、POSTデータをフォームに渡す
        child = get_object_or_404(Child, id=child_id, family=request.user.family)
        form = ChildForm(request.POST, instance=child)  # フォームにPOSTデータを渡す
        if form.is_valid():  # フォームのバリデーションを実行
            form.save()  # バリデーションが通れば、データを保存
            return redirect('child_list')  # 保存後、一覧ページへリダイレクト
        return render(request, 'child_edit.html', {'form': form})  # エラー時にフォームを再表示

class ChildDeleteView(View):
    def post(self, request, child_id):
        child = get_object_or_404(Child, id=child_id, family=request.user.family)
        child.delete()
        return redirect('child_list')
        

class QuoteDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        comments = quote.comment_set.all()  # 名言に関連するコメント
        form = CommentForm()
        home_url = request.build_absolute_uri(reverse('home'))  # ホーム画面のURLを取得

        return render(request, 'quote_detail.html', {
            'quote': quote,
            'comments': comments,
            'form': form,
            'home_url': home_url,
            'public': quote.public
        })

    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.quote = quote
            comment.user = request.user
            comment.save()
            return redirect('quote_detail', pk=pk)
        comments = quote.comment_set.all()
        return render(request, 'quote_detail.html', {
            'quote': quote,
            'comments': comments,
            'form': form
        })

    def post_public_toggle(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote.public = request.POST.get('public') == 'on'  # SNS公開のトグルスイッチ状態を保存
        quote.save()
        return redirect('quote_detail', pk=pk)

    



class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        comment.delete()
        return redirect('quote_detail', pk=comment.quote.pk)
    
class QuoteEditView(View):
    def get(self, request, pk):
        # 名言を取得し、編集用フォームを表示
        quote = get_object_or_404(Quote, pk=pk)
        children = Child.objects.filter(family=request.user.family)  # 家族内の子どもを取得
        form = QuoteForm(instance=quote)
        return render(request, 'quote_edit.html', {'form': form, 'quote': quote, 'children': children})

    def post(self, request, pk):
        # 名言を取得し、フォームからのデータで更新
        quote = get_object_or_404(Quote, pk=pk)
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()  # 名言を保存
            return redirect('home')  # ホーム画面にリダイレクト
        return render(request, 'quote_edit.html', {'form': form, 'quote': quote})

class QuoteDeleteView(View):
    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote.delete()
        return redirect('home')

class FamilyInviteView(View):
    def get(self, request):
        family = request.user.family
        if family is None:
            # 家族が未設定の場合、新しいFamilyを作成
            family = Family.objects.create()
            request.user.family = family
            request.user.save()

        invite_url = request.build_absolute_uri(f"/invite/{family.invite_url}")
        members = family.members.all()  # 関連するユーザー（家族のメンバー）を取得
        return render(request, 'family_invite.html', {
            'members': members,
            'invite_url': invite_url
        })

class FamilySignupView(View):
    def get(self, request, invite_url):
        form = SignupForm()
        return render(request, 'family_signup.html', {'form': form, 'invite_url': invite_url})

    def post(self, request, invite_url):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            family = Family.objects.get(invite_url=invite_url)
            user.family = family
            user.save()
            login(request, user)
            return redirect('home')
        return render(request, 'family_signup.html', {'form': form, 'invite_url': invite_url})  # フォームが無効だった場合

