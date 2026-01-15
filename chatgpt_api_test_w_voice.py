import os
from dotenv import load_dotenv
from openai import OpenAI
from audio2text import speech_to_text
from text2audio import text_to_speech

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

    user_input = ""
    
    # 音声出力テスト
    try:
        text_to_speech("こんにちは！何か質問があるにゃんか？")
    except Exception as e:
        print(f"音声出力エラー: {e}")
        print("音声出力に問題があります。テキストのみで続行します。")
    
    while user_input != "もういいや":
        try:
            user_input = speech_to_text()
        except Exception as e:
            print(f"音声入力エラー: {e}")
            user_input = input("質問を入力してください（音声入力に問題があるため、テキスト入力）: ")
        
        if user_input and user_input != "もういいや":
            reply = chat_with_gpt(role_content, user_input)
            print("ChatGPTの応答:", reply)
            try:
                text_to_speech(reply)
            except Exception as e:
                print(f"音声出力エラー: {e}")
    
    try:
        text_to_speech("またね！")
    except Exception as e:
        print("またね！")
