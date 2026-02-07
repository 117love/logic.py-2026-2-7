from django import forms
from .models import Encouragement, ForbiddenWord

class EncouragementForm(forms.ModelForm):
    class Meta:
        model = Encouragement
        fields = ['message','style']
        widgets  = {
            'message': forms.Textarea(attrs={'rows':4, 'cols':50, 'placeholder': '励ましのメッセージを入力して下さい'})
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message or not message.strip():
            raise forms.ValidationError("メッセージが空です。")

        # 「気にするな」の変換処理
        if "気にするな" in message:
            message = message.replace("気にするな", "気にしないで下さい。")

        # 禁句ワードのチェック
        forbidden_words = ForbiddenWord.objects.values_list('word', flat=True)
        for word in forbidden_words:
            if word.lower() in message.lower():
                raise forms.ValidationError("投稿内容に禁句ワードが含まれています。")

        return message

from .models import ForbiddenWord # ForbiddenWordモデルをインポート

class ForbiddenWordForm(forms.ModelForm):
    class Meta:
        model = ForbiddenWord
        fields = ['word'] # 禁句ワードの入力欄