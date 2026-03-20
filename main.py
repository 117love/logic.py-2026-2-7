from myapp.logic import collect_detailed_context, respond_with_safety

def main():
    print("寄り添い会話アプリを開始します(exitで終了)")

    # 話し方を選択
    style = input("話し方を選んで下さい (polite / kansai / mix / casual): ").strip()
    if style not in ["polite", "kansai", "mix", "casual"]:
        style = "polite"

    # 言われたくない言葉(返答側の禁止語句)
    banned = input("言われたくない言葉（カンマ区切り、未入力OK): ").strip()
    output_banned_words = [w.strip() for w in banned.split(",") if w.strip()]

    # 会話履歴
    conversation_history = []    

    while True:
        print("\n--- 状況を入力して下さい ---")

        data = {
            "when": input("いつ？ "),
            "where": input("どこで？ "),
            "who": input("誰から？"),
            "what": input("どんな言動をされた？"),
            "mood": input("どんな気持ち？")
        }

        if data["what"].lower() == "exit":
            print("終了します")
            break

        context = collect_detailed_context(data)

        # 履歴をcontextに渡す
        context["history"] = conversation_history

        reply = respond_with_safety(
            context=context,
            style=style,
            output_banned_words=output_banned_words,
            retries=5
        )

        if reply:
            print("\nアプリ:")
            print(reply)

            # 履歴保存
            conversation_history.append({"role": "assistant", "content": reply})

            print("\nあなた:")
            follow_input = input("> ").strip()

            if follow_input:
                print("あなた:", follow_input)

                # 履歴保存
                conversation_history.append({"role": "user", "content": follow_input})

                context["follow_up"] = follow_input
                context["history"] = conversation_history

                reply2 = respond_with_safety(
                    context=context,
                    style=style,
                    output_banned_words=output_banned_words,
                    retries=5
                )

                if reply2:
                    print("\nアプリ:")
                    print(reply2)

            print("\nその時、1番強かった気持ちはどんな気持ちでしたか？")
            mood_input = input("> ").strip()

            reply3 = ""

            if mood_input:
                print("あなた:", mood_input)

                # 履歴保存
                conversation_history.append({"role": "user", "content": mood_input})

                context["mood"] = mood_input
                context["history"] = conversation_history

                reply3 = respond_with_safety(
                    context=context,
                    style=style,
                    output_banned_words=output_banned_words,
                    retries=5
                )

            if reply3:
                print("\nアプリ:")
                print(reply3)    
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

# test