from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

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

    @property
    def age(self):
        today = timezone.now().date()
        years = today.year - self.birthdate.year
        months = today.month - self.birthdate.month

        if today.day < self.birthdate.day:
            months -= 1

        if months < 0:
            years -= 1
            months += 12

        return f"{years}歳{months}ヶ月"

    def __str__(self):
        return self.nickname

    
class Quote(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 日付フィールド
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    image = models.ImageField(upload_to='quotes_images/', null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.content


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