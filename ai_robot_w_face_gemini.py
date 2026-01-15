# GIFアニメーションを表示しながらGeminiと対話するためのプログラムです。
import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
from dotenv import load_dotenv
from google import genai
from audio2text_safe import speech_to_text
from text2audio_safe import text_to_speech
from threading import Thread
import threading

# .envファイルから環境変数を読み込み
load_dotenv()

# 古い一時音声ファイルをクリーンアップ
def cleanup_temp_audio_files():
    """プログラム開始時に古い一時音声ファイルを削除"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(script_dir):
        if filename.startswith("temp_audio_") and filename.endswith(".mp3"):
            try:
                os.remove(os.path.join(script_dir, filename))
                print(f"[クリーンアップ]: {filename}を削除しました")
            except Exception as e:
                print(f"[クリーンアップエラー]: {filename} - {e}")

cleanup_temp_audio_files()

# Google Gemini APIキーを設定
api_key_gemini = os.getenv('GOOGLE_API_KEY')
if not api_key_gemini:
    raise ValueError("GOOGLE_API_KEYが.envファイルに設定されていません")
client = genai.Client(api_key=api_key_gemini)

def chat_with_gemini(role, prompt):
    try:
        # Gemini APIを呼び出す
        print(f"API呼び出し中... モデル: models/gemini-2.5-flash")
        full_prompt = f"{role}\n\nユーザー: {prompt}"
        response = client.models.generate_content(
            model='models/gemini-2.5-flash',
            contents=full_prompt
        )
        print(f"API応答受信完了")
        return response.text
    except Exception as e:
        print(f"APIエラー詳細: {type(e).__name__}: {e}")
        return f"エラーが発生しました: {e}"

def open_gif_image(gif_path, width, height):
    # Tkinterウィンドウを作成
    root = tk.Tk()
    root.title("Robot Face GIF")

    # ウィンドウサイズを設定（全画面表示なし）
    root.geometry(f"{width}x{height}")
    
    # ウィンドウサイズ変更を禁止（オプション）
    root.resizable(False, False)

    # GIF画像を読み込む
    try:
        gif = Image.open(gif_path)
    except Exception as e:
        print(f"GIF画像を開けません: {e}")
        sys.exit(1)

    # フレームを順次表示する関数
    def update_frame(frame_index, current_gif):
        try:
            current_gif.seek(frame_index)  # 指定したフレームに移動
            frame = current_gif.copy().resize((width, height), Image.Resampling.LANCZOS)  # フレームをリサイズ
            frame_tk = ImageTk.PhotoImage(frame)
            label.config(image=frame_tk)
            label.image = frame_tk  # 参照を保持する必要があります

            # 次のフレームを表示
            next_frame = (frame_index + 1) % current_gif.n_frames
            root.after(current_gif.info['duration'], update_frame, next_frame, current_gif)  # フレーム間隔を取得して設定
        except Exception as e:
            print(f"GIFフレームの更新中にエラーが発生しました: {e}")
            sys.exit(1)

    # 初期フレームを設定
    frame = gif.copy().resize((width, height), Image.Resampling.LANCZOS)
    frame_tk = ImageTk.PhotoImage(frame)
    label = tk.Label(root, image=frame_tk)
    label.image = frame_tk  # 参照を保持する必要があります
    label.pack()

    # アニメーションを開始
    update_frame(0, gif)

    return root, label, gif, update_frame  # update_frameを返す

def main():
    # スクリプトのディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # ロール設定をテキストファイルから読み込む
    try:
        role_path = os.path.join(script_dir, "role.txt")
        with open(role_path, "r", encoding="utf-8") as role_file:
            role_content = role_file.read().strip()  # ロール設定を読み込み
    except FileNotFoundError:
        print("エラー: role.txt ファイルが見つかりません。")
        exit(1)

    # GIF画像のパスを指定
    gif_path1 = os.path.join(script_dir, "image/torakichi_animation.gif")
    gif_path2 = os.path.join(script_dir, "image/torakichi_speaking.gif")

    # 表示するピクセル数を指定
    display_width = 1024
    display_height = 600

    if not os.path.exists(gif_path1) or not os.path.exists(gif_path2):
        print("GIF画像が存在しません。")
        sys.exit(1)

    # GIFアニメーションを表示するスレッドを開始
    root, label, gif1, update_frame = open_gif_image(gif_path1, display_width, display_height)
    
    # Geminiとの対話を別スレッドで実行
    def chat_gemini_interaction():
        nonlocal gif1
        try:
            # GIFを切り替え
            gif2 = Image.open(gif_path2)
            label.config(image=None)  # 現在の画像をクリア
            update_frame(0, gif2)  # GIF2の再生を開始

            text_to_speech("やあ！何か用があるにゃんか？")
            user_input = ""
            while user_input != "もういいや":
                try:
                    user_input = speech_to_text()  # 音声入力を取得
                    if user_input and user_input.strip():  # 空でない場合のみ処理
                        print(f"ユーザー入力: {user_input}")
                        if user_input != "もういいや":
                            reply = chat_with_gemini(role_content, user_input)
                            if reply:
                                text_to_speech(reply)  # Geminiの応答を音声で出力
                        else:
                            # 終了メッセージ
                            text_to_speech("またね！バイバイ！")
                            print("プログラムを終了します...")
                except Exception as e:
                    print(f"対話処理エラー: {e}")
                    text_to_speech("すみません、エラーが発生しました。もう一度お試しください。")

            # GIFを元に戻してウィンドウを閉じる
            label.config(image=None)  # 現在の画像をクリア
            update_frame(0, gif1)  # GIF1の再生を再開
            root.after(1000, root.destroy)  # 1秒後にウィンドウを閉じる
        except Exception as e:
            print(f"エラーが発生しました: {e}")

    # スレッドを作成して開始
    chat_thread = threading.Thread(target=chat_gemini_interaction)
    chat_thread.start()

    # Tkinterのメインループを開始
    root.mainloop()

    # メインループ終了後、スレッドを待機
    chat_thread.join()

if __name__ == "__main__":
    main()