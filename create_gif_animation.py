# 2枚の画像ファイルからGIFアニメーションを作成するスクリプト
from PIL import Image
import os
def create_gif_animation(image_paths, output_path, duration=1000):
    """
    2枚の画像からGIFアニメーションを作成します。

    :param image_paths: 画像ファイルのパスのリスト
    :param output_path: 出力するGIFファイルのパス
    :param duration: 各フレームの表示時間（ミリ秒）
    """
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


if __name__ == "__main__":
    # 画像パスのリストを指定
    image_paths = [
        "image/torakichi_normal.png",
        "image/torakichi_openmouth.png"
    ]
    
    # 出力GIFファイルのパス
    output_path = "output/torakichi_speaking.gif"

    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    create_gif_animation(image_paths, output_path)