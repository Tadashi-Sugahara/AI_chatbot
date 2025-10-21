from openai import OpenAI
import os
import sys
from dotenv import load_dotenv

# ALSA エラー出力を抑制
os.environ['ALSA_CONF'] = '/dev/null'
os.environ['PULSE_RUNTIME_PATH'] = '/dev/null'

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

def safe_speech_to_text():
    """音声入力の安全な実装"""
    try:
        # ALSAエラーを標準エラー出力に向けないようにリダイレクト
        original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        
        from audio2text import speech_to_text
        result = speech_to_text()
        
        # 標準エラー出力を元に戻す
        sys.stderr.close()
        sys.stderr = original_stderr
        
        return result
    except Exception as e:
        # 標準エラー出力を確実に元に戻す
        if 'original_stderr' in locals():
            sys.stderr.close()
            sys.stderr = original_stderr
        return None

def safe_text_to_speech(text):
    """音声出力の安全な実装"""
    try:
        # ALSAエラーを標準エラー出力に向けないようにリダイレクト
        original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        
        from text2audio import text_to_speech
        text_to_speech(text)
        
        # 標準エラー出力を元に戻す
        sys.stderr.close()
        sys.stderr = original_stderr
        
        return True
    except Exception as e:
        # 標準エラー出力を確実に元に戻す
        if 'original_stderr' in locals():
            sys.stderr.close()
            sys.stderr = original_stderr
        print(f"音声機能エラー: {str(e)[:100]}...")  # エラーを短縮表示
        return False

if __name__ == "__main__":
    print("=== 音声AI チャットボット (改良版) ===")
    
    # ロール設定をテキストファイルから読み込む
    try:
        with open("role.txt", "r", encoding="utf-8") as role_file:
            role_content = role_file.read().strip()
        print("ロール設定を読み込みました。")
    except FileNotFoundError:
        print("role.txt が見つかりません。デフォルトロールを使用します。")
        role_content = "あなたは親切なアシスタントです。"

    # 初期音声出力テスト
    print("音声機能をテスト中...")
    if safe_text_to_speech("こんにちは！音声機能のテストです。"):
        print("音声出力: OK")
        audio_output_enabled = True
    else:
        print("音声出力: 無効（テキストのみ）")
        audio_output_enabled = False
        
    user_input = ""
    conversation_count = 0
    
    print("\n=== チャット開始 ===")
    print("'終了'または'もういいや'と入力すると終了します。")
    
    while user_input not in ["もういいや", "終了", "quit", "exit"]:
        conversation_count += 1
        print(f"\n--- 会話 {conversation_count} ---")
        
        # 音声入力を試行
        print("音声入力を待機中... (20秒でタイムアウト)")
        user_input = safe_speech_to_text()
        
        if user_input is None or user_input.strip() == "":
            # 音声入力に失敗した場合、テキスト入力にフォールバック
            print("音声入力に失敗しました。テキスト入力に切り替えます。")
            user_input = input("質問を入力してください: ").strip()
        else:
            print(f"音声入力: {user_input}")
        
        # 終了チェック
        if user_input.lower() in ["もういいや", "終了", "quit", "exit", ""]:
            break
            
        # ChatGPT応答取得
        print("ChatGPTが応答を生成中...")
        reply = chat_with_gpt(role_content, user_input)
        print(f"ChatGPT: {reply}")
        
        # 音声出力
        if audio_output_enabled:
            print("音声出力中...")
            safe_text_to_speech(reply)
    
    # 終了メッセージ
    print("\n=== チャット終了 ===")
    if audio_output_enabled:
        safe_text_to_speech("またね！")
    else:
        print("またね！")