import tkinter as tk
from PIL import Image, ImageTk
import sys

def open_images(image_paths):
    # Tkinterウィンドウを作成
    root = tk.Tk()
    root.title("Robot Face")

    # 全画面表示を有効化
    root.attributes('-fullscreen', True)

    # 画像リストのインデックスを管理
    current_index = [0]

    # 画像を切り替える関数
    def update_image():
        try:
            img = Image.open(image_paths[current_index[0]])
            img_tk = ImageTk.PhotoImage(img)
            label.config(image=img_tk)
            label.image = img_tk  # 参照を保持する必要があります
            current_index[0] = (current_index[0] + 1) % len(image_paths)
            root.after(2000, update_image)  # 2秒後に再度実行
        except Exception as e:
            print(f"画像を開けません: {e}")
            sys.exit(1)

    # 初期画像を設定
    img = Image.open(image_paths[0])
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=img_tk)
    label.image = img_tk  # 参照を保持する必要があります
    label.pack()

    # 画像切り替えを開始
    root.after(2000, update_image)

    # ウィンドウを表示
    root.mainloop()

if __name__ == "__main__":
    # 画像パスのリストを指定
    image_paths = [
        "image/torakichi_normal.png",
        "image/torakichi_wink.png"
    ]

    if not image_paths:
        print("画像パスが指定されていません")
        sys.exit(1)

    open_images(image_paths)