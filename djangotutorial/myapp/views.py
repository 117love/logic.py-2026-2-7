from django.shortcuts import render
from .logic import collect_detailed_context, respond_with_safety

def index(request):

    # まずは動作確認用：GETでアクセスしたら固定文を返す
    if request.method == "GET":
        return render(request, "myapp/index.html")
    
    # POSTされたフォーム値を取り出して logic.py に渡す
    data = request.POST

    # 入力をまとめる
    context = collect_detailed_context(data)

    # 話し方取得（デフォルト polite)
    style = request.POST.get("style", "polite")

    # 禁止後　(今は空でOK)
    output_banned_words = []

    # 安全生成(style反映される)
    reply = respond_with_safety(
        context=context,
        style=style,
        output_banned_words=output_banned_words
    )

    return render(request, "myapp/index.html", {
        "reply": reply,
        "style": style,
    })

