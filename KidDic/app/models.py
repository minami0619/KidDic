from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    user_permissions = None

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    family = models.ForeignKey('Family', on_delete=models.SET_NULL, null=True, blank=True)  # 家族との関連付け

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "users"

class Child(models.Model):
    family = models.ForeignKey('Family', on_delete=models.CASCADE)  # Familyモデルに関連付け
    nickname = models.CharField(max_length=255)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname

class Quote(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 年、月、日を個別に保存
    start_year = models.IntegerField(null=True, blank=True)  # 任意の開始年
    start_month = models.IntegerField(null=True, blank=True)  # 任意の開始月
    start_day = models.IntegerField(null=True, blank=True)  # 任意の開始日

    end_year = models.IntegerField(null=True, blank=True)  # 任意の終了年
    end_month = models.IntegerField(null=True, blank=True)  # 任意の終了月
    end_day = models.IntegerField(null=True, blank=True)  # 任意の終了日

    image = models.ImageField(upload_to='quotes_images/', null=True, blank=True)  # 画像のフィールド
    category = models.CharField(max_length=100, blank=True)  # カテゴリのフィールド

    def __str__(self):
        return self.content
    
    def get_start_date(self):
        """年、月、日を組み合わせて開始日を取得"""
        if self.start_year:
            return f"{self.start_year}年{self.start_month or ''}月{self.start_day or ''}日"
        return "不明"

    def get_end_date(self):
        """年、月、日を組み合わせて終了日を取得"""
        if self.end_year:
            return f"{self.end_year}年{self.end_month or ''}月{self.end_day or ''}日"
        return "不明"
    


class Comment(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]  # コメントの先頭20文字を返す

class Category(models.Model):
    category_name = models.CharField(max_length=255)  # カテゴリ名
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def __str__(self):
        return self.category_name

class Family(models.Model):
    invite_url = models.CharField(max_length=255)  # 家族招待用のURL
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def __str__(self):
        return self.invite_url  # URLを文字列表現として返す