from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world! This myapviews.pyp index page.")
# 話し方のスタイルに応じたメッセージの加工
if style == 'keigo':
    if not any(message.endswith(suffix) for suffix in ['です', 'ます', 'でしょう', 'ですね’, 'ですよ']):
        if "応援していますよ" not in message and "応援しているよ" not in message:
            message = f"{message} 応援していますよ。"

elif style == 'tamego':
    if not any(message.endswith(suffix) for suffix in ['だよ', 'ね', 'だね', 'だろ']):
        if "応援してるよ" not in message and "応援していますよ" not in message:
            message = f"{message} 応援してるよ。"

elif style == 'mixed':
    if ("応援してるよ" not in message) and ("応援していますよ" not in message):
        message = f"{message} 応援してるよ。応援していますよ。"
