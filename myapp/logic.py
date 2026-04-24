import re
from typing import Dict, List, Optional

VALID_STYLE = {"polite", "casual", "mix", "kansai"}


def normalize_style(style: str) -> str:
    if style in VALID_STYLE:
        return style
    return "polite"


# 1) 状況をまとめる
def collect_detailed_context(data: dict) -> Dict[str, str]:
    return {
        "when": (data.get("when") or "").strip(),
        "where": (data.get("where") or "").strip(),
        "who": (data.get("who") or "").strip(),
        "what": (data.get("what") or "").strip(),
        "mood": (data.get("mood") or "").strip(),
        "history": data.get("history", []),
    }


# 2) 禁止語句チェック
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
                


# 3) 口調変換
def apply_style(text: str, style: str) -> str:
    style = normalize_style(style)

    if not text:
        return text
    
    if style == "polite":
        return force_polite(text)
    
    if style == "casual":
        return force_casual(text)
    
    if style == "kansai":
        return force_kansai(text)
    
    if style == "mix":
        return force_mix(text)
    
    return force_polite(text)


def force_polite(text: str) -> str:
    replacements = {
        "やんな。": "ですよね。",
        "やな。": "ですね。",
        "やで。": "ですよ。",
        "やったで。": "でした。",
        "やったな。": "でしたね。",
        "なん？": "ですか？",
        "だよね。": "ですよね。",
        "だね。": "ですね。",
        "だよ。": "ですよ。",
        "だった。": "でした。",
        "だったね。": "でしたね。",
        "なの？": "ですか？",
    }

    for old, new in sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(old, new)

    return text


def force_casual(text: str) -> str:
    text = force_polite(text)

    replacements = {
        "ですよね。": "だよね。",
        "ですね。": "だね。",
        "ですよ。": "だよ。",
        "です。": "だよ。",
        "でしたね。": "だったね。",
        "でした。": "だった。",
        "ますよね。": "るよね。",
        "ますね。": "るね。",
        "ます。": "るよ。",
        "ました。": "たよ。",
        "ません。": "ないよ。",
        "ですか？": "なの？",
        "どうされましたか？": "どうしたの？",
        "どうしましたか？": "どうしたの？",
        "辛かったですね": "辛かったね。",
        "大変でしたね": "大変だったね。",
    }

    for old, new in sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(old, new)

    return text

def force_kansai(text: str) -> str:
    text = force_polite(text)

    replacements = {
        "ですよね。": "やんな。",
        "ですね。": "やな。",
        "ですよ。": "やで。",
        "です。": "やで。",
        "でしたね。": "やったな。",
        "ますよね。": "るよな。",
        "ますね。": "るな。",
        "ます。": "るで。",
        "ました。": "たで。",
        "ません。": "へん。",
        "ですか？": "なん？",
        "どうされましたか？": "どないしたん？",
        "どうしましたか？": "どないしたん？",
        "辛かったですね。": "しんどかったな。",
        "大変でしたね。": "大変やったな。",
    }

    for old, new in sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(old, new)

    return text


def force_mix(text: str) -> str:
    # 関西弁は混ぜないので、まず敬語ベースに戻す
    text = force_polite(text)

    sentences = re.split(r'(?<=[。！？])', text)
    result = []

    for i, s in enumerate(sentences):
        s = s.strip()
        if not s:
            continue

        # 偶数文は敬語、奇数文はタメ語

        if  i % 2 == 0:
            result.append(force_polite(s))
        else:
            result.append(force_casual(s))

    return "".join(result)


# 4) 返答生成
def generate_summary(context: Dict[str, str], style: str) -> str:
    style = normalize_style(style)

    history = context.get("history", [])
    when = context.get("when", "").strip()
    where = context.get("where", "").strip()
    who = context.get("who", "").strip()
    what = context.get("what", "").strip()
    mood = context.get("mood", "").strip()
    follow_up = context.get("follow_up", "").strip()

    parts = []

    if when:
        parts.append(when)
    if where:
        parts.append(where)
    if who:
        parts.append(who)

    scene = ""
    if parts:
        scene = "、".join(parts)

    summary = ""
    if scene and what:
        summary = f"{scene}で、「{what}」って事があったんですね。"
    elif what:
        summary = f"「{what}」って事があったんですね。"
    else:
        summary = "話して下さった出来事があったんですね。"

    empathy = "それは辛かったですね。"

    if mood:
        empathy = f"「{mood}」って感じたんですね。それは辛かったですね。"

    follow = "その後どうしましたか？"

    if follow_up:
        summary = f"{summary}\nその後「{follow_up}」という流れもあったんですね。"
        follow = "その時、1番強かった気持ちはどんな気持ちでしたか？"

    reply = f"{summary}\n{empathy}\n{follow}"
    reply = apply_style(reply, style)
    return reply


# 5) 最終応答
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
        

    fallback = "今は言葉がうまく見つかりませんが、あなたの話を大切に受け止めています。"
    fallback = apply_style(fallback, style)

    if contains_banned_word(fallback, output_banned_words):
        return ""

    return fallback