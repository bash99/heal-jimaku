"""
音频处理 Qt Worker 类

将 audio_processor 包装为 QThread，提供 Qt 信号支持。
仅用于 GUI，CLI 工具不需要此模块。

作者: fuxiaomoke
版本: 0.2.2.0
"""

from PyQt6.QtCore import QThread, pyqtSignal
from core.audio_extractor import extract_audio_to_ogg, split_audio_by_duration
import tempfile


class AudioExtractionWorker(QThread):
    """视频音频提取后台工作线程"""
    
    finished = pyqtSignal(str, str)  # (output_path, message)
    error = pyqtSignal(str)          # error_message
    progress = pyqtSignal(float)     # 0-100
    
    def __init__(self, input_path: str):
        super().__init__()
        self.input_path = input_path
        self.output_path = None
    
    def run(self):
        """执行音频提取"""
        try:
            import time
            start_time = time.time()
            print(f"[音频提取] 开始处理文件: {self.input_path}")
            
            def progress_callback(current, total):
                if total > 0:
                    percent = (current / total) * 100
                    self.progress.emit(percent)
            
            success, message, output_path = extract_audio_to_ogg(
                self.input_path,
                progress_callback=progress_callback
            )
            
            if success:
                self.output_path = output_path
                processing_time = time.time() - start_time
                print(f"[音频提取] 完成，耗时: {processing_time:.2f}秒，输出: {output_path}")
                self.finished.emit(output_path, message)
            else:
                self.error.emit(message)
        
        except Exception as e:
            self.error.emit(f"音频提取过程出错: {str(e)}")


class AudioSplittingWorker(QThread):
    """音频分割后台工作线程"""
    
    finished = pyqtSignal(str, list)  # (audio_path, chunk_info)
    error = pyqtSignal(str, str)      # (audio_path, error_message)
    progress = pyqtSignal(str)        # progress_message
    
    def __init__(self, audio_path: str, duration: float, max_duration: float):
        super().__init__()
        self.audio_path = audio_path
        self.duration = duration
        self.max_duration = max_duration
    
    def run(self):
        """执行音频分割"""
        try:
            output_dir = tempfile.gettempdir()
            
            def progress_callback(curr_chunk, total_chunks, msg):
                self.progress.emit(msg)
            
            success, message, chunk_info = split_audio_by_duration(
                self.audio_path,
                max_duration=self.max_duration,
                output_dir=output_dir,
                progress_callback=progress_callback
            )
            
            if success and chunk_info:
                self.finished.emit(self.audio_path, chunk_info)
            else:
                self.error.emit(self.audio_path, message)
        
        except Exception as e:
            import traceback
            error_msg = f"音频分割异常: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.error.emit(self.audio_path, error_msg)
