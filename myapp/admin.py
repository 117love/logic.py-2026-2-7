from django.contrib import admin
from .models import Post, Encouragement, ForbiddenWord # ForbiddenWord を含む全てのモデルをインポート


admin.site.register(Post)
admin.site.register(Encouragement) # これで管理画面から編集可能に

# Forbiddenword はデコレータを使って登録
@admin.register(ForbiddenWord)
class ForbiddenWordAdmin(admin.ModelAdmin):
    list_display = ['word'] # 管理画面で表示する項目