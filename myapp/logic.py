# logic.py
import random
from typing import Dict, List, Optional

VALID_STYLE = {"polite", "casual", "mix", "kansai"}

def normalize_style(style: str) -> str:
    if style in VALID_STYLE:
        return style
    return "polite"

# 
# 1. 状況をまとめる
def collect_detailed_context(data: dict) -> Dict[str, str]:
    return {
        "when":  (data.get("when") or "" ).strip(),
        "where":  (data.get("where") or "").strip(),
        "who": (data.get("who") or "").strip(),
        "what": (data.get("what") or "").strip(),
        "mood": (data.get("mood") or "").strip(),
        "history": []
    }

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
def apply_style(text: str, style: str) -> str:
    style = normalize_style(style)

    if style == "polite":
        return text
       
    if style == "kansai":
        replacements = {
            "ですね。": "やな。",
            "ですよね。": "やんな",
            "ます。": "するで。",
            "でした。": "やったで。",
            "ますよね。": "やんな。",
            "ますね。": "るなぁ。",
            "ません。": "へん。",
            "ですか？": "なん？",            
        }
    
    elif style == "casual":
        replacements = {
            "ですよね。": "だよね。",
            "ですね。": "だね。",
            "です": "だよ。",
            "ます": "るよ。",
            "ました。": "たよ。",
            "でした。": "だった。",
        }        

    elif style == "mix":
        replacements = {
            "ですね。": "やね。",
            "ですよね。": "やんな。",
            "でしたね。": "やったな。",
        }

    else:
        return text

    for before, after in replacements.items():
        text = text.replace(before, after)

    return text    


# 4) 返答生成(共感 → 要約 → 質問)
def generate_summary(context: Dict[str, str], style: str) -> str:
    style = normalize_style(style)

    history = context.get("history", [])

    history_text = ""
    if history:
        history_text += "これまでの会話:\n"
        for h in history[-6:]:
            role = "あなた" if h["role"] == "user" else "アプリ"
            history_text += f"{role}: {h['content']}\n"
        history_text += "\n"    

    when = context.get("when", "").strip()
    where = context.get("where", "").strip()
    who = context.get("who", "").strip()
    what = context.get("what", "").strip()

    base = ""

    if when:
        base += f"{when}"

    if where:
        if base:
            base += "、"
        if where.endswith("で"):    
            base += f"{where}で"
        else:
            base += f"{where}で"        

    if who:
        if base:
            base += "、"
        base += f"{who}に"

    if what:
        if base:
            base += f"「{what}」って事があった"
        else:
            base = f"「{what}」って事があった"

    

    #--- 文末スタイル ---         
    if style == "polite":
        summary = f"{base}んですね。"
        empathy = "それはとても辛かったですね。"
        follow = "その後どうされましたか？"

    elif style == "casual":
        summary = f"{base}んだね。"
        empathy = "それは辛かったよね。"
        follow = "その後どうしたの？"

    elif style == "kansai":
        summary = f"{base}んやな。"
        empathy = "それはほんまにしんどかったな。"
        follow = "その後どないしたん？"

    elif style == "mix":
        summary = f"{base}んですね。"
        empathy = "それは辛かったですね。"
        follow = "その後はどうしたんですか？"

    else:
        summary = base
        empathy = ""
        follow = ""

    return f"{history_text}{summary}\n{empathy}\n{follow}"                    

# 5) 最終応答（B：返答側の禁句語句を絶対に含めない)
def respond_with_safety(
    context: Dict[str, str],
    style: str,
    output_banned_words: List[str],
    retries: int = 5
) -> str:
    
    style = normalize_style(style)
    
    for _ in range(retries):
        reply = generate_summary(context, style)
        filtered = filter_output(reply, output_banned_words)
        if filtered is not None:
            return filtered

    fallback = "今はうまく言葉が見つかりませんが、あなたの話は大切に受け止めています。"
    if contains_banned_word(fallback, output_banned_words):
        return "" # どうしてもダメなら空文字 (表示しない)
    
    return fallback