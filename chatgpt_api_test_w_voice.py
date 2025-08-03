import openai
from audio2text import speech_to_text
from text2audio import text_to_speech

# OpenAI APIキーを設定
openai.api_key = "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"  # ここにAPIキーを入力

def chat_with_gpt(role, prompt):
    try:
        # ChatGPT APIを呼び出す
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # モデルを指定
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt},
            ]
        )
        # 応答を取得
        reply = response["choices"][0]["message"]["content"]
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
        exit(1)

    user_input = ""
    text_to_speech("こんにちは！何か質問があるにゃんか？")
    while user_input != "もういいや":
        user_input = speech_to_text() #input("質問を入力してください: ")
        reply = chat_with_gpt(role_content, user_input)
        #print("ChatGPTの応答:", reply)
        text_to_speech(reply)
    text_to_speech("またね！")
