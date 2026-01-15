"""
ALSA エラーを回避する音声出力モジュール
"""
import os
import sys

def text_to_speech_dummy(text):
    """ダミー音声出力関数 - テスト用"""
    print(f"[音声出力]: {text}")
    return True

def text_to_speech_safe(text):
    """安全な音声出力 - エラー時はFalseを返す"""
    temp_file = None
    try:
        from gtts import gTTS
        from pydub import AudioSegment
        from pydub.playback import play
        import re
        
        # テキストを言語ごとに分割
        segments = re.findall(r'[^\x00-\x7F]+|[\x00-\x7F]+', text)
        
        # 各セグメントを音声に変換して再生
        for segment in segments:
            if segment.strip():  # 空のセグメントを無視
                lang = 'ja' if re.search(r'[^\x00-\x7F]', segment) else 'en'
                
                # 音声ファイル作成
                tts = gTTS(text=segment, lang=lang)
                temp_file = f"temp_audio_{hash(segment)}.mp3"
                tts.save(temp_file)
                
                try:
                    # 音声再生
                    segment_audio = AudioSegment.from_mp3(temp_file)
                    
                    # 再生速度調整
                    if lang == 'ja':
                        speed_factor = 1.3
                    else:
                        speed_factor = 1.0
                        
                    new_frame_rate = int(segment_audio.frame_rate * speed_factor)
                    faster_audio = segment_audio._spawn(
                        segment_audio.raw_data, 
                        overrides={'frame_rate': new_frame_rate}
                    )
                    faster_audio = faster_audio.set_frame_rate(segment_audio.frame_rate)
                    
                    # エラー出力を一時的に抑制
                    original_stderr = sys.stderr
                    try:
                        sys.stderr = open(os.devnull, 'w')
                        play(faster_audio)
                    finally:
                        sys.stderr.close()
                        sys.stderr = original_stderr
                finally:
                    # 一時ファイル削除（確実に実行）
                    if temp_file and os.path.exists(temp_file):
                        try:
                            os.remove(temp_file)
                        except Exception as e:
                            print(f"[ファイル削除エラー]: {temp_file} - {e}")
                    temp_file = None
                    
        return True
        
    except Exception as e:
        print(f"[音声出力エラー]: {str(e)[:50]}...")
        # エラー時も一時ファイルを削除
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        return False

# 音声出力の実装を選択
text_to_speech = text_to_speech_safe  # 実際の音声合成を使用
# text_to_speech = text_to_speech_dummy  # デモ用ダミー関数を使用