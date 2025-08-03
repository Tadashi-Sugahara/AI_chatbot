import openai

# OpenAI APIキーを設定
openai.api_key = "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"  # ここにAPIキーを入力

def chat_with_gpt(prompt):
    try:
        # ChatGPT APIを呼び出す
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # モデルを指定
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": prompt},
            ]
        )
        # 応答を取得
        reply = response["choices"][0]["message"]["content"]
        return reply
    except Exception as e:
        return f"エラーが発生しました: {e}"

if __name__ == "__main__":
    user_input = input("質問を入力してください: ")
    reply = chat_with_gpt(user_input)
    print("ChatGPTの応答:", reply)