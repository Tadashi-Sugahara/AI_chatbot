from openai import OpenAI
import os
import sys
from dotenv import load_dotenv

# ALSA エラー出力を抑制
os.environ['ALSA_CONF'] = '/dev/null'

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
    print("=== 音声AI チャットボット (安定版) ===")
    
    # ロール設定をテキストファイルから読み込む
    try:
        with open("role.txt", "r", encoding="utf-8") as role_file:
            role_content = role_file.read().strip()
        print("✓ ロール設定を読み込みました。")
    except FileNotFoundError:
        print("⚠ role.txt が見つかりません。デフォルトロールを使用します。")
        role_content = "あなたは親切なアシスタントです。"

    # 安全な音声モジュールをインポート
    try:
        from audio2text_safe import speech_to_text
        from text2audio_safe import text_to_speech
        audio_enabled = True
        print("✓ 音声機能が有効です。")
    except ImportError:
        print("⚠ 音声機能が無効です。テキストのみで動作します。")
        audio_enabled = False
        
        def speech_to_text():
            return None
            
        def text_to_speech(text):
            print(f"[音声]: {text}")

    # 初期挨拶
    greeting = "こんにちは！何か質問があるにゃんか？"
    print(f"AI: {greeting}")
    if audio_enabled:
        print("🔊 音声出力中...")
        text_to_speech(greeting)
    
    user_input = ""
    conversation_count = 0
    
    print("\n=== チャット開始 ===")
    print("終了するには '終了', 'もういいや', 'quit' のいずれかを入力してください。")
    print("音声入力が失敗した場合、自動的にテキスト入力に切り替わります。\n")
    
    while user_input.lower() not in ["もういいや", "終了", "quit", "exit"]:
        conversation_count += 1
        print(f"--- 会話 {conversation_count} ---")
        
        # 音声入力を試行
        if audio_enabled:
            print("🎤 音声入力待機中... (話しかけてください)")
            user_input = speech_to_text()
        else:
            user_input = None
        
        # 音声入力に失敗した場合、テキスト入力
        if user_input is None or user_input.strip() == "":
            user_input = input("💬 質問を入力してください: ").strip()
        else:
            print(f"🎤 音声入力: {user_input}")
        
        # 終了チェック
        if user_input.lower() in ["もういいや", "終了", "quit", "exit", ""]:
            break
            
        # ChatGPT応答取得
        print("🤖 ChatGPTが応答を生成中...")
        reply = chat_with_gpt(role_content, user_input)
        print(f"AI: {reply}")
        
        # 音声出力
        if audio_enabled:
            print("🔊 音声出力中...")
            text_to_speech(reply)
        
        print()  # 空行で見やすく
    
    # 終了メッセージ
    farewell = "またね！"
    print(f"\n🎉 チャット終了: {farewell}")
    if audio_enabled:
        text_to_speech(farewell)