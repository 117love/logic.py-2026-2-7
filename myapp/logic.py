# logic.py
import random
from typing import Dict, List, Optional

# 
# 1. 状況をまとめる
# Djangoでは入力フォームの値を context に入れて渡せばOK
# 
def collect_datailed_context() -> Dict[str, str]:
    context = {}
    context["when"] = input("いつ？(例:今日の昼、昨日など): ").strip()
    context["where"] = input("どこで？(例: 職場、学校など): ").strip()
    context["who"] = input("誰に？(例:上司、先輩、友達、同僚など): ").strip()
    context["what"] = input("どんな言動をされた？: ").strip()
    context["mood"] = input("どんな気分？(例: 怒り/悲しみ/悔しさ/不安/疲れ など): ").strip()
    return context

#
# 2) 禁止語句チェック(共通)
#
def contains_banned_word(text: str, banned_words: List[str]) -> bool:
    if not text or not banned_words:
        return False
    for w in banned_words:
        w = (w or "").strip()
        if w and w in text:
            return True
    return False
    
def filter_output(reply: str, output_banned_words: List[str]) -> Optional[str]:
    return None if contains_banned_word(reply, output_banned_words) else reply   
    

#
# 3) 口調変換(敬吾/タメ語/混合/関西弁)
#
def apply_style(text: str, style: str) -> str:
    if style == "polite":
        return text
    
    #　追加:関西弁(強め)
    if style == "kansai":
        return (
            text.replace("ですね。", "やな。")
                .replace("ですよね。", "やんな")
                .replace("ます。", "するで。")
                .replace("でした。", "やったで。")
                .replace("大変でしたね。", "めっちゃしんどかったなぁ。")
                .replace("それはしんどかったですね。", "それはしんどかったなぁ。")
                .replace("ますよね。", "やんな。")
                .replace("ますね。", "るなぁ。")
                .replace("ません。", "へん。")
                .replace("ですか？", "なん？")
                .replace("ですか。", "なん")
                .replace("ました。", "たで。")
                .replace("ました", "たで")            
        )
    
    if style == "casual":
        return (
            text.replace("ですよね。", "だよね。")
                .replace("ですね。", "だね。")
                .replace("です", "だよ。")
                .replace("ます", "るよ。")
                )

    if style == "mix":
        # 丁寧を残しつつ、少しだけ距離を縮める
        # (置き換えを増やすほど、"混合感が出ます)
        return (
            text.replace("ですね。", "やね。")
                .replace("ですよね。", "やんな.")
                .replace("大変でしたね。", "しんどかったな。")
        )

    return text    



#
# 4) 返答生成(共感 → 要約 → 質問)
# 
def generate_reply_from_context(context: Dict[str, str], style: str) -> str:
    when = context.get("when", "")
    where = context.get("where", "")
    who = context.get("who", "")
    what = context.get("what", "")
    mood = context.get("mood", "")

    empathy = {
        "怒": ["それは腹が立ちますね。", "それはイラッとしますよね。"],
        "悲": ["それは悲しくなりますよね。", "それは気持ちが沈みますよね。"],
        "悔": ["それは悔しい気持ちになりますよね。", "それは気が済まないですよね。"],
        "不安": ["それは不安になりますよね。", "その状況、落ち着かないですよね。"],
        "疲": {"それは疲れが溜まりますよね。", "それは消耗しますよね。"},

    }

    key = None
    for k in empathy.keys():
        if k in mood:
            break
        
    empathy_line = random.choice(empathy[key]) if key else "それはしんどかったですね。"

    if style == "kansai":
        summary_line = f"今日、{where}で、{who}から「{what}」って事があったんやな。"
    elif style == "casual":
        summary_line = f"今日、{where}で、{who}に「{what}」って事があったんだね。"
    elif style == "mix":
        summary_line = f"今日、{where}で、{who}から「{what}」という出来事があったんだね。"
    else:  # polite
        summary_line = f"本日, {where}で、{who}から「{what}」という出来事があったのですね。"            

    return f"{empathy_line}\n{summary_line}"

#
# 5) 最終応答（B：返答側の禁句語句を絶対に含めない)
#
def respond_with_safety(
    context: Dict[str, str],
    style: str,
    output_banned_words: List[str],
    retries: int = 5
) -> str:
    # 何度か言い換えを試す　(会話が途切れにくくなる)
    for _ in range(retries):
        reply = generate_reply_from_context(context, style)
        reply = apply_style(reply, style)
        filtered = filter_output(reply, output_banned_words)
        if filtered is not None:
            return filtered

    # 最後の砦(この文言自体も禁句チェック)
    fallback = "今はうまく言葉が見つかりませんが、あなたの話は大切に受け止めています。"
    if contains_banned_word(fallback, output_banned_words):
        return "" # どうしてもダメなら空文字 (表示しない)
    return fallback