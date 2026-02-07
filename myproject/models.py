from django.db import models

class Diary(models.Model):
    title = models.CharField(max_length=100) # タイトル(100文字まで)
    content = models.TextField()             # 内容
    created_at = models.DateTimeField(auto_now_add=True) # 作成日時

    def __str__(self):
        return self.title

# 禁句ワードのモデルを追加
class ForbiddenWord(models.Model): #
    word = models.CharField(max_length=50, unique=True) # 禁句ワード(重複を避けるためunique=True)

    def __str__(self):
        return self.word