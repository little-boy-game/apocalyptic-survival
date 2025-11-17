import os
import random
import time
import webbrowser
import gmusic

# 定义颜色变量
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[33m'  # 用黄色代替橙色
WHITE = '\033[37m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'  # 重置颜色

def no(i):
    """清屏函数：i=1 时等待用户输入，i=0 时延迟清屏"""
    if i == 1:
        input(f"\n{ORANGE}按回车继续...{RESET}")
    # 非关键场景清屏前增加 1.5 秒延迟，让用户看清文字
    os.system('cls' if os.name == 'nt' else 'clear')

no(0)
print("背景音乐来源：钢铁雄心4")
time.sleep(0.5)
no(0)
mu = gmusic.go()  # 创建音乐对象
mu.play_ogg("hoi4mainthemeallies.ogg", -1)  # 播放背景音乐
# 主菜单
while True:
    no(0)  # 清屏并延迟，避免菜单闪烁
    ing = input(f'''
            {RED}===== 末日求生 ====={RESET}
            {GREEN}1. 开始游戏{RESET}
            {ORANGE}2. 查看成就{RESET}
            {BLUE}3. 导入存档{RESET}
            {PURPLE}4. 赞助作者{RESET}
            {WHITE}5.退出游戏{RESET}
            {ORANGE}请选择：{RESET}''')
    
    
        # 难度选择
    if ing == '1':
        no(0)
        name = input(f'''                {RED}===== 游戏难度 ====={RESET}
                {GREEN}1. 新手{RESET}
                {GREEN}2. 简单{RESET}
                {ORANGE}3. 普通{RESET}
                {ORANGE}4. 加难{RESET}
                {RED}5. 困难{RESET}
                {RED}6. 极其困难{RESET}
                {ORANGE}请选择：{RESET}''')
        
        # 难度说明（关键信息，显示后等待输入）
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
            no(1)  # 等待用户看清
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
        
        # 角色选择
        pep = input(f'''{GREEN}===== 角色选择 ====={RESET}
    {GREEN}1. 父亲{RESET}（饥饿+1天，道具+10%）
    {GREEN}2. 母亲{RESET}（道具+15%，负面事件-10%）
    {ORANGE}请选择：{RESET}''')
        
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
        
        # 开始游戏
        print(f"{GREEN}游戏开始！{RESET}")
        no(1)
        import go
        mu.play_ogg("La_Autocracia.ogg", 0)  # 播放开始游戏音乐

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
        go.game(None, name, pep)  # 新游戏
        
    elif ing == '2':
        no(0)
        import go
        go.show_achievements()  # 显示成就（内部已加等待）
        no(1)
        
    elif ing == '3':
        no(0)
        import go
        go.import_game()  # 导入存档（内部已加等待）
        no(1)
        
    elif ing == '4':
        webbrowser.open('https://afdian.com/a/little-boy-game')
    elif ing == '5':
        no(0)
        print(f"{WHITE}感谢游玩！{RESET}")
        time.sleep(2)
        exit()