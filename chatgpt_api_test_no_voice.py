from openai import OpenAI
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# OpenAI クライアントを初期化
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEYが.envファイルに設定されていません")
client = OpenAI(api_key=api_key)

def chat_with_gpt(role, prompt):
    try:
        # ChatGPT APIを呼び出す
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # モデルを指定
            #model="gpt-4",  # モデルを指定
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt},
            ]
        )
        # 応答を取得
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        return f"エラーが発生しました: {e}"

if __name__ == "__main__":
    # ロール設定をテキストファイルから読み込む
    try:
        with open("role.txt", "r", encoding="utf-8") as role_file:
            role_content = role_file.read().strip()  # ロール設定を読み込み
    except FileNotFoundError:
        print("エラー: role.txt ファイルが見つかりません。")
        role_content = "あなたは親切なアシスタントです。"

    print("テキストチャットボット（音声機能なし）")
    print("'終了'と入力すると終了します。")
    
    while True:
        user_input = input("質問を入力してください: ")
        if user_input == "終了":
            break
        reply = chat_with_gpt(role_content, user_input)
        print("ChatGPTの応答:", reply)
    
    print("チャットを終了しました。")