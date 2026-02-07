from myapp.logic import collect_datailed_context, respond_with_safety

def main():
    print("寄り添い会話アプリを開始します(exitで終了)")

    # 話し方を選択
    style = input("話し方を選んで下さい (polite / kansai / mix / casual): ").strip()
    if style not in ["polite", "kansai", "mix", "casual"]:
        style = "polite"

    # 言われたくない言葉(返答側の禁止語句)
    banned = input("言われたくない言葉（カンマ区切り、未入力OK): ").strip()
    output_banned_words = [w.strip() for w in banned.split(",") if w.strip()]    

    while True:
        print("\n--- 状況を入力して下さい ---")
        context = collect_datailed_context()

        if context.get("what") == "exit":
            print("終了します")
            break

        reply = respond_with_safety(
            context=context,
            style=style,
            output_banned_words=output_banned_words,
            retries=5
        )

        if reply:
            print("\nアプリ:")
            print(reply)

            print("\nその時、1番強かった気持ちはどんな気持ちでしたか？")
            follow_up = input("> ").strip()

            if follow_up:
                context["follow_up_mood"] = follow_up

        else:
            print("\nアプリ:(安全の為表示出来る文章がありませんでした)")

        # (返信を出した直後)
        print("\n続けますか？ (y / exit)")
        next_action = input("> ").strip()

        if next_action == "exit":
            print("終了します")
            break    
    
if __name__ == "__main__":
    main()            

