from django.db import models

  # 投稿モデル
class Post(models.Model):
    title = models.CharField(max_length=200) # タイトル(文字列)
    content = models.TextField() # 投稿内容(長文)
    created_at = models.DateTimeField(auto_now_add=True) # 作成日時

    def __str__(self):
        return self.title # 管理画面でタイトルを表示

class Encouragement(models.Model): # 励ましのメッセージのモデル
    message = models.TextField() # 励ましの言葉を保存
    style = models.CharField(
            max_length=10,
            choices=[('keigo', '敬語'), ('tamego', 'タメ語')],
            default='keigo'
    )
    category = models.CharField(max_length=50, blank=True, null=True) # カテゴリ(例: 元気が出る•励ます系)

    def __str__(self):
        return self.message

# 禁句ワードのモデルを追加
class ForbiddenWord(models.Model):
    word = models.CharField(max_length=50, unique=True) # 禁句ワード(重複を避けるためunique=True)

    def __str__(self):
        return self.word

    # 例: myapp/models.py の最後にIncidentモデルを追加

 # 出来事の投稿モデル
class Incident(models.Model):
    date = models.DateField(verbose_name="日付") # ユーザーが日付を入力
    location = models.CharField(max_length=200, verbose_name="場所")
    person = models.CharField(max_length=100, verbose_name="相手(誰に)")
    description = models.TextField(verbose_name="出来事の詳細")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} - {self.person} - {self.location}"

    class Meta:
        verbose_name = "出来事"
        verbose_name_plural = "出来事一覧"

# Create your models here.
