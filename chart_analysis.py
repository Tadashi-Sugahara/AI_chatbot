# Chat GPT-5 APIを使用してチャート画像の分析を行うスクリプト
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image
import io

# .envファイルから環境変数を読み込み
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEYが.envファイルに設定されていません")

client = OpenAI(api_key=api_key)

def analyze_chart(image_path, analysis_prompt):
    try:
        # 画像を読み込み
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # ChatGPT APIを呼び出す
        response = client.chat.completions.create(
            model="gpt-5",  # GPT-5モデルを指定
            messages=[
                {"role": "user", "content": f"Here is the chart image data:\n{image_data}\nPlease analyze it and provide insights based on the following prompt:\n{analysis_prompt}"},
            ]
        )
        # 応答を取得
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        return f"エラーが発生しました: {e}"
