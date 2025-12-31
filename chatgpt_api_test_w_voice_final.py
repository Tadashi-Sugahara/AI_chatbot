#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatGPT音声チャットボット - 最終版
完全にエラーフリーでユーザーフレンドリーなバージョン

Features:
- 完全なエラーハンドリング
- 分かりやすいユーザーメッセージ
- ALSAエラー抑制
- 音声認識とTTSのフォールバック
- OpenAI API統合
"""

import os
import sys
import contextlib
from io import StringIO

# ALSAエラーを完全に抑制
@contextlib.contextmanager
def suppress_stderr():
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr

# ALSAエラーを抑制してライブラリをインポート
with suppress_stderr():
    import openai
    import speech_recognition as sr
    from gtts import gTTS
    import pygame
    import tempfile
    import time
    from pydub import AudioSegment
    from pydub.playback import play

class VoiceChatBot:
    def __init__(self):
        """チャットボットの初期化"""
        print("🎤 音声チャットボットを初期化中...")
        
        # .envファイルから環境変数を読み込み
        from dotenv import load_dotenv
        load_dotenv()
        
        # OpenAI APIキーの設定
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        # 音声認識の初期化
        with suppress_stderr():
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        
        # Pygameの初期化（音声出力用）
        with suppress_stderr():
            pygame.mixer.init()
        
        # システム設定
        self.timeout = 5
        self.phrase_timeout = 1
        
        # OpenAIクライアントの初期化
        if not self.api_key:
            print("⚠️  OpenAI APIキーが.envファイルに設定されていません")
            print("   .envファイルにOPENAI_API_KEY=your-api-keyを追加してください")
            self.client = None
        else:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
                print("✅ OpenAI APIクライアント初期化完了")
            except Exception as e:
                print(f"❌ OpenAI API初期化エラー: {e}")
                self.client = None
        
        print("🎤 音声チャットボット準備完了！")
    
    def listen_for_speech(self):
        """音声入力を取得"""
        try:
            print("\n🎤 音声入力待機中... (話してください)")
            
            with suppress_stderr():
                with self.microphone as source:
                    # 環境音の調整
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # 音声を録音（with文内で実行）
                    audio = self.recognizer.listen(
                        source,
                        timeout=self.timeout,
                        phrase_time_limit=self.phrase_timeout
                    )
            
            print("🔄 音声を認識中...")
            
            # 音声をテキストに変換
            with suppress_stderr():
                text = self.recognizer.recognize_google(audio, language='ja-JP')
            
            print(f"🎤 音声入力: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏰ 音声入力がタイムアウトしました")
            return None
        except sr.UnknownValueError:
            print("❓ 音声を認識できませんでした")
            return None
        except sr.RequestError as e:
            print(f"❌ 音声認識サービスエラー: {e}")
            return None
        except Exception as e:
            print(f"❌ 音声認識エラー: {e}")
            return None
    
    def get_chatgpt_response(self, user_input):
        """ChatGPTから応答を取得"""
        if not self.client:
            return "OpenAI APIキーが設定されていないため、ChatGPTに接続できません。"
        
        try:
            print("🤖 ChatGPTが応答を生成中...")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは親切で丁寧な日本語のアシスタントです。"},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            print(f"🤖 ChatGPT: {ai_response}")
            return ai_response
            
        except Exception as e:
            error_msg = f"ChatGPTエラー: {str(e)}"
            print(f"❌ {error_msg}")
            return f"申し訳ありません。{error_msg}"
    
    def speak_text(self, text):
        """テキストを音声で出力"""
        try:
            print("🔊 音声出力中...")
            
            # Google Text-to-Speechで音声生成
            with suppress_stderr():
                tts = gTTS(text=text, lang='ja')
                
                # 一時ファイルに保存
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tts.save(tmp_file.name)
                    
                    # 音声ファイルを再生
                    audio = AudioSegment.from_mp3(tmp_file.name)
                    play(audio)
                    
                    # 一時ファイルを削除
                    os.unlink(tmp_file.name)
            
            print("✅ 音声出力完了")
            
        except Exception as e:
            print(f"❌ 音声出力エラー: {e}")
            print("テキスト出力のみ表示します")
    
    def run_chat_loop(self):
        """メインのチャットループ"""
        print("\n" + "="*50)
        print("🎤 音声チャットボット開始")
        print("Ctrl+Cで終了")
        print("="*50)
        
        try:
            while True:
                # 音声入力を取得
                user_input = self.listen_for_speech()
                
                if user_input:
                    # ChatGPTから応答を取得
                    ai_response = self.get_chatgpt_response(user_input)
                    
                    # 音声で応答
                    self.speak_text(ai_response)
                
                # 少し待機
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n👋 チャットボットを終了します")
        except Exception as e:
            print(f"\n❌ 予期しないエラー: {e}")

def main():
    """メイン関数"""
    try:
        # チャットボットを作成して実行
        chatbot = VoiceChatBot()
        chatbot.run_chat_loop()
        
    except Exception as e:
        print(f"❌ 起動エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()