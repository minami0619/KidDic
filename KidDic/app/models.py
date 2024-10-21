from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
import uuid


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
    family = models.ForeignKey('Family', on_delete=models.SET_NULL, null=True, blank=True, related_name="members")  # 家族との関連付け
    is_first_login = models.BooleanField(default=True, null=True)

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

class Category(models.Model):
    category_name = models.CharField(max_length=255)  # カテゴリ名
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def __str__(self):
        return self.category_name
    
class Quote(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateField(null=True, blank=True)  # 任意の開始日
    end_date = models.DateField(null=True, blank=True)  # 任意の終了日

    image = models.ImageField(upload_to='quotes_images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

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


class Family(models.Model):
    invite_url = models.CharField(max_length=255, unique=True)  # 家族招待用のURL
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    def save(self, *args, **kwargs):
        if not self.invite_url:
            self.invite_url = str(uuid.uuid4())  # UUIDを使ってURLを生成
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invite_url  # URLを文字列表現として返す