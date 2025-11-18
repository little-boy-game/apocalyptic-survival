import os                           # 导入 os，用于执行系统命令（如清屏）
import random                       # 导入 random，用于随机事件与概率判定
import time                         # 导入 time，用于延时与模拟等待
import webbrowser                   # 导入 webbrowser，用于打开赞助页面链接
import gmusic                       # 导入自定义音乐模块，用于播放背景音乐

# 定义颜色变量，控制终端输出颜色（ANSI 转义序列）
RED = '\033[31m'                     # 红色文本
GREEN = '\033[32m'                   # 绿色文本
ORANGE = '\033[33m'                  # 橙色/黄色文本（用黄色表示）
WHITE = '\033[37m'                   # 白色文本
BLUE = '\033[34m'                    # 蓝色文本
PURPLE = '\033[35m'                  # 紫色文本
CYAN = '\033[36m'                    # 青色文本
RESET = '\033[0m'                    # 重置颜色到默认

def no(i):                            # 清屏与等待函数，参数 i 控制行为
    """清屏函数：i=1 时等待用户回车，i=0 仅清屏（用于不阻塞场景）"""  # 函数说明
    if i == 1:                        # 当需要等待时
        input(f"\n{ORANGE}按回车继续...{RESET}")  # 提示并等待用户回车
    # 非关键场景清屏前增加短延迟，防止文字闪烁（保持界面可读性）
    os.system('cls' if os.name == 'nt' else 'clear')  # Windows 用 cls，其他系统用 clear

no(0)                                 # 启动时短暂清屏，不等待
print("背景音乐来源：钢铁雄心4")         # 打印版权/来源提示
time.sleep(0.5)                       # 暂停 0.5 秒，给玩家时间查看提示
no(0)                                 # 再次清屏准备主菜单显示
mu = gmusic.go()                      # 创建音乐控制对象（gmusic.go 类实例）
mu.play_ogg("hoi4mainthemeallies.ogg", -1)  # 播放主菜单背景音乐（循环）

# 主菜单循环，直到玩家选择退出
while True:
    no(0)                             # 每次显示菜单前清屏以保持界面整洁
    ing = input(f'''
            {RED}===== 末日求生 ====={RESET}
            {GREEN}1. 开始游戏{RESET}
            {ORANGE}2. 查看成就{RESET}
            {BLUE}3. 导入存档{RESET}
            {PURPLE}4. 赞助作者{RESET}
            {WHITE}5.退出游戏{RESET}
            {ORANGE}请选择：{RESET}''')  # 显示菜单并读取玩家选择
    
    # 玩家选择开始游戏时进入难度与角色选择流程
    if ing == '1':
        no(0)                         # 清屏显示难度选择界面
        name = input(f'''                {RED}===== 游戏难度 ====={RESET}
                {GREEN}1. 新手{RESET}
                {GREEN}2. 简单{RESET}
                {ORANGE}3. 普通{RESET}
                {ORANGE}4. 加难{RESET}
                {RED}5. 困难{RESET}
                {RED}6. 极其困难{RESET}
                {ORANGE}请选择：{RESET}''')  # 读取难度选择

        # 根据选择展示难度说明并等待用户确认
        if name == '1':
            no(0)
            print(f'''{GREEN}新手难度{RESET}
效果：
    1.每个道具获得的几率{GREEN}+50%{RESET}
    2.饥饿保持天数{GREEN}+2天（5天）{RESET}
    3.口渴保持天数{GREEN}+3天（5天）{RESET}
    4.负面事件发生几率{GREEN}-50%{RESET}
    5.正面事件发生几率{GREEN}+50%{RESET}
    6.生病（除事件产生）发生几率{GREEN}-25%（0%）{RESET}
    7.{RED}无法获得成就{RESET}''')
            no(1)                    # 等待玩家确认后继续
        elif name == '2':
            no(0)
            print(f'''{GREEN}简单难度{RESET}
效果：
    1.每个道具获得的几率{GREEN}+20%{RESET}
    2.饥饿保持天数{GREEN}+1天（4天）{RESET}
    3.口渴保持天数{GREEN}+2天（4天）{RESET}
    4.负面事件发生几率{GREEN}-25%{RESET}
    5.正面事件发生几率{GREEN}+25%{RESET}
    6.生病（除事件产生）发生几率{GREEN}-20%{RESET}
    7.{RED}只能获得部分成就{RESET}''')
            no(1)
        elif name == '3':
            no(0)
            print(f'''{GREEN}普通难度{RESET}
效果：
    1.每个道具获得的几率{GREEN}正常{RESET}
    2.饥饿保持天数{GREEN}3天{RESET}
    3.口渴保持天数{GREEN}2天{RESET}
    4.负面事件发生几率{GREEN}正常{RESET}
    5.正面事件发生几率{GREEN}正常{RESET}
    6.生病（除事件产生）发生几率{GREEN}25%{RESET}
    7.{GREEN}可获得全部成就{RESET}''')
            no(1)
        elif name == '4':
            no(0)
            print(f'''{ORANGE}加难难度{RESET}
效果：
    1.每个道具获得的几率{RED}-25%{RESET}
    2.饥饿保持天数{RED}-1天（2天）{RESET}
    3.口渴保持天数{RED}-1天（1天）{RESET}
    4.负面事件发生几率{RED}+25%{RESET}
    5.正面事件发生几率{RED}-25%{RESET}
    6.生病（除事件产生）发生几率{RED}+25%{RESET}''')
            no(1)
        elif name == '5':
            no(0)
            print(f'''{RED}困难难度{RESET}
效果：
    1.每个道具获得的几率{RED}-40%{RESET}
    2.饥饿保持天数{RED}-2天（1天）{RESET}
    3.口渴保持天数{RED}-2天（0天）{RESET}
    4.负面事件发生几率{RED}+40%{RESET}
    5.正面事件发生几率{RED}-40%{RESET}
    6.生病（除事件产生）发生几率{RED}+30%{RESET}''')
            no(1)
        elif name == '6':
            no(0)
            print(f'''{RED}极其困难难度{RESET}
效果：
    1.每个道具获得的几率{RED}-50%(0%){RESET}
    2.饥饿保持天数{RED}-3天（0天）{RESET}
    3.口渴保持天数{RED}-2天（0天）{RESET}
    4.负面事件发生几率{RED}+50%{RESET}
    5.正面事件发生几率{RED}-50%{RESET}
    6.生病（除事件产生）发生几率{RED}+70%{RESET}''')
            no(1)

        # 角色选择界面，父亲或母亲，显示效果后开始游戏
        pep = input(f'''{GREEN}===== 角色选择 ====={RESET}
    {GREEN}1. 父亲{RESET}（饥饿+1天，道具+10%）
    {GREEN}2. 母亲{RESET}（道具+15%，负面事件-10%）
    {ORANGE}请选择：{RESET}''')  # 读取角色选择

        if pep == '1':
            no(0)
            print(f'''{GREEN}父亲{RESET}
效果：
    1.饥饿保持天数{GREEN}+1天{RESET}
    2.每个道具获得的几率{GREEN}+10%{RESET}''')
            no(1)
        elif pep == '2':
            no(0)
            print(f'''{GREEN}母亲{RESET}
效果：  
    1.每个道具获得的几率{GREEN}+15%{RESET}
    2.负面事件发生几率{GREEN}-10%{RESET}''')
            no(1)

        # 开始游戏前的界面提示与音乐切换
        print(f"{GREEN}游戏开始！{RESET}")  # 提示游戏即将开始
        no(1)                         # 等待玩家确认开始
        import go                      # 延迟导入 go 模块以避免循环导入问题
        mu.play_ogg("La_Autocracia.ogg", 0)  # 播放开场音乐（只播放一次）

        # 简短序章文本，逐步展示并等待玩家阅读
        print('从前...')
        no(1)
        print('在一个风和日丽的早晨...')
        no(1)
        print('一家三口正在享受着天伦之乐...')
        no(1)
        print('突然，天空中传来一声巨响...')
        no(1)
        print('一颗巨大的陨石正朝着地球飞来...')
        no(1)
        print('末日就此降临...')
        no(1)
        go.game(None, name, pep)       # 调用游戏主循环并传入难度与角色参数

    elif ing == '2':                   # 查看成就分支
        no(0)
        import go                       # 动态导入 go 模块以调用成就显示
        go.show_achievements()          # 显示成就界面（内部包含等待）
        no(1)

    elif ing == '3':                   # 导入存档分支
        no(0)
        import go                       # 导入 go 以调用导入功能
        go.import_game()                # 打开文件对话框并导入存档（内部会启动游戏）
        no(1)

    elif ing == '4':                   # 打开赞助链接分支
        webbrowser.open('https://afdian.com/a/little-boy-game')  # 在默认浏览器打开赞助页面

    elif ing == '5':                   # 退出游戏分支
        no(0)
        print(f"{WHITE}感谢游玩！{RESET}")  # 致谢信息
        time.sleep(2)                   # 暂停 2 秒后退出，给玩家时间看到提示
        exit()                          # 退出程序