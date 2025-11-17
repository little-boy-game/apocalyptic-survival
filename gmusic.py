import pygame
import time
#导入多进程库
import multiprocessing

def _ogg_list_worker(file_list, stop_event):
    """在子进程中循环播放文件列表，遇到 stop_event 则尽快退出."""
    try:
        pygame.mixer.init()
    except Exception:
        pass
    idx = 0
    length = len(file_list) if file_list else 0
    if length == 0:
        return
    while not stop_event.is_set():
        file_path = file_list[idx % length]
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            # 等待当前曲目播放结束或被停止
            while pygame.mixer.music.get_busy():
                if stop_event.is_set():
                    try:
                        pygame.mixer.music.stop()
                    except Exception:
                        pass
                    break
                time.sleep(0.1)
        except Exception:
            # 忽略单曲播放错误，继续下一个
            time.sleep(0.5)
        idx += 1

class go():
    def __init__(self):
        # 初始化 pygame.mixer
        pygame.mixer.init()
        # 后台播放进程与停止事件引用
        self._bg_process = None
        self._stop_event = None

    def play_ogg(self, file_path, loops=-1):
        try:
            # 加载 OGG 文件
            pygame.mixer.music.load(file_path)
            # 播放音乐（loops=-1 表示循环播放，0 表示只播放一次）
            pygame.mixer.music.play(loops=loops)
        except pygame.error as e:
            print(f"背景音乐播放失败: {e}")
            time.sleep(2)

    def play_ogg_list(self, file_list):
        # 播放 OGG 文件列表，依次循环播放，并且不占用主进程
        if not file_list:
            return
        # 停掉已有后台进程（如果存在）
        if self._bg_process and self._bg_process.is_alive():
            try:
                self._stop_event.set()
                self._bg_process.join(timeout=1)
            except Exception:
                try:
                    self._bg_process.terminate()
                except Exception:
                    pass
        # 创建新的停止事件与子进程
        self._stop_event = multiprocessing.Event()
        self._bg_process = multiprocessing.Process(
            target=_ogg_list_worker,
            args=(file_list, self._stop_event),
            daemon=True
        )
        self._bg_process.start()

    def stop_music(self):
        # 手动停止并释放音频设备（在程序退出或切换音乐时调用）
        try:
            # 先通知后台进程停止
            if getattr(self, '_stop_event', None):
                try:
                    self._stop_event.set()
                except Exception:
                    pass
            if getattr(self, '_bg_process', None) and self._bg_process.is_alive():
                try:
                    self._bg_process.join(timeout=1)
                except Exception:
                    try:
                        self._bg_process.terminate()
                    except Exception:
                        pass
            # 停止主进程的 mixer（若在主进程播放）
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except Exception:
            pass

    def is_playing(self):
        # 返回当前是否正在播放（若后台进程存在则认为在播放）
        try:
            if getattr(self, '_bg_process', None) and self._bg_process.is_alive():
                return True
            return pygame.mixer.music.get_busy()
        except Exception:
            return False
