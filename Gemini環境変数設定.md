# 🤖 Gemini APIキーの.env環境変数設定ガイド

## ✅ 設定手順

### 1. Google AI Studio でAPIキーを取得
1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
2. Googleアカウントでログイン
3. "Create API Key" をクリック
4. APIキーをコピーして保存

### 2. .envファイルの設定
プロジェクトルートの `.env` ファイルに以下を追加：

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. 必要なパッケージのインストール
```bash
# 仮想環境の有効化
& D:\Python\AI_chatbot\venv\Scripts\Activate.ps1

# 必要なパッケージのインストール
pip install google-genai
pip install -r requirement.txt
```

### 4. 修正されたファイル
- `ai_robot_w_face_gemini.py` - GeminiのAPI を使用するバージョン（新しいgoogle.genaiパッケージ対応）
- `requirement.txt` - 依存関係にgoogle-genaiを追加

## 🚀 使用方法

### Gemini版の実行
```bash
cd D:\Python\AI_chatbot
& D:\Python\AI_chatbot\venv\Scripts\Activate.ps1
python ai_robot_w_face_gemini.py
```

## ⚠️ 注意事項

1. **APIキーは秘密情報です**
   - .envファイルをGitにコミットしないでください
   - 他人と共有しないでください

2. **利用制限について**
   - Gemini APIには使用制限があります
   - 詳細は [Google AI の利用規約](https://ai.google.dev/terms) を確認してください

3. **エラー対処**
   - APIキーが正しく設定されているか確認
   - インターネット接続を確認
   - Google AI APIの利用可能状況を確認

## 📝 ChatGPTからGeminiへの主な変更点

1. **APIライブラリの変更**
   - `openai` → `google-genai` （最新版）

2. **環境変数名の変更**
   - `OPENAI_API_KEY` → `GOOGLE_API_KEY`

3. **APIの呼び出し方法の変更**
   - OpenAIのChat Completion → GeminiのGenerative Content（新API）

4. **モデル名**
   - `gpt-3.5-turbo` → `gemini-1.5-flash`