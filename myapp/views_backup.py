from django.shortcuts import render, redirect
from .models import Encouragement, ForbiddenWord # まとめてインポート
from .forms import ForbiddenWordForm # フォームのインポート

def index(request):
    return render(request, "myapp/index.html")

# 励ましの言葉投稿(禁句ワードチェック機能を追加)
def encouragement_view(request):
    if request.method == "POST":
        message = request.POST.get("message") # フォームの入力を取得
        style = request.POST.get("style") # 話し方の選択を取得

        if message:
            # 話し方のスタイルに応じたメッセージの加工
            if style == 'keigo':
                if message.endswith(('です', 'ます', 'でしょう', 'ですね', 'ですよ')):
                    message = message
                elif message.endswith(('よ', 'ね')):
                    message = f"{message} 応援していますよ。" # より自然な敬語
                elif message == "気にするな":
                    message = "気にしないで下さい。"
                else:
                    message = f"{message}ですね。"

            elif style == 'tamego':
                if message.endswith(('だよ', 'じゃん', 'ぜ', 'で', 'ね', 'ないで')):
                    message = message
                elif message == "頑張りすぎないで":
                    message = "頑張りすぎないでね。"
                else:
                    message = f"{message}だよ！"

# 禁句ワードのチェック
            forbidden_words = ForbiddenWord.objects.values_list('word', flat=True)
            if any(word in message for word in forbidden_words):
                # 禁句ワードが含まれていた場合の処理
                error_message = "投稿内容に禁句ワードが含まれています。"
                encouragements = Encouragement.objects.all()
                return render(request, "myapp/encouragement.html", {
                    "encouragements": encouragements,
                    "error_message": error_message
                })

        # 禁句ワードがなければ保存
        Encouragement.objects.create(message=message)
        return redirect("encouragement") #

    encouragements = Encouragement.objects.all()
    return render(request, "myapp/encouragement.html", {"encouragements": encouragements})

# 禁句ワード登録
def forbidden_word_view(request):
    if request.method == "POST":
        form = ForbiddenWordForm(request.POST)
        if form.is_valid():
            form.save() # フォームのデータを保存
            return redirect('forbidden_word')
    else:
        form = ForbiddenWordForm()

    forbidden_words = ForbiddenWord.objects.all()
    return render(request, 'myapp/forbidden_word.html',{'form': form, 'forbidden_words': forbidden_words})
