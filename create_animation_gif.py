# torakichi_animation.gifを作成
from PIL import Image
import os

def create_gif_animation(image_paths, output_path, duration=1000):
    images = []
    
    for image_path in image_paths:
        try:
            img = Image.open(image_path)
            images.append(img)
        except Exception as e:
            print(f"画像を開けません: {e}")
            return

    if len(images) < 2:
        print("少なくとも2枚の画像が必要です")
        return

    # GIFアニメーションを保存
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=duration, loop=0)
    print(f"GIFアニメーションを作成しました: {output_path}")

# normalとwinkの組み合わせでアニメーションGIFを作成
image_paths = [
    "image/torakichi_normal.png",
    "image/torakichi_wink.png"
]

output_path = "output/torakichi_animation.gif"

# 出力ディレクトリが存在しない場合は作成
os.makedirs(os.path.dirname(output_path), exist_ok=True)

create_gif_animation(image_paths, output_path, duration=800)