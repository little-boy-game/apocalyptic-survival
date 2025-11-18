import pygame                                          # 导入 pygame 用于音频播放
import time                                            # 导入 time 用于睡眠等待
#导入多进程库
import multiprocessing                                 # 导入 multiprocessing 用于后台播放子进程

def _ogg_list_worker(file_list, stop_event):           # 子进程函数：循环播放文件列表，碰到停止事件退出
    """在子进程中循环播放文件列表，遇到 stop_event 则尽快退出."""  # 函数说明文档（保留供阅读）
    try:
        pygame.mixer.init()                            # 在子进程中初始化音频混音器，可能因环境失败而抛异常
    except Exception:
        pass                                          # 初始化失败时忽略错误（子进程继续以防止崩溃）
    idx = 0                                           # 当前播放索引初始化为 0
    length = len(file_list) if file_list else 0       # 计算文件列表长度，空列表长度为 0
    if length == 0:
        return                                       # 若无文件则直接返回，不进入播放循环
    while not stop_event.is_set():                    # 只要未收到停止事件，就继续循环播放列表
        file_path = file_list[idx % length]           # 取当前索引对应的文件（循环方式）
        try:
            pygame.mixer.music.load(file_path)        # 尝试加载指定路径的音乐文件
            pygame.mixer.music.play()                 # 开始播放（子进程中调用，不带 loops，按单曲播放）
            # 等待当前曲目播放结束或被停止
            while pygame.mixer.music.get_busy():     # 当播放器仍在播放时循环检查
                if stop_event.is_set():               # 如果收到停止事件，尝试停止播放并跳出等待
                    try:
                        pygame.mixer.music.stop()    # 停止当前播放
                    except Exception:
                        pass                          # 停止失败时忽略，继续退出循环以防卡死
                    break                            # 跳出等待循环，进入下一首或退出
                time.sleep(0.1)                      # 未被停止则短暂休眠，避免空循环占用 CPU
        except Exception:
            # 忽略单曲播放错误，继续下一个
            time.sleep(0.5)                          # 单曲播放失败时等待并继续下一个（容错）
        idx += 1                                      # 增加索引以播放下一首（或环回）

class go():                                           # 音乐控制类，封装播放/停止接口
    def __init__(self):                               # 构造函数，初始化 pygame.mixer 和后台进程引用
        # 初始化 pygame.mixer
        pygame.mixer.init()                           # 在主进程中初始化混音器（可能在某些环境抛异常）
        # 后台播放进程与停止事件引用
        self._bg_process = None                       # 保存后台播放子进程对象的引用，初始为 None
        self._stop_event = None                       # 保存用于通知子进程停止的 Event，初始为 None

    def play_ogg(self, file_path, loops=-1):          # 在主进程播放单个 OGG，支持 loops 参数（-1 为无限循环）
        try:
            # 加载 OGG 文件
            pygame.mixer.music.load(file_path)        # 加载指定文件到混音器
            # 播放音乐（loops=-1 表示循环播放，0 表示只播放一次）
            pygame.mixer.music.play(loops=loops)     # 开始播放并传入 loops 参数以控制循环行为
        except pygame.error as e:
            print(f"背景音乐播放失败: {e}")           # 打印 pygame 错误信息以便调试
            time.sleep(2)                             # 播放失败时稍作等待，避免信息闪过

    def play_ogg_list(self, file_list):               # 在子进程中按顺序循环播放一个文件列表（非阻塞）
        # 播放 OGG 文件列表，依次循环播放，并且不占用主进程
        if not file_list:
            return                                    # 若传入空列表则直接返回，不启动子进程
        # 停掉已有后台进程（如果存在）
        if self._bg_process and self._bg_process.is_alive():  # 如果已有后台进程正在运行
            try:
                self._stop_event.set()                 # 通知子进程停止播放
                self._bg_process.join(timeout=1)       # 等待子进程优雅退出，最多等待 1 秒
            except Exception:
                try:
                    self._bg_process.terminate()      # 若 join 失败则强制终止子进程
                except Exception:
                    pass                              # 忽略终止失败，继续执行
        # 创建新的停止事件与子进程
        self._stop_event = multiprocessing.Event()    # 创建一个新的事件，用于通知子进程停止
        self._bg_process = multiprocessing.Process(   # 创建子进程，目标为 _ogg_list_worker
            target=_ogg_list_worker,                  # 子进程执行的函数
            args=(file_list, self._stop_event),       # 传入文件列表与停止事件作为参数
            daemon=True                               # 设置为守护进程，主进程退出时子进程随之结束
        )
        self._bg_process.start()                      # 启动子进程（返回立即，不阻塞主进程）

    def stop_music(self):                             # 停止所有音乐并释放音频设备（供程序退出或切换时调用）
        # 手动停止并释放音频设备（在程序退出或切换音乐时调用）
        try:
            # 先通知后台进程停止
            if getattr(self, '_stop_event', None):    # 如果存在停止事件对象
                try:
                    self._stop_event.set()            # 设置事件，通知子进程尽快退出播放循环
                except Exception:
                    pass                              # 忽略设置事件的异常
            if getattr(self, '_bg_process', None) and self._bg_process.is_alive():  # 若后台进程存在且在运行
                try:
                    self._bg_process.join(timeout=1)  # 等待子进程结束，最多等待 1 秒
                except Exception:
                    try:
                        self._bg_process.terminate() # 无法优雅退出则强制终止子进程
                    except Exception:
                        pass                          # 忽略终止失败
            # 停止主进程的 mixer（若在主进程播放）
            pygame.mixer.music.stop()                 # 停止当前主进程中的播放（若有）
            pygame.mixer.quit()                       # 释放音频设备资源，退出 mixer
        except Exception:
            pass                                      # 忽略任何在停止过程中发生的异常，保证程序继续关闭

    def is_playing(self):                              # 返回当前是否正在播放（含主进程或后台子进程）
        # 返回当前是否正在播放（若后台进程存在则认为在播放）
        try:
            if getattr(self, '_bg_process', None) and self._bg_process.is_alive():  # 若后台进程活跃
                return True                            # 认为正在播放并返回 True
            return pygame.mixer.music.get_busy()       # 否则返回主进程 mixer 的播放状态
        except Exception:
            return False                               # 任何异常都视为未播放，返回 False
