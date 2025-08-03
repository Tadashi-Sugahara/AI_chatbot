# 起動時に指定したピクセル数でGIFアニメーションを表示するプログラム
import tkinter as tk
from PIL import Image, ImageTk
import sys
import os
import time

def open_gif_image(gif_path, width, height):
    # Tkinterウィンドウを作成
    root = tk.Tk()
    root.title("Robot Face GIF")

    # 全画面表示を有効化（必要に応じてコメント解除）
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
    def update_frame(frame_index):
        try:
            gif.seek(frame_index)  # 指定したフレームに移動
            frame = gif.copy().resize((width, height), Image.Resampling.LANCZOS)  # フレームをリサイズ
            frame_tk = ImageTk.PhotoImage(frame)
            label.config(image=frame_tk)
            label.image = frame_tk  # 参照を保持する必要があります

            # 次のフレームを表示
            next_frame = (frame_index + 1) % gif.n_frames
            root.after(gif.info['duration'], update_frame, next_frame)  # フレーム間隔を取得して設定
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
    update_frame(0)

    # ウィンドウを表示
    root.mainloop()

if __name__ == "__main__":
    # GIF画像のパスを指定
    gif_path1= "output/torakichi_animation.gif"

    # 表示するピクセル数を指定
    display_width = 1024
    display_height = 600

    if not os.path.exists(gif_path1):
        print(f"GIF画像が存在しません: {gif_path1}")
        sys.exit(1)

    open_gif_image(gif_path1, display_width, display_height)


# 起動時に指定したピクセル数でGIFアニメーションを表示するプログラム