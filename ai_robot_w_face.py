# GIFアニメーションを表示しながらChatGPTと対話するためのプログラムです。
import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import openai
from audio2text import speech_to_text
from text2audio import text_to_speech
from threading import Thread
import threading

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

def open_gif_image(gif_path, width, height):
    # Tkinterウィンドウを作成
    root = tk.Tk()
    root.title("Robot Face GIF")

    # 全画面表示を有効にする
    root.attributes('-fullscreen', True)

    # Escapeキーで全画面解除
    root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))

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
    # ロール設定をテキストファイルから読み込む
    try:
        with open("role.txt", "r", encoding="utf-8") as role_file:
            role_content = role_file.read().strip()  # ロール設定を読み込み
    except FileNotFoundError:
        print("エラー: role.txt ファイルが見つかりません。")
        exit(1)

    # GIF画像のパスを指定
    gif_path1 = "output/torakichi_animation.gif"
    gif_path2 = "output/torakichi_speaking.gif"

    # 表示するピクセル数を指定
    display_width = 1024
    display_height = 600

    if not os.path.exists(gif_path1) or not os.path.exists(gif_path2):
        print("GIF画像が存在しません。")
        sys.exit(1)

    # GIFアニメーションを表示するスレッドを開始
    root, label, gif1, update_frame = open_gif_image(gif_path1, display_width, display_height)

    # ChatGPTとの対話を別スレッドで実行
    def chat_gpt_interaction():
        nonlocal gif1
        try:
            # GIFを切り替え
            gif2 = Image.open(gif_path2)
            label.config(image=None)  # 現在の画像をクリア
            update_frame(0, gif2)  # GIF2の再生を開始

            text_to_speech("やあ！何か用があるにゃんか？")
            user_input = ""
            while user_input != "もういいや":
                user_input = speech_to_text()  # 音声入力を取得
                reply = chat_with_gpt(role_content, user_input)
                text_to_speech(reply)  # ChatGPTの応答を音声で出力

            # GIFを元に戻す
            label.config(image=None)  # 現在の画像をクリア
            update_frame(0, gif1)  # GIF1の再生を再開
        except Exception as e:
            print(f"エラーが発生しました: {e}")

    # スレッドを作成して開始
    chat_thread = threading.Thread(target=chat_gpt_interaction)
    chat_thread.start()

    # Tkinterのメインループを開始
    root.mainloop()

    # メインループ終了後、スレッドを待機
    chat_thread.join()

if __name__ == "__main__":
    main()