from django.contrib import admin
from .models import Diary # models.py の Diary をインポート

admin.site.register(Diary) # Diary モデルを管理画面に登録