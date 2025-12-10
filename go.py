'''
末日求生
1.1.0 - pre.2
更新内容：
1.修复了选择道具的显示错误
2.添加了github选项
3.添加了kook频道快捷加入选项
4.删除了过滤动画
'''

import os  # 导入操作系统接口，用于清屏等文件路径操作
import random  # 导入随机模块，用于事件与概率判断
import time  # 导入时间模块，用于延迟与等待
import pickle  # 导入 pickle，用于二进制序列化成就数据
import tkinter as tk  # 导入 tkinter，用于文件对话框
from tkinter import filedialog  # 从 tkinter 导入文件对话框函数
import gmusic  # 导入自定义音乐模块，用于播放背景音乐

root = tk.Tk()  # 创建 tkinter 根窗口实例（用于文件对话框）
root.withdraw()  # 隐藏 tkinter 根窗口，避免弹出空白窗口

# 定义颜色变量，控制终端输出的颜色
RED = '\033[31m'  # 红色文本
GREEN = '\033[32m'  # 绿色文本
ORANGE = '\033[33m'  # 橙色/黄色文本
WHITE = '\033[37m'  # 白色文本
BLUE = '\033[34m'  # 蓝色文本
PURPLE = '\033[35m'  # 紫色文本
CYAN = '\033[36m'  # 青色文本
RESET = '\033[0m'  # 重置文本颜色

# -------------------------- 成就系统（二进制存储）--------------------------
# 初始化成就模板，包含成就名、描述与是否解锁标志
DEFAULT_ACHIEVEMENTS = {  # 默认成就字典
    "生存达人": {"desc": "生存100天", "unlocked": False},  # 生存100天成就
    "顽强求生": {"desc": "生存200天", "unlocked": False},  # 生存200天成就
    "猫咪守护者": {"desc": "获得猫咪道具", "unlocked": False},  # 获得猫咪道具成就
    "技术专家": {"desc": "获得电脑道具", "unlocked": False},  # 获得电脑成就
    "物资大亨": {"desc": "拥有100个罐头", "unlocked": False},  # 拥有大量罐头成就
    "水资源管理者": {"desc": "拥有100个水瓶", "unlocked": False},  # 拥有大量水瓶成就
    "医疗兵": {"desc": "拥有10个急救包", "unlocked": False},  # 拥有多个急救包成就
    "幸运儿": {"desc": "连续5天触发正面事件", "unlocked": False},  # 连续正面事件成就
    "收藏家": {"desc": "获得所有类型的道具", "unlocked": False},  # 收集所有道具成就
    "困难征服者": {"desc": "在困难难度下生存50天", "unlocked": False},  # 困难难度成就
    "极限生存者": {"desc": "在极其困难难度下生存30天", "unlocked": False},  # 极其困难成就
    "军方信任者": {"desc": "获得军方结局", "unlocked": False},  # 军方结局成就
    "寒冬勇士": {"desc": "获得极寒结局", "unlocked": False},  # 极寒结局成就
    "数字救援": {"desc": "通过电脑获得救援", "unlocked": False},  # 电子救援成就
    "突围者": {"desc": "成功冲出封锁区", "unlocked": False},  # 冲出封锁区成就
    "天命之子": {"desc": "解锁神仙降临结局", "unlocked": False},  # 隐藏神仙结局成就
    "猫咪伙伴": {"desc": "获得猫咪结局", "unlocked": False}  # 猫咪结局成就
}
ACHIEVEMENT_FILE = "achievements.cjt"  # 成就文件名，使用自定义后缀并以二进制存储
NAME='1'

def save_achievements(achievements):  # 保存成就函数，接受成就字典
    """保存成就到二进制文件（无法直接修改）"""  # 函数说明：使用 pickle 写入文件
    if NAME!='1':
        try:
            with open(ACHIEVEMENT_FILE, "wb") as f:  # 以二进制写模式打开文件
                pickle.dump(achievements, f, protocol=pickle.HIGHEST_PROTOCOL)  # 使用最高协议序列化并写入
        except Exception as e:  # 捕获任何异常并提示
            print(f"{RED}成就保存失败：{str(e)}{RESET}")  # 打印错误信息
            no(1)  # 等待用户按回车继续

def load_achievements():  # 加载成就函数，返回成就字典
    """加载成就（文件不存在则初始化）"""  # 函数说明：如果文件损坏或不存在则使用默认成就
    if os.path.exists(ACHIEVEMENT_FILE):  # 检查成就文件是否存在
        try:
            with open(ACHIEVEMENT_FILE, "rb") as f:  # 以二进制读模式打开文件
                return pickle.load(f)  # 反序列化并返回成就字典
        except Exception as e:  # 若加载失败则提示并返回默认成就
            print(f"{RED}成就文件损坏，使用默认成就！{RESET}")  # 打印警告
            no(1)  # 等待用户输入
            return DEFAULT_ACHIEVEMENTS.copy()  # 返回默认成就的副本
    else:
        init_achievements = DEFAULT_ACHIEVEMENTS.copy()  # 首次运行初始化成就副本
        save_achievements(init_achievements)  # 保存初始化后的成就文件
        return init_achievements  # 返回初始化的成就字典

def show_achievements():  # 显示成就列表的函数
    """显示成就列表（关键信息，等待用户输入）"""  # 函数说明：打印所有成就并统计已解锁数量
    achievements = load_achievements()  # 加载当前成就数据
    print(f"{PURPLE}===== 成就列表 ====={RESET}\n")  # 打印成就标题
    unlocked_count = 0  # 统计已解锁数量的初始值
    for name, data in achievements.items():  # 遍历成就字典
        status = f"{GREEN}【已解锁】{RESET}" if data["unlocked"] else f"{RED}【未解锁】{RESET}"  # 设置显示状态文本
        print(f"{name}：{data['desc']} {status}")  # 打印成就名称、描述与状态
        if data["unlocked"]:  # 如果已解锁则计数
            unlocked_count += 1  # 已解锁计数加一
    print(f"\n{BLUE}已解锁 {unlocked_count}/{len(achievements)} 个成就{RESET}")  # 打印解锁统计

def check_achievement(achievements, name):  # 检查并解锁指定成就的函数
    """检查并解锁成就（显示后等待用户确认）"""  # 函数说明：若未解锁则修改并保存
    if not achievements[name]["unlocked"]:  # 如果该成就尚未解锁
        achievements[name]["unlocked"] = True  # 将成就标记为已解锁
        save_achievements(achievements)  # 保存修改后的成就文件
        print(f"\n{CYAN}===== 成就解锁！====={RESET}")  # 打印提示标题
        print(f"{CYAN}成就名称：{name}{RESET}")  # 显示成就名称
        print(f"{CYAN}成就描述：{achievements[name]['desc']}{RESET}")  # 显示成就描述
        no(1)  # 等待用户按回车以确保看清提示
    return achievements  # 返回（可能已更新的）成就字典

# -------------------------- 存档系统 --------------------------
def save_game(data):  # 保存进度函数，接受游戏数据字典
    """保存游戏进度（json格式，方便导入）"""  # 函数说明：使用文件对话框选择保存位置
    try:
        file_path = filedialog.asksaveasfilename(  # 打开保存文件对话框并获取路径
            defaultextension=".json",  # 默认扩展名为 .json
            filetypes=[("存档文件", "*.json"), ("所有文件", "*.*")],  # 可选文件类型
            title="保存游戏"  # 对话框标题
        )
        if file_path:  # 如果用户选择了路径
            import json  # 局部导入 json 模块以写入文本格式
            with open(file_path, "w", encoding="utf-8") as f:  # 以 utf-8 写模式打开目标文件
                json.dump(data, f, ensure_ascii=False, indent=4)  # 写入格式化的 json 数据
            print(f"{GREEN}存档成功：{file_path}{RESET}")  # 提示保存成功
    except Exception as e:  # 捕获并显示保存错误
        print(f"{RED}存档失败：{str(e)}{RESET}")  # 打印错误信息
    no(1)  # 等待用户确认

def import_game():  # 导入存档函数
    """导入游戏进度"""  # 函数说明：使用文件对话框选择要导入的 json 存档
    try:
        file_path = filedialog.askopenfilename(  # 打开文件选择对话框
            filetypes=[("存档文件", "*.json"), ("所有文件", "*.*")],  # 允许的文件类型
            title="导入游戏"  # 对话框标题
        )
        if file_path:  # 如果用户选择了文件
            import json  # 局部导入 json 模块以读取数据
            with open(file_path, "r", encoding="utf-8") as f:  # 以 utf-8 读模式打开文件
                data = json.load(f)  # 解析 json 数据为字典
            print(f"{GREEN}导入成功！正在加载...{RESET}")  # 提示加载中
            time.sleep(2)  # 等待短暂时间以模拟加载
            game(data, None, None)  # 使用导入的数据启动游戏主循环（作为存档加载）
    except Exception as e:  # 捕获导入过程中的异常并显示
        print(f"{RED}导入失败：{str(e)}{RESET}")  # 打印错误信息
    no(1)  # 等待用户确认

# -------------------------- 游戏核心逻辑 --------------------------
def no(i):  # 清屏等待函数，与 main.py 保持行为一致
    """清屏函数（与main.py保持一致）"""  # 函数说明：i=1 等待回车，i=0 仅清屏
    if i == 1:  # 如果需要等待
        input(f"\n{ORANGE}按回车继续...{RESET}")  # 等待用户按回车
    os.system('cls' if os.name == 'nt' else 'clear')  # 根据操作系统选择清屏命令并执行

def game(saved_data, name, pep):  # 游戏主循环函数，接受存档数据、难度和角色选择
    """游戏主循环"""  # 函数说明：初始化、循环天数与事件处理均在此函数中完成
    global NAME
    NAME=name

    mu = gmusic.go()  # 创建音乐控制对象 mu，用于播放背景音乐
    mu.play_ogg("general_war_theattack.ogg", -1)  # 播放开场音乐，loops=-1 表示循环播放
    achievements = load_achievements()  # 加载成就数据以便后续解锁与保存
    
    # -------------------------- 初始化游戏参数 --------------------------
    xg = {'道具获得几率':50, '饥饿保持天数':3, '口渴保持天数':2,  # 默认平衡参数字典
          '负面事件发生几率':50, '正面事件发生几率':50, '生病发生几率':25}  # 包含事件与生病几率等

    # 事件列表（正面与负面），可以扩展以增加游戏内容
    events_positive = [  # 正面事件名称列表
        '发现食物', '找到干净的水源', '遇到友善的幸存者', '找到医疗包',
        '发现道具', '外面有动静', '天气转好', '发现补给箱', '遇到救援队伍',
        '发现物资箱', '发现猫咪', '发现电脑','春暖花开','找到商店','发现受伤幸存者','没有遇到丧尸'
    ]
    events_negative = [  # 负面事件名称列表
        '遭遇野兽攻击', '食物中毒', '遇到敌对幸存者', '受伤感染',
        '道具损坏', '恶劣天气来袭', '迷路了', '水源被污染', '军方来到',
        '建筑物倒塌', '极端寒冷', '中暑', '被变异树的叶子砸伤','踩到陷阱',
        '遇到小型尸群','遇到中型尸群','遇到大型尸群'
    ]
    
    # 事件对应的文字描述，用于在触发事件时显示给玩家
    events_Speech = {  # 事件到文本的映射字典
        '发现食物':'你在废墟中找到半块面包，饥饿值恢复1点。',  # 文本：发现食物
        '找到干净的水源':'发现一处未污染的小溪，口渴值恢复1点。',  # 文本：找到水源
        '遇到友善的幸存者':'他分给你1个罐头，感谢你的帮助。',  # 文本：友善幸存者
        '找到医疗包':'在废弃医院找到1个急救包，健康值+2。',  # 文本：找到医疗包
        '发现道具':'随机获得1件常用道具（绷带/火柴等）。',  # 文本：发现道具
        '外面有动静':'远处传来奇怪的声音，可能是危险也可能是机会。',  # 文本：外面有动静
        '天气转好':'阳光明媚，正面事件概率+5%。',  # 文本：天气转好
        '发现补给箱':'获得罐头+2、水瓶+2。',  # 文本：发现补给箱
        '遇到救援队伍':'获得罐头+1、水瓶+1。',  # 文本：遇到救援队伍
        '发现物资箱':'打开后随机获得2件道具！',  # 文本：发现物资箱
        '发现猫咪':'一只流浪猫信任你，跟着你回到营地（触发猫咪结局必备）。',  # 文本：发现猫咪
        '发现电脑':'找到一台能工作的笔记本电脑（触发电子救援结局必备）。',  # 文本：发现电脑
        '春暖花开':'春天来了，正面事件概率+5%。',  # 文本：春暖花开（春季特有）
        '找到商店':'你在街角发现一家幸存的商店，货架上还有些物资。罐头+5，水瓶+5',  # 文本：找到商店
        '发现受伤幸存者':'你发现一名受伤的幸存者，救助后他给了你些补给并道谢。罐头+2',  # 文本：发现受伤幸存者
        '没有遇到丧尸':'今天没有遇到丧尸，心情稍微好了一些。健康值+1',  # 文本：没有遇到丧尸
        '遭遇野兽攻击':'被野狗咬伤，健康值-2，获得【受伤】状态。',  # 文本：野兽攻击
        '食物中毒':'吃了变质食物，健康值-1，获得【生病】状态。',  # 文本：食物中毒
        '遇到敌对幸存者':'被抢走1个罐头和1个水瓶。',  # 文本：遇到敌对幸存者
        '受伤感染':'伤口发炎，健康值-2，同时获得【生病】和【受伤】状态。',  # 文本：受伤感染
        '道具损坏':'随机1件道具（非关键）损坏消失。',  # 文本：道具损坏
        '恶劣天气来袭':'暴雨导致负面事件概率+5%。',  # 文本：恶劣天气
        '迷路了':'浪费1天时间，饥饿值-0.5，正面事件概率-5%。',  # 文本：迷路
        '水源被污染':'找到的水不能喝，口渴值-0.5。',  # 文本：水源污染
        '军方来到':'军方搜查后留下3个罐头和3个水瓶（触发军方结局必备）。',  # 文本：军方来到
        '建筑物倒塌':'躲避不及被砸伤，健康值-3，获得【受伤】状态。',  # 文本：建筑物倒塌
        '极端寒冷':'体温下降，健康值-1，饥饿值-1，口渴值-1。',  # 文本：极端寒冷
        '中暑':'夏天高温导致身体不适，健康值-1，口渴值-1。',  # 文本：中暑
        '被变异树的叶子砸伤':'秋天被掉落的变异树叶砸中，健康值-2，获得【受伤】状态。',  # 文本：变异树叶
        '踩到陷阱':'不小心踩到陷阱，健康值-4，获得【受伤】状态。',  # 文本：踩到陷阱
        '遇到小型尸群':'遇到一小群丧尸，发生争斗并受伤。获得【受伤】状态',  # 文本：小型尸群
        '遇到中型尸群':'遇到中等规模的尸群，战斗很危险。获得【受伤】状态并健康值-2',  # 文本：中型尸群
        '遇到大型尸群':'遇到大型尸群，极大伤害风险。获得【受伤】状态并健康值-4'  # 文本：大型尸群
    }
    
    # 道具字典，记录每种道具的获得几率、每次获得数量与当前拥有数量
    items = {  # 初始化道具与其属性
        '罐头': {'获得几率':70, '获得数量':2, '拥有数量':4},  # 罐头初始数量4
        '水瓶': {'获得几率':70, '获得数量':2, '拥有数量':3},  # 水瓶初始数量3
        '绷带': {'获得几率':50, '获得数量':1, '拥有数量':0},  # 绷带初始0
        '急救包': {'获得几率':30, '获得数量':1, '拥有数量':0},  # 急救包初始0
        '手电筒': {'获得几率':15, '获得数量':1, '拥有数量':0},  # 手电筒初始0
        '电池': {'获得几率':50, '获得数量':2, '拥有数量':0},  # 电池初始0
        '刀具': {'获得几率':30, '获得数量':1, '拥有数量':0},  # 刀具初始0
        '绳子': {'获得几率':30, '获得数量':1, '拥有数量':0},  # 绳子初始0
        '火柴盒': {'获得几率':40, '获得数量':3, '拥有数量':0},  # 火柴盒初始0
        '帐篷': {'获得几率':20, '获得数量':1, '拥有数量':0},  # 帐篷初始0
        '猫咪': {'获得几率':1, '获得数量':1, '拥有数量':0},  # 猫咪极其稀有，初始0
        '电脑': {'获得几率':5, '获得数量':1, '拥有数量':0},  # 电脑稀有，初始0
        '物资箱': {'获得几率':10, '获得数量':1, '拥有数量':0}  # 物资箱中等稀有，初始0
    }
    
    # 如果有存档数据则从中加载状态
    if saved_data:  # 若传入了 saved_data 则进行恢复
        day = saved_data["day"]  # 恢复天数
        hunger = saved_data["hunger"]  # 恢复饥饿值
        thirst = saved_data["thirst"]  # 恢复口渴值
        health = saved_data["health"]  # 恢复健康值
        status = saved_data["status"]  # 恢复状态字典
        xg = saved_data["xg"]  # 恢复平衡参数
        items = saved_data["items"]  # 恢复道具数据
        name = saved_data["difficulty"]  # 恢复难度选择
        pep = saved_data["character"]  # 恢复角色选择
        military_visited = saved_data["military_visited"]  # 恢复军方访问标志
        consecutive_positive = saved_data["consecutive_positive"]  # 恢复连续正面事件计数
        has_asked_survival_end = saved_data["has_asked_survival_end"]  # 恢复是否已经询问200天结局
    else:
        # 根据难度调整基础参数
        if name == '1':  # 新手难度调整参数
            xg['道具获得几率'] += 50; xg['饥饿保持天数'] += 2; xg['口渴保持天数'] += 3  # 增益
            xg['负面事件发生几率'] -= 50; xg['正面事件发生几率'] += 50; xg['生病发生几率'] -= 25  # 降低难度
        elif name == '2':  # 简单难度调整参数
            xg['道具获得几率'] += 20; xg['饥饿保持天数'] += 1; xg['口渴保持天数'] += 2
            xg['负面事件发生几率'] -= 25; xg['正面事件发生几率'] += 25; xg['生病发生几率'] -= 20
        elif name == '4':  # 加难难度调整参数
            xg['道具获得几率'] -= 25; xg['饥饿保持天数'] -= 1; xg['口渴保持天数'] -= 1
            xg['负面事件发生几率'] += 25; xg['正面事件发生几率'] -= 25; xg['生病发生几率'] += 25
        elif name == '5':  # 困难难度调整参数
            xg['道具获得几率'] -= 40; xg['饥饿保持天数'] -= 2; xg['口渴保持天数'] -= 2
            xg['负面事件发生几率'] += 40; xg['正面事件发生几率'] -= 40; xg['生病发生几率'] += 30
        elif name == '6':  # 极其困难难度调整参数
            xg['道具获得几率'] -= 50; xg['饥饿保持天数'] -= 3; xg['口渴保持天数'] -= 2
            xg['负面事件发生几率'] += 50; xg['正面事件发生几率'] -= 50; xg['生病发生几率'] += 70
        
        # 根据角色选择调整参数
        if pep == '1':  # 父亲角色的属性加成
            xg['道具获得几率'] += 10; xg['饥饿保持天数'] += 1
        elif pep == '2':  # 母亲角色的属性加成
            xg['道具获得几率'] += 15; xg['负面事件发生几率'] -= 10
        
        # 初始状态设置（默认饥饿/口渴上限为6、健康上限为10）
        day = 1; hunger = 6; thirst = 6; health = 10  # 初始天数与属性
        status = {"生病": False, "受伤": False,"极度饥饿": False, "极度口渴": False}  # 初始状态字典
        military_visited = False; consecutive_positive = 0  # 初始事件计数与军方标志
        has_asked_survival_end = False  # 标记是否已询问 200 天结局，初始为 False
    
    # -------------------------- 游戏主循环 --------------------------
    while True:  # 无限循环，直到触发返回或结束
        season = (day // 30) % 4  # 计算季节索引：每 30 天一个季节
        winter = season == 3  # 当季节为 3 时视为冬季（用于极寒概率与效果）
        autumn = season == 2  # 当季节为 2 时视为秋季(用于变异树叶子事件)
        summer = season == 1  # 当季节为 1 时视为夏季（用于中暑事件）
        spring = season == 0  # 当季节为 0 时视为春季（用于春暖花开事件）
        
        # -------------------------- 结局触发检查 --------------------------
        if day >= 200 and not has_asked_survival_end:  # 首次达到 200 天时提示结局选择
            no(0)  # 清屏但不等待
            print(f"{GREEN}===== 生存结局达成！====={RESET}")  # 打印生存结局标题
            print(f"{GREEN}你已在末日中生存了{day}天，成为了传奇幸存者！{RESET}")  # 结局描述
            achievements = check_achievement(achievements, "顽强求生")  # 解锁 200 天成就
            choice = input(f"{ORANGE}请选择：{RESET}\n1. 结束游戏（保留成就）\n2. 继续挑战（冲击更高天数）\n选择: ")  # 提示用户选择
            while choice not in ["1", "2"]:  # 验证输入合法性
                print(f"{RED}无效选择，请输入1或2！{RESET}")  # 无效输入提示
                choice = input("选择: ")  # 重新读取输入
            if choice == "1":  # 选择结束游戏
                print(f"{GREEN}恭喜你成功生存，游戏结束！{RESET}")  # 结束提示
                no(1)  # 等待用户按回车
                return  # 返回到上层结束游戏
            else:  # 选择继续挑战
                print(f"{ORANGE}你决定继续挑战，看看自己能走多远...{RESET}")  # 继续提示
                has_asked_survival_end = True  # 标记已询问，避免再次弹出
                no(1)  # 等待并继续
        
        # 猫咪结局检查：拥有猫咪并生存至少 50 天且按概率触发
        if items["猫咪"]["拥有数量"] > 0 and day >= 50:  # 条件：拥有猫且天数足够
            if random.randint(1, 100) <= 5:  # 5% 概率触发猫咪结局
                no(0)  # 清屏
                print(f"{GREEN}===== 猫咪结局达成！====={RESET}")  # 打印结局标题
                print(f"{GREEN}猫咪的叫声吸引了救援直升机，你被成功营救！{RESET}")  # 结局描述
                achievements = check_achievement(achievements, "猫咪伙伴")  # 解锁相关成就
                no(1)  # 等待用户查看
                return  # 返回结束游戏
        
        # 军方结局检查：若军方曾出现，则每天有 1/500 概率触发
        if military_visited and random.randint(1, 500) == 1:  # 条件与概率检测
            no(0)  # 清屏
            print(f"{GREEN}===== 军方结局达成！====={RESET}")  # 打印结局标题
            print(f"{GREEN}军方救援部队根据之前的接触记录，找到了你的位置！{RESET}")  # 结局描述
            achievements = check_achievement(achievements, "军方信任者")  # 解锁相关成就
            no(1)  # 等待用户查看
            return  # 返回结束游戏
        
        # 极寒结局检查：冬季时每天有 1/1000 概率触发
        if winter and random.randint(1, 1000) == 1:  # 冬季概率判断
            no(0)  # 清屏
            print(f"{GREEN}===== 极寒结局达成！====={RESET}")  # 打印结局标题
            print(f"{GREEN}一支极地救援队在暴风雪中发现了你，带你回到安全区！{RESET}")  # 结局描述
            achievements = check_achievement(achievements, "寒冬勇士")  # 解锁相关成就
            no(1)  # 等待用户查看
            return  # 返回结束游戏
        
        # 冲出封锁区结局选项：每天有 1/100 概率出现尝试选项，成功概率 1/10
        if random.randint(1, 100) == 1:  # 每日触发判断
            choice = input(f"{ORANGE}发现一处封锁薄弱点，是否尝试突围？{RESET}（1.是 2.否）: ")  # 提示玩家
            if choice == "1":  # 玩家选择尝试突围
                print(f"{ORANGE}你屏住呼吸，快速冲向封锁线...{RESET}")  # 行动描述
                time.sleep(2)  # 暂停以增加紧张感
                if random.randint(1, 10) == 1:  # 1/10 成功几率
                    no(0)  # 清屏
                    print(f"{GREEN}===== 冲出封锁区结局达成！====={RESET}")  # 成功结局提示
                    print(f"{GREEN}你成功突破封锁，进入了未被污染的安全地带！{RESET}")  # 结局描述
                    achievements = check_achievement(achievements, "突围者")  # 解锁相关成就
                    no(1)  # 等待用户查看
                    return  # 结束游戏
                else:  # 突围失败
                    print(f"{RED}突围失败，被巡逻队发现，健康值-3，获得【受伤】状态！{RESET}")  # 失败提示
                    health -= 3  # 扣除生命值
                    status["受伤"] = True  # 标记受伤状态
                    no(1)  # 等待用户查看
        
        # 隐藏结局：神仙降临，极低概率触发
        if random.randint(1, 100000000) == 1:  # 极其罕见的随机触发
            no(0)  # 清屏
            print(f"{PURPLE}===== 神仙降临结局达成！====={RESET}")  # 打印隐藏结局标题
            print(f"{PURPLE}天空裂开一道金光，一位神仙降临，挥手间灾难消失，世界恢复和平！{RESET}")  # 结局描述
            achievements = check_achievement(achievements, "天命之子")  # 解锁此隐藏成就
            no(1)  # 等待用户查看
            return  # 返回结束游戏
        
        # -------------------------- 成就检查 --------------------------
        if day == 100:  # 到达 100 天则解锁生存达人成就
            achievements = check_achievement(achievements, "生存达人")
        if items["猫咪"]["拥有数量"] > 0:  # 持有猫咪解锁守护者成就
            achievements = check_achievement(achievements, "猫咪守护者")
        if items["电脑"]["拥有数量"] > 0:  # 持有电脑解锁技术专家成就
            achievements = check_achievement(achievements, "技术专家")
        if items["罐头"]["拥有数量"] >= 100:  # 拥有大量罐头解锁物资大亨成就
            achievements = check_achievement(achievements, "物资大亨")
        if items["水瓶"]["拥有数量"] >= 100:  # 拥有大量水瓶解锁水资源管理者成就
            achievements = check_achievement(achievements, "水资源管理者")
        if items["急救包"]["拥有数量"] >= 10:  # 拥有足够急救包解锁医疗兵成就
            achievements = check_achievement(achievements, "医疗兵")
        if consecutive_positive >= 5:  # 连续正面事件达到阈值解锁幸运儿成就
            achievements = check_achievement(achievements, "幸运儿")
        has_all_items = all(item["拥有数量"] > 0 for item in items.values())  # 判断是否拥有所有道具
        if has_all_items:  # 若拥有所有种类道具则解锁收藏家成就
            achievements = check_achievement(achievements, "收藏家")
        if name == "5" and day >= 50:  # 在困难难度下生存 50 天解锁困难征服者
            achievements = check_achievement(achievements, "困难征服者")
        if name == "6" and day >= 30:  # 在极其困难难度下生存 30 天解锁极限生存者
            achievements = check_achievement(achievements, "极限生存者")
        
        # -------------------------- 每日行动选择 --------------------------
        while True:  # 每日行动选择循环，直到玩家选择结束当天的行动
            print(f"{ORANGE}===== 第 {day} 天 ====={RESET}")  # 打印当前天数标题
            print(f"{RED}健康值: {round(health, 1)}/10 | {ORANGE}饥饿值: {round(hunger, 1)}/6 | {BLUE}口渴值: {round(thirst, 1)}/6{RESET}")  # 打印生命值、饥饿与口渴
            status_text = []  # 用于拼接当前状态的文本列表
            if status["生病"]: status_text.append(f"{RED}【生病】健康-0.5/天{RESET}")  # 生病状态说明
            if status["受伤"]: status_text.append(f"{RED}【受伤】健康-0.3/天{RESET}")  # 受伤状态说明
            if winter: status_text.append(f"{BLUE}【冬季】极寒风险↑{RESET}")  # 冬季风险提示
            if summer: status_text.append(f"{ORANGE}【夏季】中暑风险↑{RESET}")  # 夏季风险提示
            print(f"状态: {' | '.join(status_text) if status_text else '【正常】'}\n")  # 打印当前状态文本
            
            print(f"{GREEN}当前道具:{RESET}")  # 显示道具标题
            item_display = []  # 用于显示拥有的道具项列表
            for item_name, item_data in items.items():  # 遍历道具字典
                if item_data["拥有数量"] > 0:  # 仅显示拥有数量大于 0 的道具
                    item_display.append(f"{item_name}×{item_data['拥有数量']}")  # 添加显示字符串
            print(f"  {', '.join(item_display) if item_display else '无'}\n")  # 打印拥有的道具列表或“无”
            print()  #空格
            print('当前季节为：',end='')
            if spring:
                print(f'{GREEN}春季{RESET}')
            elif summer:
                print(f'{ORANGE}夏季{RESET}')
            elif autumn:
                print(f'{ORANGE}秋季{RESET}')
            else:
                print(f'{BLUE}冬季{RESET}')
            action = input(f'''{GREEN}请选择行动:{RESET}
    1. 搜寻物资（风险高，收益高）
    2. 休息恢复（健康+1，饥饿/口渴-0.5）
    3. 使用道具（恢复状态或触发效果）
    4. 保存游戏
    5. 退出游戏
    选择: ''')  # 提示玩家选择每日行动
            
            # 1. 搜寻物资逻辑
            if action == "1":
                print(f"{ORANGE}你拿起工具，外出搜寻物资...{RESET}")  # 搜寻提示
                time.sleep(2)  # 暂停以模拟搜寻时间
                
                event_prob = random.randint(1, 100)  # 生成 1-100 的随机数决定事件类型
                if event_prob <= xg['正面事件发生几率']:  # 如果落在正面事件概率范围内
                    sj = random.choice(events_positive)  # 随机选择一个正面事件
                    consecutive_positive += 1  # 连续正面事件计数增加
                    if spring and sj == '天气转好':  # 春季触发春暖花开事件
                        sj = '春暖花开'  # 替换为春暖花开事件
                    elif not spring and sj == '春暖花开':  # 非春季时移除春暖花开事件
                        sj = random.choice(events_positive)  # 重新选择一个正面事件
                    
                elif event_prob <= xg['正面事件发生几率'] + xg['负面事件发生几率']:  # 落在负面事件范围
                    sj = random.choice(events_negative)  # 随机选择一个负面事件
                    consecutive_positive = 0  # 连续正面事件计数清零
                    if autumn and sj == '被变异树的叶子砸伤':  # 秋季触发变异树叶子事件
                        sj = '被变异树的叶子砸伤'  # 替换为变异树叶子事件
                    elif not autumn and sj == '被变异树的叶子砸伤':  # 非秋季时移除该事件
                        sj = random.choice(events_negative)  # 重新选择一个负面事件
                    if winter and sj == '极端寒冷':  # 冬季触发极端寒冷事件
                        sj = '极端寒冷'  # 替换为极端寒冷事件
                    elif not winter and sj == '极端寒冷':  # 非冬季时移除该事件
                        sj = random.choice(events_negative)  # 重新选择一个负面事件
                    if summer and sj == '中暑':  # 夏季触发中暑事件
                        sj = '中暑'  # 替换为中暑事件
                    elif not summer and sj == '中暑':  # 非夏季时概率移除中暑事件
                        num = random.randint(1, 3)  # 生成 1-3 的随机数
                        if num != 1:  # 2/3 概率移除中暑事件
                            sj = random.choice(events_negative)  # 重新选择一个负面事件
                        else:  # 1/3 概率保留中暑事件
                            sj = '中暑'  # 保留中暑事件
                else:  # 否则视为无事发生
                    sj = '无事发生'  # 设置事件为无事
                    consecutive_positive = 0  # 连续计数清零
                
                if sj != '无事发生':  # 如果触发了具体事件
                    no(0)  # 清屏但不等待
                    print(f"{ORANGE}触发事件：{sj}{RESET}")  # 打印事件名称
                    print(f"{events_Speech[sj]}")  # 打印事件描述文本
                    # -------------------------- 事件效果处理 --------------------------
                    # 正面事件处理分支
                    if sj == '发现食物':
                        hunger = min(6, hunger + 1)  # 饥饿恢复但不超过上限 6
                    elif sj == '找到干净的水源':
                        thirst = min(6, thirst + 1)  # 口渴恢复但不超过上限 6
                    elif sj == '遇到友善的幸存者':
                        items['罐头']['拥有数量'] += 1  # 获得一个罐头
                    elif sj == '找到医疗包':
                        health = min(10, health + 2)  # 健康值恢复但不超过 10
                        items['急救包']['拥有数量'] += 1  # 增加急救包
                    elif sj == '发现道具':
                        common_items = ['绷带', '火柴盒', '电池', '绳子']  # 常用道具列表
                        target_item = random.choice(common_items)  # 随机选取一件常用道具
                        items[target_item]['拥有数量'] += 1  # 增加所选道具数量
                        print(f"{GREEN}获得：{target_item}×1{RESET}")  # 输出获得提示
                    elif sj == '外面有动静':
                        choice = input(f"{ORANGE}选择：{RESET}\n1. 悄悄查看\n2. 原地隐藏\n选择: ")  # 提示玩家选择处理方式
                        if choice == '1':  # 悄悄查看分支
                            if random.randint(1, 2) == 1:  # 50% 发现遗弃背包
                                print(f"{GREEN}发现一个遗弃背包，获得罐头×1、水瓶×2！{RESET}")  # 成功提示
                                items['罐头']['拥有数量'] += 1
                                items['水瓶']['拥有数量'] += 2
                            else:  # 被野狗咬伤分支
                                print(f"{RED}突然冲出一只野狗，你被咬伤！健康-3，获得【受伤】状态！{RESET}")
                                health -= 3
                                status['受伤'] = True
                        else:  # 原地隐藏分支
                            print(f"{GREEN}你屏住呼吸，动静逐渐消失，安全返回！{RESET}")  # 成功隐藏提示
                            xg['正面事件发生几率'] = min(100, xg['正面事件发生几率'] + 3)  # 小幅提升正面事件概率
                    elif sj == '天气转好':
                        xg['正面事件发生几率'] = min(100, xg['正面事件发生几率'] + 5)  # 增加正面事件概率
                    elif sj == '发现补给箱':
                        items['罐头']['拥有数量'] += 2  # 获得两个罐头
                        items['水瓶']['拥有数量'] += 2  # 获得两个水瓶
                    elif sj == '遇到救援队伍':
                        items['罐头']['拥有数量'] += 1  # 获得一个罐头
                        items['水瓶']['拥有数量'] += 1  # 获得一个水瓶
                    elif sj == '发现物资箱':
                        all_items = list(items.keys())  # 列出所有道具键名
                        for _ in range(2):  # 随机获得两件道具
                            target_item = random.choice(all_items)
                            items[target_item]['拥有数量'] += 1
                            print(f"{GREEN}获得：{target_item}×1{RESET}")  # 打印获得提示
                    elif sj == '发现猫咪':
                        items['猫咪']['拥有数量'] += 1  # 增加猫咪道具数量
                    elif sj == '发现电脑':
                        items['电脑']['拥有数量'] += 1  # 增加电脑道具数量
                    elif sj == '春暖花开':
                        xg['正面事件发生几率'] = min(100, xg['正面事件发生几率'] + 5)  # 春季正面事件概率
                    elif sj == '找到商店':
                        items['罐头']['拥有数量'] += 5  # 增加5个罐头
                        items['水瓶']['拥有数量'] += 5  # 增加5个水瓶
                    elif sj == '发现受伤幸存者':
                        items['罐头']['拥有数量'] += 2  # 获得2个罐头作为感谢
                        health = min(10, health - 0.5)  # 救助过程消耗体力，健康值略降
                    elif sj == '没有遇到丧尸':
                        health = min(10, health + 1)  # 健康值恢复1点

                    # 负面事件处理分支
                    elif sj == '遭遇野兽攻击':
                        health = max(0, health - 2)  # 健康值减少2点（不低于0）
                        status['受伤'] = True  # 标记受伤状态
                    elif sj == '食物中毒':
                        health = max(0, health - 1)  # 健康值减少1点
                        status['生病'] = True  # 标记生病状态
                    elif sj == '遇到敌对幸存者':
                        items['罐头']['拥有数量'] = max(0, items['罐头']['拥有数量'] - 1)  # 减少1个罐头
                        items['水瓶']['拥有数量'] = max(0, items['水瓶']['拥有数量'] - 1)  # 减少1个水瓶
                    elif sj == '受伤感染':
                        health = max(0, health - 2)  # 健康值减少2点
                        status['生病'] = True  # 同时标记生病和受伤状态
                        status['受伤'] = True
                    elif sj == '道具损坏':
                        # 排除关键道具（猫咪、电脑），随机选择可损坏道具
                        breakable_items = [item for item in items if item not in ['猫咪', '电脑'] and items[item]['拥有数量'] > 0]
                        if breakable_items:  # 若有可损坏道具
                            broken_item = random.choice(breakable_items)
                            items[broken_item]['拥有数量'] -= 1  # 数量减1
                            print(f"{RED}{broken_item}在使用中损坏了！{RESET}")
                        else:
                            print(f"{ORANGE}你没有可损坏的道具，侥幸躲过一劫。{RESET}")
                    elif sj == '恶劣天气来袭':
                        xg['负面事件发生几率'] = min(100, xg['负面事件发生几率'] + 5)  # 增加负面事件概率
                    elif sj == '迷路了':
                        hunger = max(0, hunger - 0.5)  # 饥饿值减少0.5
                        xg['正面事件发生几率'] = max(0, xg['正面事件发生几率'] - 5)  # 降低正面事件概率
                    elif sj == '水源被污染':
                        thirst = max(0, thirst - 0.5)  # 口渴值减少0.5
                    elif sj == '军方来到':
                        items['罐头']['拥有数量'] += 3  # 获得3个罐头
                        items['水瓶']['拥有数量'] += 3  # 获得3个水瓶
                        military_visited = True  # 标记军方已到访（用于触发结局）
                    elif sj == '建筑物倒塌':
                        health = max(0, health - 3)  # 健康值减少3点
                        status['受伤'] = True  # 标记受伤状态
                    elif sj == '极端寒冷':
                        health = max(0, health - 1)  # 健康值减少1点
                        hunger = max(0, hunger - 1)  # 饥饿值减少1点
                        thirst = max(0, thirst - 1)  # 口渴值减少1点
                    elif sj == '中暑':
                        health = max(0, health - 1)  # 健康值减少1点
                        thirst = max(0, thirst - 1)  # 口渴值减少1点
                    elif sj == '被变异树的叶子砸伤':
                        health = max(0, health - 2)  # 健康值减少2点
                        status['受伤'] = True  # 标记受伤状态
                    elif sj == '踩到陷阱':
                        health = max(0, health - 4)  # 健康值减少4点
                        status['受伤'] = True  # 标记受伤状态
                    elif sj == '遇到小型尸群':
                        status['受伤'] = True  # 标记受伤状态
                        health = max(0, health - 1)  # 额外减少1点健康值
                    elif sj == '遇到中型尸群':
                        status['受伤'] = True  # 标记受伤状态
                        health = max(0, health - 2)  # 健康值减少2点
                    elif sj == '遇到大型尸群':
                        status['受伤'] = True  # 标记受伤状态
                        health = max(0, health - 4)  # 健康值减少4点

                    no(1)  # 等待用户确认事件结果
                else:
                    print(f"{GREEN}一整天平安无事，你收集了一些基础物资（罐头×1，水瓶+1）。{RESET}")  # 无事件时基础收获提示
                    items['罐头']['拥有数量'] += 1  # 增加基础罐头
                    items['水瓶']['拥有数量'] += 1  # 增加基础水瓶
                    no(1)  # 等待用户确认
                break  # 搜寻后结束当天，跳出每日行动循环
            # 2. 休息恢复逻辑
            elif action == "2":
                print(f"{GREEN}你回到营地休息，恢复体力...{RESET}")  # 休息提示
                health = min(10, health + 1)  # 恢复健康但不超过上限
                hunger -= 0.5  # 休息消耗饥饿值
                thirst -= 0.5  # 休息消耗口渴值
                
                if random.randint(1, 100) <= 30:  # 30% 概率有额外恢复效果
                    if status["生病"] and random.randint(1, 2) == 1:  # 生病有一半几率好转
                        status["生病"] = False  # 清除生病状态
                        print(f"{GREEN}你的病在休息后好转了！{RESET}")  # 提示病情好转
                    if status["受伤"] and random.randint(1, 2) == 1:  # 受伤有一半几率愈合
                        status["受伤"] = False  # 清除受伤状态
                        print(f"{GREEN}你的伤口在休息后愈合了！{RESET}")  # 提示愈合
                no(1)  # 等待确认
                break  # 休息后结束当天
            
            # 3. 使用道具逻辑
            elif action == "3":
                print(f"\n{GREEN}可用道具:{RESET}")  # 输出可用道具标题
                usable_items = []  # 用于存放可用道具的列表及索引
                num = 0  #用于记录前面的索引
                for i, (item_name, item_data) in enumerate(items.items()):  # 遍历道具并列出可用项
                    if item_data["拥有数量"] > 0 and item_name not in ['猫咪']:  # 排除猫咪（不可消耗）
                        num += 1  #增加索引
                        usable_items.append((num, item_name, item_data))  # 添加索引与道具信息
                        print(f"{num}. {item_name}×{item_data['拥有数量']}")  # 打印道具选项
                
                if not usable_items:  # 如果没有可用道具
                    print(f"{RED}无可用道具！{RESET}")  # 提示无道具
                    no(1)  # 等待确认
                    continue  # 回到每日行动选择循环
                
                try:
                    choice = int(input(f"{ORANGE}选择道具：{RESET}")) - 1  # 读取玩家输入并转换为索引
                    if 0 <= choice < len(usable_items):  # 验证选择范围
                        idx, item_name, item_data = usable_items[choice]  # 取对应道具信息
                        items[item_name]['拥有数量'] -= 1  # 使用后道具数量减一
                        print(f"{GREEN}使用了：{item_name}{RESET}")  # 提示已使用道具
                        
                        # 各道具具体效果实现
                        if item_name == '罐头':
                            hunger = min(6, hunger + 2)  # 罐头恢复饥饿但不超过上限 6
                            print(f"{ORANGE}饥饿值恢复2点！{RESET}")  # 提示恢复
                        elif item_name == '水瓶':
                            thirst = min(6, thirst + 2)  # 水瓶恢复口渴值但不超过上限 6
                            print(f"{BLUE}口渴值恢复2点！{RESET}")  # 提示恢复
                        elif item_name == '绷带':
                            if status["受伤"]:  # 绷带用于治疗受伤状态
                                status["受伤"] = False  # 清除受伤状态
                                print(f"{GREEN}受伤状态恢复！{RESET}")  # 提示恢复
                            else:
                                print(f"{ORANGE}你没有受伤，无需使用绷带！{RESET}")  # 没有受伤的提示
                        elif item_name == '急救包':
                            health = min(10, health + 3)  # 急救包恢复健康值
                            status["生病"] = False  # 清除生病状态
                            status["受伤"] = False  # 清除受伤状态
                            print(f"{GREEN}健康值恢复3点，所有负面状态清除！{RESET}")  # 提示全部恢复
                        elif item_name == '手电筒':
                            xg['正面事件发生几率'] = min(100, xg['正面事件发生几率'] + 5)  # 增加正面事件概率
                            print(f"{BLUE}正面事件概率+5%！{RESET}")  # 提示效果
                        elif item_name == '电池':
                            if items['手电筒']['拥有数量'] > 0:  # 如果有手电筒则电池生效
                                xg['正面事件发生几率'] = min(100, xg['正面事件发生几率'] + 3)  # 小幅增加概率
                                print(f"{BLUE}手电筒续航增加，正面事件概率+3%！{RESET}")  # 提示效果
                            else:
                                print(f"{ORANGE}你没有手电筒，电池无用！{RESET}")  # 没有手电筒时提示无效
                        elif item_name == '刀具':
                            xg['负面事件发生几率'] = max(0, xg['负面事件发生几率'] - 5)  # 降低负面事件概率
                            print(f"{RED}负面事件概率-5%！{RESET}")  # 提示效果
                        elif item_name == '绳子':
                            print(f"{GREEN}你用绳子加固了营地，安全感提升！{RESET}")  # 绳子仅给出描述性效果
                        elif item_name == '火柴盒':
                            if winter:  # 冬季与非冬季效果不同
                                health = min(10, health + 1)  # 冬季生火增加健康
                                print(f"{BLUE}生火取暖，健康值+1！{RESET}")  # 提示效果
                            else:
                                hunger = min(6, hunger + 1)  # 非冬季生火可烹饪恢复饥饿
                                print(f"{ORANGE}生火烹饪，饥饿值+1！{RESET}")  # 提示效果
                        elif item_name == '帐篷':
                            xg['生病发生几率'] = max(0, xg['生病发生几率'] - 10)  # 帐篷降低生病几率
                            print(f"{GREEN}生病概率-10%！{RESET}")  # 提示效果
                        elif item_name == '物资箱':
                            all_items = list(items.keys())  # 打开物资箱获得三件随机道具
                            for _ in range(3):
                                target_item = random.choice(all_items)
                                items[target_item]['拥有数量'] += 1
                                print(f"{GREEN}获得：{target_item}×1{RESET}")  # 打印获得信息
                        elif item_name == '电脑':
                            use_pc = input(f"{BLUE}使用电脑做什么？{RESET}（1.发送求救信号（不消耗道具） 2.寻找物资地点）: ")  # 电脑操作选项
                            if use_pc == "1":  # 发送求救信号分支
                                print(f"{BLUE}你打开电脑，尝试发送求救信号...{RESET}")  # 提示行为
                                time.sleep(2)  # 等待模拟发送时间
                                if random.randint(1, 100) == 1:  # 1% 成功几率触发电子救援
                                    no(0)  # 清屏
                                    print(f"{GREEN}===== 电子救援结局达成！====={RESET}")  # 打印结局标题
                                    print(f"{GREEN}求救信号被附近的科考队接收，你被成功救援！{RESET}")  # 结局描述
                                    achievements = check_achievement(achievements, "数字救援")  # 解锁成就
                                    no(1)  # 等待用户查看
                                    return  # 结束游戏
                                else:
                                    print(f"{GREEN}未收到回应……{RESET}")  # 未收到回应的提示
                                    no(1)  # 等待用户查看
                            elif use_pc == "2":  # 使用电脑寻找物资分支
                                print(f"{ORANGE}你决定用电脑寻找物资……{RESET}")  # 描述
                                time.sleep(2)  # 暂停模拟搜索
                                print(f"{GREEN}找到了一个隐藏的物资仓库，获得罐头+4、水瓶+3！{RESET}")  # 搜索成功提示
                                items["罐头"]["拥有数量"] += 4  # 增加罐头
                                items["水瓶"]["拥有数量"] += 3  # 增加水瓶
                                no(1)  # 等待用户查看
                    else:
                        print(f"{RED}无效选择！{RESET}")  # 选择超出范围的提示
                except:  # 捕获输入转换或索引错误
                    print(f"{RED}无效输入！{RESET}")  # 无效输入提示
                no(1)  # 使用道具流程结束后等待
            
            # 4. 保存游戏选项
            elif action == "4":
                save_data = {  # 构建保存用的数据字典
                    "day": day, "hunger": hunger, "thirst": thirst, "health": health,
                    "status": status, "xg": xg, "items": items,
                    "difficulty": name, "character": pep,
                    "military_visited": military_visited,
                    "consecutive_positive": consecutive_positive,
                    "has_asked_survival_end": has_asked_survival_end
                }
                save_game(save_data)  # 调用保存函数保存进度
            
            # 5. 退出游戏选项
            elif action == "5":
                confirm = input(f"{RED}确定退出游戏吗？（进度会丢失）{RESET}（y/n）: ")  # 确认退出提示
                if confirm.lower() == "y":  # 确认退出则结束程序
                    print(f"{WHITE}感谢游玩！{RESET}")  # 致谢提示
                    time.sleep(2)  # 等待后退出
                    exit()  # 退出程序
                else:
                    print(f"{GREEN}取消退出，继续游戏！{RESET}")  # 取消退出提示
                    no(1)  # 等待并返回每日选择
            
            else:  # 无效输入处理
                print(f"{RED}无效选择，请输入1-5！{RESET}")  # 提示范围内输入
                no(1)  # 等待并重试
        
        # -------------------------- 每日状态衰减 --------------------------
        hunger -= 1  # 每天饥饿值自然减少 1
        thirst -= 1  # 每天口渴值自然减少 1
        
        if status["生病"]:  # 生病状态额外影响
            health -= 0.5; hunger -= 0.5; thirst -= 0.5  # 生病每日扣血并加速饥渴下降
        if status["受伤"]:  # 受伤状态每日扣血
            health -= 0.3  # 受伤每日扣血 0.3
        
        # 限制数值下界并保留一位小数
        hunger = max(0, round(hunger, 1))  # 饥饿下限为 0，保留一位小数
        thirst = max(0, round(thirst, 1))  # 口渴下限为 0，保留一位小数
        health = max(0, round(health, 1))  # 健康下限为 0，保留一位小数

        # 极度饥饿/口渴判定与处理：若到 0 切换到极度状态并设置保持天数倒计时
        if hunger == 0 and not status["极度饥饿"]:
            status["极度饥饿"] = True  # 进入极度饥饿状态
            hunger = xg['饥饿保持天数'] -1  # 将饥饿设置为保持天数减一作为倒计时
        if thirst == 0 and not status["极度口渴"]:
            status["极度口渴"] = True  # 进入极度口渴状态
            thirst = xg['口渴保持天数'] -1  # 将口渴设置为保持天数减一作为倒计时

        # 恢复正常检查：当计时超过保持天数时恢复并重置为上限 6
        if hunger > xg["饥饿保持天数"] and status["极度饥饿"] :
            status["极度饥饿"] = False  # 退出极度饥饿状态
            hunger = 6  # 重置饥饿为上限 6
        if thirst > xg["口渴保持天数"] and status["极度口渴"] :
            status["极度口渴"] = False  # 退出极度口渴状态
            thirst = 6  # 重置口渴为上限 6
        
        # -------------------------- 死亡检查 --------------------------
        if health <= 0:  # 健康降为 0 或更低则死亡
            no(0)  # 清屏
            print(f"{RED}===== 游戏结束 ====={RESET}")  # 打印游戏结束标题
            print(f"{RED}你因伤势过重，在第{day}天倒下了...{RESET}")  # 死亡描述
            print(f"{ORANGE}最终生存天数：{day}天{RESET}")  # 打印生存天数
            no(1)  # 等待用户
            return  # 返回结束函数
        if hunger <= 0 and status["极度饥饿"]:  # 极度饥饿且饥饿值为 0 则死亡
            no(0)  # 清屏
            print(f"{RED}===== 游戏结束 ====={RESET}")  # 打印游戏结束标题
            print(f"{RED}你因极度饥饿，在第{day}天倒下了...{RESET}")  # 死亡描述
            print(f"{ORANGE}最终生存天数：{day}天{RESET}")  # 打印生存天数
            no(1)  # 等待用户
            return  # 返回结束函数
        if thirst <= 0 and status["极度口渴"]:  # 极度口渴且口渴值为 0 则死亡
            no(0)  # 清屏
            print(f"{RED}===== 游戏结束 ====={RESET}")  # 打印游戏结束标题
            print(f"{RED}你因极度口渴，在第{day}天倒下了...{RESET}")  # 死亡描述
            print(f"{ORANGE}最终生存天数：{day}天{RESET}")  # 打印生存天数
            no(1)  # 等待用户
            return  # 返回结束函数
        
        # -------------------------- 随机生病检查 --------------------------
        if not status["生病"] and random.randint(1, 100) <= xg['生病发生几率']:  # 非生病状态下按概率生病
            status["生病"] = True  # 设置生病状态
            print(f"{RED}你感觉身体不适，患上了疾病！{RESET}")  # 提示生病
            no(1)  # 等待查看
        
        day += 1  # 每个循环结束后天数增加 1，进入下一天