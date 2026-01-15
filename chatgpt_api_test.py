import os
from dotenv import load_dotenv
from openai import OpenAI

# .envファイルから環境変数を読み込み
load_dotenv()

# OpenAI クライアントを初期化
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEYが.envファイルに設定されていません")
client = OpenAI(api_key=api_key)

def chat_with_gpt(prompt):
    try:
        # ChatGPT APIを呼び出す
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # モデルを指定
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": prompt},
            ]
        )
        # 応答を取得
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        return f"エラーが発生しました: {e}"

if __name__ == "__main__":
    user_input = input("質問を入力してください: ")
    reply = chat_with_gpt(user_input)
    print("ChatGPTの応答:", reply)