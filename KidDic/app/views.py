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
from .forms import QuoteForm
from .models import Child
from django.utils import timezone

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

class HomeView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        # ユーザーのファミリーを取得
        family = request.user.family

        # 名言をファミリーに関連するものにフィルタリング
        quotes = Quote.objects.filter(child__family=family)

        # 子どもリストを取得
        children = Child.objects.filter(family=family)
        categories = Category.objects.all()  # すべてのカテゴリを取得

        # フィルタリング
        keyword = request.GET.get('keyword')
        year = request.GET.get('year')
        category = request.GET.get('category')
        speaker = request.GET.get('speaker')
        sort_order = request.GET.get('sort_order', 'newest')
        year_month = request.GET.get('year_month')

        if keyword:
            quotes = quotes.filter(content__icontains=keyword)
        if year_month:
            year, month = year_month.split('-')
            quotes = quotes.filter(start_date__year=year, start_date__month=month)
        # if year:
        #     quotes = quotes.filter(created_at__year=year)
        if category:
            quotes = quotes.filter(category__id=category)
        if speaker:
            quotes = quotes.filter(child__nickname__icontains=speaker)

        # ソート
        if sort_order == 'newest':
            quotes = quotes.order_by('-created_at')
        elif sort_order == 'alphabet':
            quotes = quotes.order_by('content')
        elif sort_order == 'year':
            quotes = quotes.order_by('created_at')
        
                # フォームの設定
        form = QuoteForm()

        # テンプレートへのデータ渡し
        return render(request, 'home.html', {
            'quotes': quotes,
            'children': children,
            'categories': categories,
            'form': form,
        })

    def post(self, request):
        form = QuoteForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)

            quote = form.save(commit=False)
            quote.start_date = form.cleaned_data.get('start_date')
            quote.end_date = form.cleaned_data.get('end_date')
            quote.child = form.cleaned_data.get('child')
            quote.description = form.cleaned_data.get('description')
            # quote.category = form.cleaned_data.get('category')
            # category_id = request.POST.get('category')
            # if category_id:
            #     category = Category.objects.get(id=category_id)
            #     quote.category = category
            # else:
            #     quote.category = None  # カテゴリが選択されていない場合はNoneを設定
            
            category_id = form.cleaned_data.get('category')
            if category_id:
                category = Category.objects.get(id=category_id)
                quote.category = category
            else:
                quote.category = None

            quote.save()
            return redirect('home')
        
            # フォームが無効だった場合のデバッグ
            print(form.errors)  # これでコンソールにエラーが表示される
            print(request.POST)  # 送信されたデータも確認できる

        # エラー時は再度レンダリング
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
        # ユーザーにFamilyが設定されていない場合、Familyを作成する
        if request.user.family is None:
            family = Family.objects.create(invite_url="example_invite_url")
            request.user.family = family
            request.user.save()

    def post(self, request):
        print(f"User's family: {request.user.family}")
        # 入力されたニックネームと生年月日を取得
        nicknames = request.POST.getlist('nickname')
        birthdates = request.POST.getlist('birthdate')

        # 複数の子ども情報を保存
        for nickname, birthdate in zip(nicknames, birthdates):
            try:
                child = Child(
                    nickname=nickname,
                    birthdate=birthdate,
                    family=request.user.family  # familyを設定
                )
                child.save()  # エラーがここで発生したらキャッチ
            except IntegrityError as e:
                print(f"Error saving child: {e}")
                return render(request, 'error.html', {'message': f'保存エラー: {e}'})

        return redirect('home')
        

class QuoteDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        comments = quote.comment_set.all()  # 名言に紐づくコメント
        form = CommentForm()
        return render(request, 'quote_detail.html', {'quote': quote, 'comments': comments, 'form': form})

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
        return render(request, 'quote_detail.html', {'quote': quote, 'comments': comments, 'form': form})

class QuoteToggleSNSView(LoginRequiredMixin, View):
    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk, child__family=request.user)
        quote.public = not quote.public
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

    # def post_delete(self, request, pk):
    #     # 名言を取得し削除
    #     quote = get_object_or_404(Quote, pk=pk)
    #     quote.delete()
    #     return redirect('home')
class QuoteDeleteView(View):
    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        quote.delete()
        return redirect('home')

    
