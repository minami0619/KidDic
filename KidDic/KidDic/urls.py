"""
URL configuration for KidDic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from app.views import PortfolioView, SignupView, LoginView, HomeView, AccountInfoView, ChildCreateView, QuoteDetailView, QuoteToggleSNSView, CommentDeleteView, QuoteEditView, QuoteDeleteView, ChildListView, ChildEditView, ChildDeleteView, FamilyInviteView, FamilySignupView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',PortfolioView.as_view(), name="portfolio"),
    path('signup/',SignupView.as_view(), name="signup"),
    path('login/',LoginView.as_view(), name="login"),
    path('home/',HomeView.as_view(), name="home"),
    path('account-info/', AccountInfoView.as_view(), name='account_info'),
    path('children/add/', ChildCreateView.as_view(), name='child_add'),
    path('children/', ChildListView.as_view(), name='child_list'),
    path('children/<int:child_id>/edit/', ChildEditView.as_view(), name='child_edit'),
    path('children/<int:child_id>/delete/', ChildDeleteView.as_view(), name='child_delete'),
    path('quotes/<int:pk>/', QuoteDetailView.as_view(), name='quote_detail'),
    path('quotes/<int:pk>/edit/', QuoteEditView.as_view(), name='quote_edit'),  # 名言編集画面のURLパターン
    path('quotes/<int:pk>/delete/', QuoteDeleteView.as_view(), name='quote_delete'),  # 名言削除用のURLパターン
    path('quotes/<int:pk>/toggle_sns/', QuoteToggleSNSView.as_view(), name='quote_toggle_sns'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('invite/', FamilyInviteView.as_view(), name='family_invite'),
    path('invite/<str:invite_url>/', FamilySignupView.as_view(), name='family_signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
