import re # 正規表現のライブラリを追加
from django.shortcuts import render, redirect
from .models import Encouragement, ForbiddenWord
from .forms import ForbiddenWordForm # フォームを追加

def index(request):
    return render(request, "myapp/index.html")

# 励ましの言葉投稿 (禁句ワードチェック・話し方選択機能を追加)
def encouragement_view(request):
    if request.method == "POST":
        message = request.POST.get("message", "").strip() # フォームの入力を取得　(空白削除)
        style = request.POST.get("style") # 話し方の選択を取得

        # 🔹 空メッセージのチェック
        if not message:
            error_message = "メッセージが空です。"
            encouragements = Encouragement.objects.all()
            return render(request, "myapp/encouragement.html", {
                "encouragements": encouragements,
                "error_message": error_message
            })

        # 🔹「気にするな」の変換処理を最優先に実行
        message = message.replace("気にするな", "気にしないで下さい。")

        # 🔹 禁句ワードのチェック (小文字・カタカナ対応)
        forbidden_words = ForbiddenWord.objects.values_list('word', flat=True)
        if any(re.search(rf'\b{re.escape(word)}\b', message, re.IGNORECASE) for word in forbidden_words):
            error_message = "投稿内容に禁句ワードが含まれています。"
            encouragements = Encouragement.objects.all()
            return render(request, "myapp/encouragement.html", {
                "encouragements": encouragements,
                "error_message": error_message
            })


        # 🔹 話し方のスタイルに応じたメッセージの加工 (重複防止も含む)
        if style == 'keigo':
            # 敬語の応援が含まれていない場合のみ追加
            # タメ語を敬語に変換
            message = message.replace("応援してるよ", "応援していますよ")

        elif style == 'tamego':
            # 敬語をタメ語に変換
            message = message.replace("応援していますよ", "応援してるよ")

        elif style == 'mixed':
            # 両方のメッセージがない場合のみ両方追加
            if "応援してるよ" not in message:
                message += "応援してるよ。"
            if "応援していますよ" not in message:
                message += " 応援していますよ。"



        # 🔹 重複する 「素晴らしい」の削除
        # message = re.sub(r'(素晴らしい)(?:\s*\1)+', r'\1', message)

        # 禁句ワードがなければ保存
        Encouragement.objects.create(message=message)

        # 投稿成功メッセージの追加
        success_message = "投稿が完了しました！"
        encouragements = Encouragement.objects.all()
        return render(request, "myapp/encouragement.html", {
            "encouragements": encouragements,
            "success_message": success_message
        })

    # GET の処理
    else:
        encouragements = Encouragement.objects.all()
        return render(request, "myapp/encouragement.html",{
            "encouragements": encouragements
        })

# from .forms import FrustrationForm
# from .models import Frustration


# 禁句ワード登録
def forbidden_word_view(request):
    if request.method == "POST":
        form = ForbiddenWordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forbidden_word')
    else:
        form = ForbiddenWordForm()

    forbidden_words = ForbiddenWord.objects.all()
    return render(request, 'myapp/forbidden_word.html', {
        'form': form,
        'forbidden_words': forbidden_words
    })


# 癪に触った出来事投稿
def frustration_view(request):
    if request.method == "POST":
        form = FrustrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "myapp/frustration.html", {
                "form":FrustrationForm(),
                "success_message":"出来事を記録しました!"
            })
    else:
        form = FrustrationForm()

    return render(request, "myapp/frustration.html", {"form": form})



