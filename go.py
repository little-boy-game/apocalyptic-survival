import os
import random
import time
import pickle  # 替换json，用于二进制存储
import tkinter as tk
from tkinter import filedialog
import gmusic

root = tk.Tk()
root.withdraw()  # 隐藏tkinter主窗口

# 定义颜色变量
RED = '\033[31m'
GREEN = '\033[32m'
ORANGE = '\033[33m'
WHITE = '\033[37m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'

# -------------------------- 成就系统（二进制存储）--------------------------
# 初始化成就模板
DEFAULT_ACHIEVEMENTS = {
    "生存达人": {"desc": "生存100天", "unlocked": False},
    "顽强求生": {"desc": "生存200天", "unlocked": False},
    "猫咪守护者": {"desc": "获得猫咪道具", "unlocked": False},
    "技术专家": {"desc": "获得电脑道具", "unlocked": False},
    "物资大亨": {"desc": "拥有100个罐头", "unlocked": False},
    "水资源管理者": {"desc": "拥有100个水瓶", "unlocked": False},
    "医疗兵": {"desc": "拥有10个急救包", "unlocked": False},
    "幸运儿": {"desc": "连续5天触发正面事件", "unlocked": False},
    "收藏家": {"desc": "获得所有类型的道具", "unlocked": False},
    "困难征服者": {"desc": "在困难难度下生存50天", "unlocked": False},
    "极限生存者": {"desc": "在极其困难难度下生存30天", "unlocked": False},
    "军方信任者": {"desc": "获得军方结局", "unlocked": False},
    "寒冬勇士": {"desc": "获得极寒结局", "unlocked": False},
    "数字救援": {"desc": "通过电脑获得救援", "unlocked": False},
    "突围者": {"desc": "成功冲出封锁区", "unlocked": False},
    "天命之子": {"desc": "解锁神仙降临结局", "unlocked": False},
    "猫咪伙伴": {"desc": "获得猫咪结局", "unlocked": False}
}
ACHIEVEMENT_FILE = "achievements.cjt"  # 自定义后缀，二进制存储

def save_achievements(achievements):
    """保存成就到二进制文件（无法直接修改）"""
    try:
        with open(ACHIEVEMENT_FILE, "wb") as f:
            # 使用最高协议序列化，加密性更强
            pickle.dump(achievements, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print(f"{RED}成就保存失败：{str(e)}{RESET}")
        no(1)

def load_achievements():
    """加载成就（文件不存在则初始化）"""
    if os.path.exists(ACHIEVEMENT_FILE):
        try:
            with open(ACHIEVEMENT_FILE, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"{RED}成就文件损坏，使用默认成就！{RESET}")
            no(1)
            return DEFAULT_ACHIEVEMENTS.copy()
    else:
        # 首次运行，初始化成就并保存
        init_achievements = DEFAULT_ACHIEVEMENTS.copy()
        save_achievements(init_achievements)
        return init_achievements

def show_achievements():
    """显示成就列表（关键信息，等待用户输入）"""
    achievements = load_achievements()
    print(f"{PURPLE}===== 成就列表 ====={RESET}\n")
    unlocked_count = 0
    for name, data in achievements.items():
        status = f"{GREEN}【已解锁】{RESET}" if data["unlocked"] else f"{RED}【未解锁】{RESET}"
        print(f"{name}：{data['desc']} {status}")
        if data["unlocked"]:
            unlocked_count += 1
    print(f"\n{BLUE}已解锁 {unlocked_count}/{len(achievements)} 个成就{RESET}")

def check_achievement(achievements, name):
    """检查并解锁成就（显示后等待用户确认）"""
    if not achievements[name]["unlocked"]:
        achievements[name]["unlocked"] = True
        save_achievements(achievements)
        print(f"\n{CYAN}===== 成就解锁！====={RESET}")
        print(f"{CYAN}成就名称：{name}{RESET}")
        print(f"{CYAN}成就描述：{achievements[name]['desc']}{RESET}")
        no(1)  # 强制等待，确保用户看清
    return achievements

# -------------------------- 存档系统 --------------------------
def save_game(data):
    """保存游戏进度（json格式，方便导入）"""
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("存档文件", "*.json"), ("所有文件", "*.*")],
            title="保存游戏"
        )
        if file_path:
            # 用json保存进度（pickle用于成就加密，进度无需加密）
            import json
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"{GREEN}存档成功：{file_path}{RESET}")
    except Exception as e:
        print(f"{RED}存档失败：{str(e)}{RESET}")
    no(1)

def import_game():
    """导入游戏进度"""
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("存档文件", "*.json"), ("所有文件", "*.*")],
            title="导入游戏"
        )
        if file_path:
            import json
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"{GREEN}导入成功！正在加载...{RESET}")
            time.sleep(2)
            game(data, None, None)  # 加载存档
    except Exception as e:
        print(f"{RED}导入失败：{str(e)}{RESET}")
    no(1)

# -------------------------- 游戏核心逻辑 --------------------------
def no(i):
    """清屏函数（与main.py保持一致）"""
    if i == 1:
        input(f"\n{ORANGE}按回车继续...{RESET}")
    os.system('cls' if os.name == 'nt' else 'clear')

def game(saved_data, name, pep):
    """游戏主循环"""

    mu = gmusic.go()  # 重新创建音乐对象
    mu.play_ogg("general_war_theattack.ogg", -1)  # 播放开场音乐
    # 加载成就（全局共享）
    achievements = load_achievements()
    
    # -------------------------- 初始化游戏参数 --------------------------
    xg = {'道具获得几率':50, '饥饿保持天数':3, '口渴保持天数':2, 
          '负面事件发生几率':50, '正面事件发生几率':50, '生病发生几率':25}
    
    # 事件列表（新增猫咪、电脑、物资箱事件）
    events_positive = [
        '发现食物', '找到干净的水源', '遇到友善的幸存者', '找到医疗包',
        '发现道具', '外面有动静', '天气转好', '发现补给箱', '遇到救援队伍',
        '发现物资箱', '发现猫咪', '发现电脑'
    ]
    events_negative = [
        '遭遇野兽攻击', '食物中毒', '遇到敌对幸存者', '受伤感染',
        '道具损坏', '恶劣天气来袭', '迷路了', '水源被污染', '军方来到',
        '建筑物倒塌', '极端寒冷'
    ]
    
    # 事件描述（关键信息，详细说明）
    events_Speech = {
        '发现食物':'你在废墟中找到半块面包，饥饿值恢复1点。',
        '找到干净的水源':'发现一处未污染的小溪，口渴值恢复1点。',
        '遇到友善的幸存者':'他分给你1个罐头，感谢你的帮助。',
        '找到医疗包':'在废弃医院找到1个急救包，健康值+2。',
        '发现道具':'随机获得1件常用道具（绷带/火柴等）。',
        '外面有动静':'远处传来奇怪的声音，可能是危险也可能是机会。',
        '天气转好':'阳光明媚，正面事件概率+5%。',
        '发现补给箱':'获得罐头+2、水瓶+2。',
        '遇到救援队伍':'获得罐头+1、水瓶+1。',
        '发现物资箱':'打开后随机获得2件道具！',
        '发现猫咪':'一只流浪猫信任你，跟着你回到营地（触发猫咪结局必备）。',
        '发现电脑':'找到一台能工作的笔记本电脑（触发电子救援结局必备）。',
        '遭遇野兽攻击':'被野狗咬伤，健康值-2，获得【受伤】状态。',
        '食物中毒':'吃了变质食物，健康值-1，获得【生病】状态。',
        '遇到敌对幸存者':'被抢走1个罐头和1个水瓶。',
        '受伤感染':'伤口发炎，健康值-2，同时获得【生病】和【受伤】状态。',
        '道具损坏':'随机1件道具（非关键）损坏消失。',
        '恶劣天气来袭':'暴雨导致负面事件概率+5%。',
        '迷路了':'浪费1天时间，饥饿值-0.5，正面事件概率-5%。',
        '水源被污染':'找到的水不能喝，口渴值-0.5。',
        '军方来到':'军方搜查后留下3个罐头和3个水瓶（触发军方结局必备）。',
        '建筑物倒塌':'躲避不及被砸伤，健康值-3，获得【受伤】状态。',
        '极端寒冷':'体温下降，健康值-1，饥饿值-1，口渴值-1。'
    }
    
    # 道具列表（新增猫咪、电脑、物资箱）
    items = {
        '罐头': {'获得几率':70, '获得数量':2, '拥有数量':4},
        '水瓶': {'获得几率':70, '获得数量':2, '拥有数量':3},
        '绷带': {'获得几率':50, '获得数量':1, '拥有数量':0},
        '急救包': {'获得几率':30, '获得数量':1, '拥有数量':0},
        '手电筒': {'获得几率':15, '获得数量':1, '拥有数量':0},
        '电池': {'获得几率':50, '获得数量':2, '拥有数量':0},
        '刀具': {'获得几率':30, '获得数量':1, '拥有数量':0},
        '绳子': {'获得几率':30, '获得数量':1, '拥有数量':0},
        '火柴盒': {'获得几率':40, '获得数量':3, '拥有数量':0},
        '帐篷': {'获得几率':20, '获得数量':1, '拥有数量':0},
        '猫咪': {'获得几率':1, '获得数量':1, '拥有数量':0},  # 极其稀有
        '电脑': {'获得几率':5, '获得数量':1, '拥有数量':0},   # 稀有
        '物资箱': {'获得几率':10, '获得数量':1, '拥有数量':0} # 中等稀有
    }
    
    # 从存档加载数据
    if saved_data:
        day = saved_data["day"]
        hunger = saved_data["hunger"]
        thirst = saved_data["thirst"]
        health = saved_data["health"]
        status = saved_data["status"]
        xg = saved_data["xg"]
        items = saved_data["items"]
        name = saved_data["difficulty"]
        pep = saved_data["character"]
        military_visited = saved_data["military_visited"]
        consecutive_positive = saved_data["consecutive_positive"]
        has_asked_survival_end = saved_data["has_asked_survival_end"]
    else:
        # 根据难度调整参数
        if name == '1':  # 新手
            xg['道具获得几率'] += 50; xg['饥饿保持天数'] += 2; xg['口渴保持天数'] += 3
            xg['负面事件发生几率'] -= 50; xg['正面事件发生几率'] += 50; xg['生病发生几率'] -= 25
        elif name == '2':  # 简单
            xg['道具获得几率'] += 20; xg['饥饿保持天数'] += 1; xg['口渴保持天数'] += 2
            xg['负面事件发生几率'] -= 25; xg['正面事件发生几率'] += 25; xg['生病发生几率'] -= 20
        elif name == '4':  # 加难
            xg['道具获得几率'] -= 25; xg['饥饿保持天数'] -= 1; xg['口渴保持天数'] -= 1
            xg['负面事件发生几率'] += 25; xg['正面事件发生几率'] -= 25; xg['生病发生几率'] += 25
        elif name == '5':  # 困难
            xg['道具获得几率'] -= 40; xg['饥饿保持天数'] -= 2; xg['口渴保持天数'] -= 2
            xg['负面事件发生几率'] += 40; xg['正面事件发生几率'] -= 40; xg['生病发生几率'] += 30
        elif name == '6':  # 极其困难
            xg['道具获得几率'] -= 50; xg['饥饿保持天数'] -= 3; xg['口渴保持天数'] -= 2
            xg['负面事件发生几率'] += 50; xg['正面事件发生几率'] -= 50; xg['生病发生几率'] += 70
        
        # 根据角色调整参数
        if pep == '1':  # 父亲
            xg['道具获得几率'] += 10; xg['饥饿保持天数'] += 1
        elif pep == '2':  # 母亲
            xg['道具获得几率'] += 15; xg['负面事件发生几率'] -= 10
        
        # 初始状态
        day = 1; hunger = 6; thirst = 6; health = 10
        status = {"生病": False, "受伤": False,"极度饥饿": False, "极度口渴": False}
        military_visited = False; consecutive_positive = 0
        has_asked_survival_end = False  # 标记是否已询问200天结局
    
    # -------------------------- 游戏主循环 --------------------------
    while True:
        # 检查季节（每30天一个季节，冬季触发极寒结局）
        season = (day // 30) % 4
        winter = season == 3  # 第3个季节为冬季（90-120天、120-150天等）
        # 显示状态效果
        status_text = []
        if status["生病"]: status_text.append(f"{RED}【生病】健康-0.5/天{RESET}")
        if status["受伤"]: status_text.append(f"{RED}【受伤】健康-0.3/天{RESET}")
        if winter: status_text.append(f"{BLUE}【冬季】极寒风险↑{RESET}")
        print(f"状态: {' | '.join(status_text) if status_text else '【正常】'}\n")
        
        # 显示道具
        print(f"{GREEN}当前道具:{RESET}")
        item_display = []
        for item_name, item_data in items.items():
            if item_data["拥有数量"] > 0:
                item_display.append(f"{item_name}×{item_data['拥有数量']}")
        print(f"  {', '.join(item_display) if item_display else '无'}\n")
        
        # -------------------------- 结局触发检查 --------------------------
        # 1. 生存结局（首次达到200天提示）
        if day >= 200 and not has_asked_survival_end:
            no(0)
            print(f"{GREEN}===== 生存结局达成！====={RESET}")
            print(f"{GREEN}你已在末日中生存了{day}天，成为了传奇幸存者！{RESET}")
            achievements = check_achievement(achievements, "顽强求生")  # 解锁成就
            choice = input(f"{ORANGE}请选择：{RESET}\n1. 结束游戏（保留成就）\n2. 继续挑战（冲击更高天数）\n选择: ")
            while choice not in ["1", "2"]:
                print(f"{RED}无效选择，请输入1或2！{RESET}")
                choice = input("选择: ")
            if choice == "1":
                print(f"{GREEN}恭喜你成功生存，游戏结束！{RESET}")
                no(1)
                return
            else:
                print(f"{ORANGE}你决定继续挑战，看看自己能走多远...{RESET}")
                has_asked_survival_end = True  # 标记为已询问，不再提示
                no(1)
        
        # 2. 猫咪结局（有猫咪且生存50天）
        if items["猫咪"]["拥有数量"] > 0 and day >= 50:
            if random.randint(1, 100) <= 5:  # 5%概率触发
                no(0)
                print(f"{GREEN}===== 猫咪结局达成！====={RESET}")
                print(f"{GREEN}猫咪的叫声吸引了救援直升机，你被成功营救！{RESET}")
                achievements = check_achievement(achievements, "猫咪伙伴")
                no(1)
                return
        
        # 3. 军方结局（军方来过且后续每天1/500概率）
        if military_visited and random.randint(1, 500) == 1:
            no(0)
            print(f"{GREEN}===== 军方结局达成！====={RESET}")
            print(f"{GREEN}军方救援部队根据之前的接触记录，找到了你的位置！{RESET}")
            achievements = check_achievement(achievements, "军方信任者")
            no(1)
            return
        
        # 4. 极寒结局（冬季每天1/1000概率）
        if winter and random.randint(1, 1000) == 1:
            no(0)
            print(f"{GREEN}===== 极寒结局达成！====={RESET}")
            print(f"{GREEN}一支极地救援队在暴风雪中发现了你，带你回到安全区！{RESET}")
            achievements = check_achievement(achievements, "寒冬勇士")
            no(1)
            return
        
        
        
        # 6. 冲出封锁区结局（每天1/100概率出现选项，选择后1/10成功）
        if random.randint(1, 100) == 1:
            choice = input(f"{ORANGE}发现一处封锁薄弱点，是否尝试突围？{RESET}（1.是 2.否）: ")
            if choice == "1":
                print(f"{ORANGE}你屏住呼吸，快速冲向封锁线...{RESET}")
                time.sleep(2)
                if random.randint(1, 10) == 1:
                    no(0)
                    print(f"{GREEN}===== 冲出封锁区结局达成！====={RESET}")
                    print(f"{GREEN}你成功突破封锁，进入了未被污染的安全地带！{RESET}")
                    achievements = check_achievement(achievements, "突围者")
                    no(1)
                    return
                else:
                    print(f"{RED}突围失败，被巡逻队发现，健康值-3，获得【受伤】状态！{RESET}")
                    health -= 3
                    status["受伤"] = True
                    no(1)
        
        # 7. 隐藏结局：神仙降临（每天1/1亿概率）
        if random.randint(1, 100000000) == 1:
            no(0)
            print(f"{PURPLE}===== 神仙降临结局达成！====={RESET}")
            print(f"{PURPLE}天空裂开一道金光，一位神仙降临，挥手间灾难消失，世界恢复和平！{RESET}")
            achievements = check_achievement(achievements, "天命之子")
            no(1)
            return
        
        # -------------------------- 成就检查 --------------------------
        # 生存天数成就
        if day == 100:
            achievements = check_achievement(achievements, "生存达人")
        # 道具收集成就
        if items["猫咪"]["拥有数量"] > 0:
            achievements = check_achievement(achievements, "猫咪守护者")
        if items["电脑"]["拥有数量"] > 0:
            achievements = check_achievement(achievements, "技术专家")
        if items["罐头"]["拥有数量"] >= 100:
            achievements = check_achievement(achievements, "物资大亨")
        if items["水瓶"]["拥有数量"] >= 100:
            achievements = check_achievement(achievements, "水资源管理者")
        if items["急救包"]["拥有数量"] >= 10:
            achievements = check_achievement(achievements, "医疗兵")
        # 连续正面事件成就
        if consecutive_positive >= 5:
            achievements = check_achievement(achievements, "幸运儿")
        # 全道具收集成就
        has_all_items = all(item["拥有数量"] > 0 for item in items.values())
        if has_all_items:
            achievements = check_achievement(achievements, "收藏家")
        # 难度成就
        if name == "5" and day >= 50:  # 困难难度50天
            achievements = check_achievement(achievements, "困难征服者")
        if name == "6" and day >= 30:  # 极其困难难度30天
            achievements = check_achievement(achievements, "极限生存者")
        
        # -------------------------- 每日行动选择 --------------------------
        while True:
            # 显示当前状态（关键信息，不立即清屏）
            print(f"{ORANGE}===== 第 {day} 天 ====={RESET}")
            print(f"{RED}健康值: {round(health, 1)}/10 | {ORANGE}饥饿值: {round(hunger, 1)}/6 | {BLUE}口渴值: {round(thirst, 1)}/6{RESET}")
            action = input(f'''{GREEN}请选择行动:{RESET}
    1. 搜寻物资（风险高，收益高）
    2. 休息恢复（健康+1，饥饿/口渴-0.5）
    3. 使用道具（恢复状态或触发效果）
    4. 保存游戏
    5. 退出游戏
    选择: ''')
            
            # 1. 搜寻物资
            if action == "1":
                print(f"{ORANGE}你拿起工具，外出搜寻物资...{RESET}")
                time.sleep(2)
                
                # 触发事件
                event_prob = random.randint(1, 100)
                if event_prob <= xg['正面事件发生几率']:
                    sj = random.choice(events_positive)
                    consecutive_positive += 1
                elif event_prob <= xg['正面事件发生几率'] + xg['负面事件发生几率']:
                    sj = random.choice(events_negative)
                    consecutive_positive = 0
                else:
                    sj = '无事发生'
                    consecutive_positive = 0
                
                # 处理事件
                if sj != '无事发生':
                    no(0)
                    print(f"{ORANGE}触发事件：{sj}{RESET}")
                    print(f"{events_Speech[sj]}")
                    
                    # 正面事件处理
                    if sj == '发现食物':
                        hunger = min(6, hunger + 1)
                    elif sj == '找到干净的水源':
                        thirst = min(6, thirst + 1)
                    elif sj == '遇到友善的幸存者':
                        items['罐头']['拥有数量'] += 1
                    elif sj == '找到医疗包':
                        health = min(10, health + 2)
                        items['急救包']['拥有数量'] += 1
                    elif sj == '发现道具':
                        # 随机获得1件常用道具
                        common_items = ['绷带', '火柴盒', '电池', '绳子']
                        target_item = random.choice(common_items)
                        items[target_item]['拥有数量'] += 1
                        print(f"{GREEN}获得：{target_item}×1{RESET}")
                    elif sj == '外面有动静':
                        # 详细交互逻辑（已优化等待）
                        choice = input(f"{ORANGE}选择：{RESET}\n1. 悄悄查看\n2. 原地隐藏\n选择: ")
                        if choice == '1':
                            if random.randint(1, 2) == 1:
                                print(f"{GREEN}发现一个遗弃背包，获得罐头×1、水瓶×1！{RESET}")
                                items['罐头']['拥有数量'] += 1
                                items['水瓶']['拥有数量'] += 1
                            else:
                                print(f"{RED}突然冲出一只野狗，你被咬伤！健康-3，获得【受伤】状态！{RESET}")
                                health -= 3
                                status['受伤'] = True
                        else:
                            print(f"{GREEN}你屏住呼吸，动静逐渐消失，安全返回！{RESET}")
                            xg['正面事件发生几率'] = min(100, xg['正面事件发生几率'] + 3)
                    elif sj == '天气转好':
                        xg['正面事件发生几率'] = min(100, xg['正面事件发生几率'] + 5)
                    elif sj == '发现补给箱':
                        items['罐头']['拥有数量'] += 2
                        items['水瓶']['拥有数量'] += 2
                    elif sj == '遇到救援队伍':
                        items['罐头']['拥有数量'] += 1
                        items['水瓶']['拥有数量'] += 1
                    elif sj == '发现物资箱':
                        # 随机获得2件道具
                        all_items = list(items.keys())
                        for _ in range(2):
                            target_item = random.choice(all_items)
                            items[target_item]['拥有数量'] += 1
                            print(f"{GREEN}获得：{target_item}×1{RESET}")
                    elif sj == '发现猫咪':
                        items['猫咪']['拥有数量'] += 1
                    elif sj == '发现电脑':
                        items['电脑']['拥有数量'] += 1
                    
                    # 负面事件处理
                    elif sj == '遭遇野兽攻击':
                        health -= 2
                        status['受伤'] = True
                    elif sj == '食物中毒':
                        health -= 1
                        status['生病'] = True
                    elif sj == '遇到敌对幸存者':
                        items['罐头']['拥有数量'] = max(0, items['罐头']['拥有数量'] - 1)
                        items['水瓶']['拥有数量'] = max(0, items['水瓶']['拥有数量'] - 1)
                    elif sj == '受伤感染':
                        health -= 2
                        status['生病'] = True
                        status['受伤'] = True
                    elif sj == '道具损坏':
                        # 随机损坏1件非关键道具
                        breakable_items = [item for item in items if item not in ['猫咪', '电脑'] and items[item]['拥有数量'] > 0]
                        if breakable_items:
                            broken_item = random.choice(breakable_items)
                            items[broken_item]['拥有数量'] -= 1
                            print(f"{RED}道具损坏：{broken_item}×1{RESET}")
                    elif sj == '恶劣天气来袭':
                        xg['负面事件发生几率'] = min(100, xg['负面事件发生几率'] + 5)
                    elif sj == '迷路了':
                        hunger -= 0.5
                        xg['正面事件发生几率'] = max(0, xg['正面事件发生几率'] - 5)
                    elif sj == '水源被污染':
                        thirst -= 0.5
                    elif sj == '军方来到':
                        military_visited = True
                        items['罐头']['拥有数量'] += 3
                        items['水瓶']['拥有数量'] += 3
                    elif sj == '建筑物倒塌':
                        health -= 3
                        status['受伤'] = True
                    elif sj == '极端寒冷':
                        health -= 1
                        hunger -= 1
                        thirst -= 1
                    
                    no(1)  # 事件处理后等待用户确认
                else:
                    print(f"{GREEN}一整天平安无事，你收集了一些基础物资（罐头×1，水瓶+1）。{RESET}")
                    items['罐头']['拥有数量'] += 1
                    items['水瓶']['拥有数量'] += 1
                    no(1)
                break  # 搜寻后结束当天
            # 2. 休息恢复
            elif action == "2":
                print(f"{GREEN}你回到营地休息，恢复体力...{RESET}")
                health = min(10, health + 1)
                hunger -= 0.5
                thirst -= 0.5
                
                # 30%概率恢复状态
                if random.randint(1, 100) <= 30:
                    if status["生病"] and random.randint(1, 2) == 1:
                        status["生病"] = False
                        print(f"{GREEN}你的病在休息后好转了！{RESET}")
                    if status["受伤"] and random.randint(1, 2) == 1:
                        status["受伤"] = False
                        print(f"{GREEN}你的伤口在休息后愈合了！{RESET}")
                no(1)
                break  # 休息后结束当天
            
            # 3. 使用道具
            elif action == "3":
                print(f"\n{GREEN}可用道具:{RESET}")
                usable_items = []
                for i, (item_name, item_data) in enumerate(items.items()):
                    if item_data["拥有数量"] > 0 and item_name not in ['猫咪']:
                        usable_items.append((i+1, item_name, item_data))
                        print(f"{i+1}. {item_name}×{item_data['拥有数量']}")
                
                if not usable_items:
                    print(f"{RED}无可用道具！{RESET}")
                    no(1)
                    continue
                
                # 选择道具
                try:
                    choice = int(input(f"{ORANGE}选择道具：{RESET}")) - 1
                    if 0 <= choice < len(usable_items):
                        idx, item_name, item_data = usable_items[choice]
                        items[item_name]['拥有数量'] -= 1
                        print(f"{GREEN}使用了：{item_name}{RESET}")
                        
                        # 道具效果
                        if item_name == '罐头':
                            hunger = min(6, hunger + 2)
                            print(f"{ORANGE}饥饿值恢复2点！{RESET}")
                        elif item_name == '水瓶':
                            thirst = min(6, thirst + 2)
                            print(f"{BLUE}口渴值恢复2点！{RESET}")
                        elif item_name == '绷带':
                            if status["受伤"]:
                                status["受伤"] = False
                                print(f"{GREEN}受伤状态恢复！{RESET}")
                            else:
                                print(f"{ORANGE}你没有受伤，无需使用绷带！{RESET}")
                        elif item_name == '急救包':
                            health = min(10, health + 3)
                            status["生病"] = False
                            status["受伤"] = False
                            print(f"{GREEN}健康值恢复3点，所有负面状态清除！{RESET}")
                        elif item_name == '手电筒':
                            xg['正面事件发生几率'] = min(100, xg['正面事件发生几率'] + 5)
                            print(f"{BLUE}正面事件概率+5%！{RESET}")
                        elif item_name == '电池':
                            if items['手电筒']['拥有数量'] > 0:
                                xg['正面事件发生几率'] = min(100, xg['正面事件发生几率'] + 3)
                                print(f"{BLUE}手电筒续航增加，正面事件概率+3%！{RESET}")
                            else:
                                print(f"{ORANGE}你没有手电筒，电池无用！{RESET}")
                        elif item_name == '刀具':
                            xg['负面事件发生几率'] = max(0, xg['负面事件发生几率'] - 5)
                            print(f"{RED}负面事件概率-5%！{RESET}")
                        elif item_name == '绳子':
                            print(f"{GREEN}你用绳子加固了营地，安全感提升！{RESET}")
                        elif item_name == '火柴盒':
                            if winter:
                                health = min(10, health + 1)
                                print(f"{BLUE}生火取暖，健康值+1！{RESET}")
                            else:
                                hunger = min(6, hunger + 1)
                                print(f"{ORANGE}生火烹饪，饥饿值+1！{RESET}")
                        elif item_name == '帐篷':
                            xg['生病发生几率'] = max(0, xg['生病发生几率'] - 10)
                            print(f"{GREEN}生病概率-10%！{RESET}")
                        elif item_name == '物资箱':
                            # 打开物资箱获得3件道具
                            all_items = list(items.keys())
                            for _ in range(3):
                                target_item = random.choice(all_items)
                                items[target_item]['拥有数量'] += 1
                                print(f"{GREEN}获得：{target_item}×1{RESET}")
                        # 5. 电子救援结局（有电脑且每天使用1/100概率）
                        elif item_name == '电脑':
                            use_pc = input(f"{BLUE}使用电脑做什么？{RESET}（1.发送求救信号（不消耗道具） 2.寻找物资地点）: ")
                            if use_pc == "1":
                                print(f"{BLUE}你打开电脑，尝试发送求救信号...{RESET}")
                                time.sleep(2)
                                if random.randint(1, 100) == 1:
                                    no(0)
                                    print(f"{GREEN}===== 电子救援结局达成！====={RESET}")
                                    print(f"{GREEN}求救信号被附近的科考队接收，你被成功救援！{RESET}")
                                    achievements = check_achievement(achievements, "数字救援")
                                    no(1)
                                    return
                                else:
                                    print(f"{GREEN}未收到回应……{RESET}")
                                    no(1)
                            elif use_pc == "2":
                                print(f"{ORANGE}你决定用电脑寻找物资……{RESET}")
                                time.sleep(2)
                                print(f"{GREEN}找到了一个隐藏的物资仓库，获得罐头+4、水瓶+3！{RESET}")
                                items["罐头"]["拥有数量"] += 4
                                items["水瓶"]["拥有数量"] += 3
                                no(1)
                    else:
                        print(f"{RED}无效选择！{RESET}")
                except:
                    print(f"{RED}无效输入！{RESET}")
                no(1)
            
            # 4. 保存游戏
            elif action == "4":
                save_data = {
                    "day": day, "hunger": hunger, "thirst": thirst, "health": health,
                    "status": status, "xg": xg, "items": items,
                    "difficulty": name, "character": pep,
                    "military_visited": military_visited,
                    "consecutive_positive": consecutive_positive,
                    "has_asked_survival_end": has_asked_survival_end
                }
                save_game(save_data)
            
            # 5. 退出游戏
            elif action == "5":
                confirm = input(f"{RED}确定退出游戏吗？（进度会丢失）{RESET}（y/n）: ")
                if confirm.lower() == "y":
                    print(f"{WHITE}感谢游玩！{RESET}")
                    time.sleep(2)
                    exit()
                else:
                    print(f"{GREEN}取消退出，继续游戏！{RESET}")
                    no(1)
            
            # 无效选择
            else:
                print(f"{RED}无效选择，请输入1-5！{RESET}")
                no(1)
        
        # -------------------------- 每日状态衰减 --------------------------
        # 饥饿/口渴自然消耗
        hunger -= 1
        thirst -= 1
        
        # 负面状态消耗
        if status["生病"]:
            health -= 0.5; hunger -= 0.5; thirst -= 0.5
        if status["受伤"]:
            health -= 0.3
        
        # 数值边界限制
        hunger = max(0, round(hunger, 1))
        thirst = max(0, round(thirst, 1))
        health = max(0, round(health, 1))

        #极度饥饿/口渴额外扣血
        if hunger == 0 and not status["极度饥饿"]:
            status["极度饥饿"] = True
            hunger = xg['饥饿保持天数'] -1
        if thirst == 0 and not status["极度口渴"]:
            status["极度口渴"] = True
            thirst = xg['口渴保持天数'] -1

        #恢复正常检查
        if hunger > xg["饥饿保持天数"] and status["极度饥饿"] :
            status["极度饥饿"] = False
            hunger = 6
        if thirst > xg["口渴保持天数"] and status["极度口渴"] :
            status["极度口渴"] = False
            thirst = 6
        
        # -------------------------- 死亡检查 --------------------------
        if health <= 0:
            no(0)
            print(f"{RED}===== 游戏结束 ====={RESET}")
            print(f"{RED}你因伤势过重，在第{day}天倒下了...{RESET}")
            print(f"{ORANGE}最终生存天数：{day}天{RESET}")
            no(1)
            return
        if hunger <= 0 and status["极度饥饿"]:
            no(0)
            print(f"{RED}===== 游戏结束 ====={RESET}")
            print(f"{RED}你因极度饥饿，在第{day}天倒下了...{RESET}")
            print(f"{ORANGE}最终生存天数：{day}天{RESET}")
            no(1)
            return
        if thirst <= 0 and status["极度口渴"]:
            no(0)
            print(f"{RED}===== 游戏结束 ====={RESET}")
            print(f"{RED}你因极度口渴，在第{day}天倒下了...{RESET}")
            print(f"{ORANGE}最终生存天数：{day}天{RESET}")
            no(1)
            return
        
        # -------------------------- 随机生病检查 --------------------------
        if not status["生病"] and random.randint(1, 100) <= xg['生病发生几率']:
            status["生病"] = True
            print(f"{RED}你感觉身体不适，患上了疾病！{RESET}")
            no(1)
        
        # 天数递增
        day += 1