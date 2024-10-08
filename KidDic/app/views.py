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
        children = Child.objects.filter(family=family)  # 家族に関連する子どもを取得

        # フィルタリング
        keyword = request.GET.get('keyword')
        month = request.GET.get('month')
        category = request.GET.get('category')
        speaker = request.GET.get('speaker')
        sort_order = request.GET.get('sort_order', 'newest')

        if keyword:
            quotes = quotes.filter(content__icontains=keyword)
        if month:
            quotes = quotes.filter(created_at__month=month)  # created_atに基づいてフィルタリング
        if category:
            quotes = quotes.filter(category__id=category)
        if speaker:
            quotes = quotes.filter(child__nickname__icontains=speaker)

        # ソート
        if sort_order == 'newest':
            quotes = quotes.order_by('-created_at')  # created_atでソート
        elif sort_order == 'alphabet':
            quotes = quotes.order_by('content')
        elif sort_order == 'year':
            quotes = quotes.order_by('created_at')
        
        # 子どもリストと名言リストをテンプレートに渡す
        return render(request, 'home.html', {'quotes': quotes, 'children': children})



class AccountInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user  # 現在のユーザーを取得
        form = AccountInfoForm(initial={
            'username': user.username,
            'email': user.email,
            'current_user': user  # 現在のユーザーを initial に設定
        })
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
        

class QuoteCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = QuoteForm()

        # 子どもリストを取得
        children = Child.objects.filter(family=request.user.family)

        # 現在の日付を取得
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day

        # 年、月、日の範囲を生成（例えば過去10年から未来10年まで）
        year_range = range(current_year - 10, current_year + 11)
        month_range = range(1, 13)
        day_range = range(1, 32)

        return render(request, "quote_form.html", {
            "form": form,
            "children": children,
            "year_range": year_range,
            "month_range": month_range,
            "day_range": day_range,
            "current_year": current_year,
            "current_month": current_month,
            "current_day": current_day
        })

    def post(self, request):
        form = QuoteForm(request.POST)
        if form.is_valid():
            child_id = request.POST.get('child')
            child = Child.objects.get(id=child_id)
            
            # フォームから取得したデータに子どもを追加して保存
            quote = form.save(commit=False)
            quote.child = child

            # 日付処理: 任意登録対応
            start_year = request.POST.get('start-year')
            start_month = request.POST.get('start-month')
            start_day = request.POST.get('start-day')

            # 日付フィールドが設定されているかを確認しながら設定
            if start_year and start_year.isdigit():
                if start_month and start_month.isdigit():
                    if start_day and start_day.isdigit():
                        # 完全な日付が入力された場合
                        quote.start_date = datetime(
                            int(start_year), int(start_month), int(start_day)
                        )
                    else:
                        # 年と月のみ
                        quote.start_date = datetime(
                            int(start_year), int(start_month), 1
                        )
                else:
                    # 年のみ
                    quote.start_date = datetime(
                        int(start_year), 1, 1
                    )
            else:
                # 何も入力されていない場合、デフォルトで今日の日付を設定
                quote.start_date = datetime.now()

            # 保存処理
            quote.save()
            return redirect("home")

        # エラー時は再度子どもリストを取得して再描画
        children = Child.objects.filter(family=request.user.family)
        return render(request, "quote_form.html", context={"form": form, "children": children})



# class QuoteCreateView(LoginRequiredMixin, View):
#     def get(self, request):
#         # デフォルトの日付（今日の日付）を初期値に設定
#         today = timezone.now()
#         form = QuoteForm(initial={
#             'start_year': today.year,
#             'start_month': today.month,
#             'start_day': today.day,
#         })

#         # 家族に関連する子どもを取得
#         children = Child.objects.filter(family=request.user.family)

#         return render(request, "quote_form.html", context={"form": form, "children": children})

#     def post(self, request):
#         form = QuoteForm(request.POST)

#         if form.is_valid():
#             # 子どもを取得
#             child_id = request.POST.get('child')  # POSTリクエストから child のIDを取得
#             child = Child.objects.get(id=child_id)

#             # フォームから取得したデータに子どもを追加して保存
#             quote = form.save(commit=False)
#             quote.child = child

#             # 日付の処理
#             start_year = form.cleaned_data.get('start_year')
#             start_month = form.cleaned_data.get('start_month')
#             start_day = form.cleaned_data.get('start_day')

#             if start_year and start_month and start_day:
#                 quote.start_date = f"{start_year}-{start_month:02}-{start_day:02}"
#             else:
#                 # 部分的な入力にも対応（年のみや年+月）
#                 quote.start_date = None  # またはデフォルト値

#             # 終了日も同様に処理
#             end_year = form.cleaned_data.get('end_year')
#             end_month = form.cleaned_data.get('end_month')
#             end_day = form.cleaned_data.get('end_day')

#             if end_year and end_month and end_day:
#                 quote.end_date = f"{end_year}-{end_month:02}-{end_day:02}"
#             else:
#                 quote.end_date = None  # または必要に応じてデフォルト値

#             quote.save()

#             return redirect("home")

#         # エラー時は再度子どもリストを取得して再描画
#         children = Child.objects.filter(family=request.user.family)
#         return render(request, "quote_form.html", context={"form": form, "children": children})


class QuoteListView(LoginRequiredMixin, View):
    def get(self, request):
        quotes = Quote.objects.filter(child__family=request.user)
        return render(request, 'quote_list.html', {'quotes': quotes})

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
        form = QuoteForm(instance=quote)
        return render(request, 'quote_edit.html', {'form': form, 'quote': quote})

    def post(self, request, pk):
        # 名言を取得し、フォームからのデータで更新
        quote = get_object_or_404(Quote, pk=pk)
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()  # 名言を保存
            return redirect('home')  # ホーム画面にリダイレクト
        return render(request, 'quote_edit.html', {'form': form, 'quote': quote})

    def post_delete(self, request, pk):
        # 名言を取得し削除
        quote = get_object_or_404(Quote, pk=pk)
        quote.delete()
        return redirect('home')
    
# class QuoteCreateView(View):
#     def get(self, request):
#         children = Child.objects.filter(family=request.user.family)  # 子供のリストを取得
#         categories = Category.objects.all()  # カテゴリのリストを取得
#         form = QuoteForm()
#         return render(request, 'home.html', {'form': form, 'children': children, 'categories': categories, 'today_date': now().date()})

#     def post(self, request):
#         form = QuoteForm(request.POST, request.FILES)
#         if form.is_valid():
#             quote = form.save(commit=False)
#             quote.user = request.user
#             quote.save()
#             return redirect('home')  # 成功時はホームにリダイレクト
#         children = Child.objects.filter(family=request.user.family)
#         categories = Category.objects.all()
#         return render(request, 'home.html', {'form': form, 'children': children, 'categories': categories, 'today_date': now().date()})



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
