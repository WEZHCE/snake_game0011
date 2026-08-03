"""
====================================================================
   🐍 贪吃蛇 - Snake Game  (v7.8 优化修复版)
   修复: 菜单按钮悬停仅按键时生效 | 对战模式可反向穿自身
        | 对战模式游戏时长未统计 | 食物生成满盘死循环
        | 重力皮肤误替换主食物 | 皮肤确认弹窗未实现
   优化: 遮罩表面缓存 | 事件处理结构优化 | 代码健壮性提升
   开发者: WEZHCE | B站: 1309420497 | GitHub: https://github.com/WEZHCE
====================================================================
"""
import sys
import os

try:
    import pygame
    from pygame.locals import *
except ImportError:
    print("="*60)
    print("  [错误] 缺少 pygame 库！请运行: pip install pygame")
    print("="*60)
    input("按 Enter 退出...")
    sys.exit(1)

import json
import random
import math
import colorsys
from collections import deque

def main():
    try:
        _run_game()
    except Exception as e:
        print("="*60)
        print(f"  [错误] {e}")
        import traceback
        traceback.print_exc()
        input("\n按 Enter 退出...")
        sys.exit(1)

def _run_game():
    pygame.init()
    pygame.mixer.init()
    pygame.key.set_repeat(200, 50)

    WINDOW_WIDTH = 880
    WINDOW_HEIGHT = 720
    GRID_SIZE = 20
    CELL_SIZE = 26
    GRID_PX = GRID_SIZE * CELL_SIZE
    GRID_X = (WINDOW_WIDTH - GRID_PX) // 2
    GRID_Y = 78
    TOP_BAR_HEIGHT = 72
    FPS = 60
    SAVE_FILE = "snake_save.json"
    SAVE_FILE_BACKUP = "snake_save_backup.json"
    SCORE_SCALE = 10

    def fmt_score(val):
        return f"{val / SCORE_SCALE:.1f}"

    # ==================================================================
    #  语言系统
    # ==================================================================
    current_lang = "zh"
    LANG = {
        "zh": {
            "title": "贪  吃  蛇",
            "subtitle": "经 典 重 现  ·  挑 战 高 分",
            "speed": "移动速度",
            "mode_prefix": "模式: ",
            "mode_endless": "无限",
            "mode_timed": "限时",
            "edge_slide": "边缘: 滑动",
            "edge_death": "边缘: 死亡",
            "edge_wrap": "边缘: 穿墙",
            "start": "开始游戏",
            "vs_mode": "人机对战",
            "shop": "积分商店",
            "skin_shop": "皮肤商店",
            "achievements": "成就",
            "skin_label": "皮肤",
            "help": "游戏说明",
            "stats": "统计信息",
            "update": "更新说明",
            "dev": "开发者",
            "music": "音乐控制",
            "music_title": "音 乐 控 制",
            "effects_on": "特效: 开",
            "effects_off": "特效: 关",
            "score": "得分",
            "multiplier": "倍率",
            "mode_label": "模式",
            "mode_endless": "无限",
            "mode_timed": "限时",
            "time_label": "时间",
            "food_label": "食物",
            "high_label": "最高纪录",
            "pause": "暂停",
            "paused_label": "已 暂 停",
            "resume": "继续",
            "end": "结束",
            "game_over": "游 戏 结 束",
            "score_label": "本局得分",
            "max_endless": "无限最高",
            "max_timed": "限时最高",
            "total_score": "累计总分",
            "new_record": "新 纪 录 !",
            "restart": "再来一局",
            "back_menu": "返回菜单",
            "score_earned": "本局累计总分",
            "real_time": "实时分数",
            "current": "本局",
            "track_label": "曲目",
            "volume": "音量",
            "no_music": "无音乐",
            "playing_status": "播放中",
            "paused_status": "已暂停",
            "current_playing": "当前播放",
            "status": "状态",
            "track_list": "曲目列表",
            "prev": "<<",
            "play": "播放",
            "pause_btn": "暂停",
            "next": ">>",
            "shop_title": "积 分 商 店",
            "exchange_rate": "兑换比例: 2 累计总分 = 1 已兑换积分",
            "redeemable": "可兑换积分",
            "redeemed": "已兑换积分",
            "total": "累计总分",
            "current_redeemable": "当前可兑换: {} 积分",
            "history_total": "历史总积分: {}",
            "exchange_1": "兑 换 1 积 分",
            "exchange_10": "兑换 10",
            "exchange_50": "兑换 50",
            "exchange_all": "兑换全部",
            "exchange_success": "兑换成功! 用{}可兑换积分换得{}已兑换积分",
            "exchange_fail": "可兑换积分不足{}",
            "click_close": "点击外部关闭",
            "scroll_close": "滚轮滚动  |  点击外部关闭",
            "stats_title": "详 细 统 计 数 据",
            "games_played": "总游戏局数",
            "play_time": "总游戏时长",
            "avg_score": "平均每局得分",
            "mode_title": "各模式最高分",
            "help_title": "游 戏 说 明",
            "dev_title": "开 发 者 信 息",
            "update_title": "更 新 说 明",
            "skin_title": "皮 肤 商 店",
            "skin_hint": "左键点击购买/切换 | 滚轮滚动 | 点击外部关闭",
            "equipped": "使用中",
            "owned": "已拥有",
            "price_pts": "{} 积分",
            "confirm_buy": "确认购买 {}?",
            "cost_pts": "消耗 {} 可兑换积分",
            "confirm_yes": "确认",
            "confirm_no": "取消",
            "skin_click_equip": "点击切换",
            "skin_click_buy": "点击购买",
            "unlock_time": "游戏时长≥3分钟解锁",
            "vs_info": "双蛇对战",
            "vs_player": "玩家",
            "vs_ai": "AI",
            "vs_win": "玩家获胜!",
            "vs_lose": "AI 获胜!",
            "vs_draw": "平局!",
            "vs_food": "食物数",
            "diff_select": "选择 AI 难度",
            "lang_select": "语言选择",
            "theme": "主题",
            "rank_bronze": "青铜",
            "rank_silver": "白银",
            "rank_gold": "黄金",
            "rank_platinum": "铂金",
            "rank_diamond": "钻石",
            "rank_master": "大师",
            "rank_title": "段 位",
            "rank_xp": "经验值",
            "rank_level": "等级",
            "rank_next_reward": "下级奖励",
            "rank_xp_earned": "+{} XP",
            "rank_level_up": "升级! Lv.{}",
            "rank_progress": "{}/{} XP",
            "rank_streak": "连胜 x{}",
            "rank_bonus": "+{}% 连胜加成",
            "daily_challenge": "每日挑战",
            "daily_modifier": "今日规则",
            "daily_best": "最佳成绩",
            "daily_play": "挑 战",
            "daily_result": "挑战完成",
            "daily_xp_bonus": "挑战奖励 +{} XP",
            "daily_rewards": "奖励说明",
            "daily_reward_participate": "参与奖励 +20 XP",
            "daily_reward_score": "得分奖励 +分数÷10 XP",
            "daily_reward_modifier": "高倍率挑战额外奖励",
            "daily_speed_storm": "极速风暴",
            "daily_speed_storm_desc": "速度强制地狱档，得分x2.5",
            "daily_shrink": "瘦身蛇",
            "daily_shrink_desc": "每10次移动自动缩短1节",
            "daily_maze": "墙体迷宫",
            "daily_maze_desc": "地图内随机8个障碍物",
            "daily_rush": "极速冲刺",
            "daily_rush_desc": "限时90秒，得分x2",
            "daily_quad_food": "四倍食物",
            "daily_quad_food_desc": "同时存在4个食物",
            "daily_skin_lock": "皮肤锁定",
            "daily_skin_lock_desc": "随机锁定皮肤",
            "daily_wrap_random": "随机传送",
            "daily_wrap_random_desc": "撞墙后随机出现",
            "daily_crit_chance": "暴击机制",
            "daily_crit_chance_desc": "20%暴击x5/10%落空",
            "help_content": [
                "[ 操作说明 ]",
                "  方向键 / WASD    控制蛇的移动方向",
                "  ESC              返回菜单",
                "  空格键            暂停/继续",
                "",
                "[ 游戏规则 ]",
                "  吃到食物增加长度与分数",
                "  边缘模式可在菜单切换",
                "  撞到自身则游戏结束",
                "",
                "[ 双模式 ]",
                "  无限模式 - 经典无限游玩",
                "  限时模式 - 3分钟限时挑战",
                "",
                "[ 得分倍率 ]",
                "  基础倍率: 简单×0.8  普通×1.0  困难×1.5  地狱×2.0",
                "  翻倍机制: 每吃10个食物，得分翻倍",
                "  皮肤加成: 贪吃蛇×1.2  熵减蛇×3(操作反向)",
                "  全局特效关闭时只保留外观, 所有加成失效",
                "",
                "[ 人机对战 ]",
                "  主界面点击「人机对战」",
                "  选择AI难度后开始对战",
                "  对战结果计入总得分和局数",
            ],
            "dev_content": [
                "[ 开发者信息 ]",
                "",
                "  作者    :  WEZHCE",
                "  邮箱    :  wezhce055@outlook.com",
                "  B站 UID :  1309420497",
                "  GitHub  :  https://github.com/WEZHCE",
                "",
                "  版本    :  7.10 (段位每日版)",
                "  引擎    :  Python 3 + Pygame",
            ],
            "update_content": [
                "═══════  v7.10 版本更新 ═══════",
                "",
                "  [新增] 段位/等级系统：XP、升级、段位、连胜加成",
                "  [新增] 6个段位：青铜/白银/黄金/铂金/钻石/大师",
                "  [新增] 5款段位专属皮肤（Lv.10~50解锁）",
                "  [新增] 段位面板：等级、XP进度、连胜、里程碑",
                "  [新增] 升级通知弹窗",
                "  [新增] 每日挑战系统：8种Modifier每日轮换",
                "  [新增] 每日挑战信息弹窗与结算界面",
                "  [新增] 成就积分奖励（按难度5~50pts）",
                "  [修复] 皮肤商店滚动条拖动算法优化",
                "  [修复] 皮肤商店新增皮肤解锁条件显示",
                "  [修复] 所有弹窗滚动条支持鼠标拖拽",
                "",
                "═══════  v7.9 版本更新 ═══════",
                "",
                "  [新增] 日语语言支持（中/英/日三语切换）",
                "  [新增] 主题系统：6套配色主题可切换",
                "  [新增] 语言选择弹窗，切换更便捷",
                "  [新增] 主题选择弹窗，实时预览配色",
                "  [新增] 按钮颜色随主题自动切换",
                "  [新增] 文字自动对比度适配（深浅背景自适应）",
                "  [修复] 难度选择弹窗点击外部可关闭",
                "  [修复] 语言切换时积分商店按钮文本同步更新",
                "  [修复] 浅色主题下按钮文字自动适配深色",
                "  [修复] 主题弹窗布局优化，动态高度防溢出",
                "  [修复] 日语模式音乐弹窗和弹窗标题翻译补全",
                "  [修复] 音乐列表当前曲目标记改为通用符号",
                "  [新增] 成就系统：22个成就（含6个隐藏彩蛋）",
                "  [新增] 成就解锁通知弹窗",
                "  [新增] 成就查看面板",
                "  [优化] 整体UI界面美化，配色更专业",
                "",
                "  ※ 日语翻译部分由机器翻译完成",
                "",
                "═══════  v7.8 版本更新 ═══════",
                "",
                "  [修复] 菜单按钮悬停仅按键时生效的问题",
                "  [修复] 对战模式玩家可反向移动的问题",
                "  [修复] 对战模式游戏时长未统计的问题",
                "  [修复] 食物生成满盘时死循环的问题",
                "  [修复] 重力皮肤误替换主食物的问题",
                "  [新增] 皮肤购买确认弹窗",
                "  [优化] 遮罩表面缓存，减少每帧创建开销",
                "  [新增] 边缘模式三态切换：死亡/滑动/穿墙",
                "  [修复] 边缘滑动改为真正的沿墙滑行机制",
                "  [修复] 英文模式按钮文本缺失和崩溃问题",
                "  [修复] 所有按钮悬停文本随语言切换",
                "  [修复] 音乐弹窗音量条与文本重叠",
                "  [修复] 积分商店按钮溢出问题",
                "  [优化] 皮肤商店UI重新设计，无重叠遮盖",
                "",
                "═══════  v7.7 版本更新 ═══════",
                "",
                "  [修复] 普通模式无法移动、暂停、结束",
                "  [修复] 人机对战边缘滑动死亡问题",
                "  [修复] 边缘滑动改为穿墙环绕",
                "",
                "═══════  v7.6 版本更新 ═══════",
                "",
                "  [调整] 虫洞核心蛇降至120积分",
                "  [新增] 得分倍率说明整合至游戏帮助",
                "  [修复] 人机对战计入总得分与局数",
                "",
                "═══════  v7.5 版本更新 ═══════",
                "",
                "  [修复] 重力蛇吸附/烈艳红速度/虫洞传送",
                "  [新增] AI三级难度选择",
                "",
                "═══════  v7.4 版本更新 ═══════",
                "",
                "  [新增] 人机对战模式 (BFS AI)",
                "",
                "═══════  v7.3 版本更新 ═══════",
                "",
                "  [修复] 简单模式不得分",
                "  [新增] 得分一位小数显示",
                "",
                "═══════  v7.2 版本更新 ═══════",
                "",
                "  [修复] 烈艳红自动解锁",
                "  [修复] 得分倍率失效",
                "  [新增] 简单模式×0.8",
                "",
                "═══════  v7.1 版本更新 ═══════",
                "",
                "  [修复] 皮肤商店购买功能",
                "  [修复] 存档文件权限问题",
                "",
                "═══════  v7.0 版本更新 ═══════",
                "",
                "  [新增] 11款皮肤系统",
                "  [新增] 全局特效开关",
                "  [调整] 困难模式×1.5, 地狱模式×2.0",
                "",
                "═══════  v6.0 版本更新 ═══════",
                "",
                "  [新增] 英文语言支持",
                "  [新增] 死亡闪白特效",
                "  [优化] 结算界面重设计",
                "",
                "═══════  v5.9 版本更新 ═══════",
                "",
                "  [新增] 积分商店系统",
                "",
                "═══════  v5.8 版本更新 ═══════",
                "",
                "  [新增] 独立音乐控制窗口",
                "",
                "═══════  v5.7 版本更新 ═══════",
                "",
                "  [修复] PyInstaller 打包音乐丢失",
                "",
                "═══════  v5.6 版本更新 ═══════",
                "",
                "  [修复] 音乐控制文字按钮不重叠",
                "",
                "═══════  v5.5 版本更新 ═══════",
                "",
                "  [修复] 音乐按钮放到右下角",
                "",
                "═══════  v5.4 版本更新 ═══════",
                "",
                "  [修复] 音乐文件损坏自动跳过",
                "",
                "═══════  v5.3 版本更新 ═══════",
                "",
                "  [更新] 开发者信息",
                "",
                "═══════  v5.2 版本更新 ═══════",
                "",
                "  [新增] 背景音乐系统",
                "",
                "═══════  v5.1 版本更新 ═══════",
                "",
                "  [新增] 统计信息按钮",
                "",
                "═══════  v5.0 版本更新 ═══════",
                "",
                "  [调整] 移除账户系统",
                "",
                "═══════  v4.0 版本更新 ═══════",
                "",
                "  [新增] 双模式系统",
                "  [新增] 游戏内控制",
                "  [新增] 实时分数面板",
                "",
                "═══════  v3.0 版本更新 ═══════",
                "",
                "  [新增] 边缘碰撞模式切换",
                "  [新增] 分数翻倍机制",
            ],
        },
        "en": {
            "title": "S N A K E",
            "subtitle": "Classic Revival \u00b7 Challenge High Score",
            "speed": "Speed",
            "mode_prefix": "Mode: ",
            "mode_endless": "Endless",
            "mode_timed": "Timed",
            "edge_slide": "Edge: Slide",
            "edge_death": "Edge: Death",
            "edge_wrap": "Edge: Wrap",
            "start": "Start Game",
            "vs_mode": "VS AI",
            "shop": "Shop",
            "skin_shop": "Skins",
            "achievements": "Achievements",
            "skin_label": "Skin",
            "help": "Help",
            "stats": "Stats",
            "update": "Updates",
            "dev": "Dev",
            "music": "Music",
            "music_title": "M U S I C",
            "effects_on": "FX: ON",
            "effects_off": "FX: OFF",
            "score": "Score",
            "multiplier": "Multiplier",
            "mode_label": "Mode",
            "mode_endless": "Endless",
            "mode_timed": "Timed",
            "time_label": "Time",
            "food_label": "Food",
            "high_label": "Record",
            "pause": "Pause",
            "paused_label": "PAUSED",
            "resume": "Resume",
            "end": "End",
            "game_over": "G A M E   O V E R",
            "score_label": "Score",
            "max_endless": "Endless High",
            "max_timed": "Timed High",
            "total_score": "Total Score",
            "new_record": "NEW RECORD !",
            "restart": "Play Again",
            "back_menu": "Main Menu",
            "score_earned": "Total Points Earned",
            "shop_title": "P O I N T   S H O P",
            "exchange_rate": "Exchange: 2 Total Score = 1 Point",
            "redeemable": "Redeemable",
            "redeemed": "Redeemed",
            "total": "Total Score",
            "current_redeemable": "Redeemable: {} pts",
            "history_total": "Total Earned: {} pts",
            "exchange_1": "Exchange 1",
            "exchange_10": "Exchange 10",
            "exchange_50": "Exchange 50",
            "exchange_all": "Exchange All",
            "exchange_success": "Success! Used {} points to get {} redeemed",
            "exchange_fail": "Need at least {} redeemable points",
            "click_close": "Click outside",
            "scroll_close": "Scroll | Click outside",
            "skin_title": "S K I N   S H O P",
            "skin_hint": "Click to buy/equip | Scroll | Click outside",
            "equipped": "Equipped",
            "owned": "Owned",
            "price_pts": "{} pts",
            "confirm_buy": "Buy {}?",
            "cost_pts": "Cost: {} pts",
            "confirm_yes": "Yes",
            "confirm_no": "Cancel",
            "skin_click_equip": "Click to equip",
            "skin_click_buy": "Click to buy",
            "unlock_time": "Unlock: 3min playtime",
            "vs_player": "Player",
            "vs_ai": "AI",
            "vs_win": "Player Wins!",
            "vs_lose": "AI Wins!",
            "vs_draw": "Draw!",
            "vs_food": "Food",
            "diff_select": "Select AI Difficulty",
            "lang_select": "Language",
            "theme": "Theme",
            "rank_bronze": "Bronze",
            "rank_silver": "Silver",
            "rank_gold": "Gold",
            "rank_platinum": "Platinum",
            "rank_diamond": "Diamond",
            "rank_master": "Master",
            "rank_title": "RANK",
            "rank_xp": "XP",
            "rank_level": "Level",
            "rank_next_reward": "Next Reward",
            "rank_xp_earned": "+{} XP",
            "rank_level_up": "Level Up! Lv.{}",
            "rank_progress": "{}/{} XP",
            "rank_streak": "Streak x{}",
            "rank_bonus": "+{}% Streak",
            "daily_challenge": "Daily Challenge",
            "daily_modifier": "Today's Rule",
            "daily_best": "Best Score",
            "daily_play": "Challenge",
            "daily_result": "Challenge Done",
            "daily_xp_bonus": "Bonus +{} XP",
            "daily_rewards": "Rewards",
            "daily_reward_participate": "Participate +20 XP",
            "daily_reward_score": "Score +score/10 XP",
            "daily_reward_modifier": "High multiplier bonus",
            "daily_speed_storm": "Speed Storm",
            "daily_speed_storm_desc": "Hell speed, score x2.5",
            "daily_shrink": "Shrink",
            "daily_shrink_desc": "Auto shrink every 10 moves",
            "daily_maze": "Maze",
            "daily_maze_desc": "8 random obstacles",
            "daily_rush": "Rush",
            "daily_rush_desc": "90s limit, score x2",
            "daily_quad_food": "Quad Food",
            "daily_quad_food_desc": "4 foods at once",
            "daily_skin_lock": "Skin Lock",
            "daily_skin_lock_desc": "Random skin forced",
            "daily_wrap_random": "Random Warp",
            "daily_wrap_random_desc": "Appear randomly on wall hit",
            "daily_crit_chance": "Critical",
            "daily_crit_chance_desc": "20% crit x5 / 10% miss",
            "help_content": [
                "[ Controls ]",
                "  Arrow Keys / WASD    Move snake",
                "  ESC                  Back to menu",
                "  SPACE                Pause / Resume",
                "",
                "[ Rules ]",
                "  Eat food to grow and score",
                "  Edge mode switchable in menu",
                "  Hit yourself = game over",
                "",
                "[ Modes ]",
                "  Endless - classic infinite play",
                "  Timed   - 3-minute challenge",
                "",
                "[ Score Multiplier ]",
                "  Base: Easy×0.8 Normal×1.0 Hard×1.5 Hell×2.0",
                "  Double: every 10 foods, score x2",
                "  Skin bonus: Glutton×1.2 Entropy×3(reversed)",
                "  Disabled when FX is OFF",
                "",
                "[ VS AI ]",
                "  Click 'VS AI' on main menu",
                "  Choose difficulty to start",
                "  Results count to total score",
            ],
            "dev_content": [
                "[ Developer ]",
                "",
                "  Author  :  WEZHCE",
                "  Email   :  wezhce055@outlook.com",
                "  Bili UID:  1309420497",
                "  GitHub  :  https://github.com/WEZHCE",
                "",
                "  Version :  7.10 (Rank & Daily)",
                "  Engine  :  Python 3 + Pygame",
            ],
            "update_content": [
                "═══════  v7.10  ═══════",
                "",
                "  [New] Rank/Level system: XP, levels, ranks, streak bonus",
                "  [New] 6 ranks: Bronze/Silver/Gold/Platinum/Diamond/Master",
                "  [New] 5 rank-exclusive skins (Lv.10~50 unlock)",
                "  [New] Rank panel: level, XP bar, streak, milestones",
                "  [New] Level-up notification popup",
                "  [New] Daily Challenge: 8 modifiers rotate daily",
                "  [New] Daily challenge info and result screens",
                "  [New] Achievement point rewards (5~50pts by difficulty)",
                "  [Fix] Skin shop scrollbar drag algorithm improved",
                "  [Fix] Skin shop new skins unlock condition display",
                "  [Fix] All popup scrollbars support mouse drag",
                "",
                "═══════  v7.9  ═══════",
                "",
                "  [New] Japanese language support (zh/en/ja)",
                "  [New] Theme system: 6 color themes",
                "  [New] Language selection popup",
                "  [New] Theme selection popup with live preview",
                "  [New] Button colors adapt to theme",
                "  [New] Auto text contrast (light/dark adaptive)",
                "  [Fix] Difficulty popup close on outside click",
                "  [Fix] Shop button text sync on language switch",
                "  [Fix] Auto dark text on light theme buttons",
                "  [Fix] Theme popup layout fix, dynamic height",
                "  [Fix] Japanese mode music popup translations",
                "  [Fix] Music list marker changed to universal symbol",
                "  [Opt] Overall UI beautification, pro color schemes",
                "  [New] Achievement system: 22 achievements (6 secret)",
                "  [New] Achievement unlock notification popup",
                "  [New] Achievement viewing panel",
                "",
                "  ※ Japanese translations partially machine-translated",
                "",
                "═══════  v7.8  ═══════",
                "",
                "  [Fix] Menu buttons hover only on key press",
                "  [Fix] VS mode player can reverse into self",
                "  [Fix] VS mode play time not counted",
                "  [Fix] Food spawn infinite loop on full board",
                "  [Fix] Gravity skin wrongly replaces main food",
                "  [New] Skin purchase confirmation popup",
                "  [Opt] Overlay surface caching",
                "  [New] Edge mode 3-state: Death/Slide/Wrap",
                "  [Fix] Edge slide: real wall-sliding mechanic",
                "  [Fix] English mode missing text & crash fix",
                "  [Fix] All button text updates on language switch",
                "  [Fix] Music popup volume bar overlap",
                "  [Fix] Shop button overflow in English",
                "  [Opt] Skin shop UI redesign, no overlap",
                "",
                "═══════  v7.7  ═══════",
                "",
                "  [Fix] Normal mode move/pause/end missing",
                "  [Fix] VS mode edge slide death",
                "  [Fix] Pause/end button not working",
                "  [Fix] Edge slide changed to wall-wrap",
                "",
                "═══════  v7.6  ═══════",
                "",
                "  [Adj] Wormhole Core skin down to 120pts",
                "  [Adj] DeepSeek-Flash up to 500pts",
                "  [Fix] Second life: random position revive",
                "  [Fix] VS mode counts to total score",
                "  [Fix] Edge collision active in VS",
                "  [New] Score multiplier in Help",
                "  [Opt] Full update log history",
                "",
                "═══════  v7.5  ═══════",
                "",
                "  [Fix] Gravity attract / Red speed / Wormhole",
                "  [New] 3-level AI difficulty",
                "",
                "═══════  v7.4  ═══════",
                "",
                "  [New] VS AI mode (BFS AI)",
                "",
                "═══════  v7.3  ═══════",
                "",
                "  [Fix] Easy mode no score",
                "  [New] 1-decimal score display",
                "",
                "═══════  v7.2  ═══════",
                "",
                "  [Fix] Blazing Red auto-unlock",
                "  [Fix] Score multiplier broken",
                "  [New] Easy mode ×0.8",
                "",
                "═══════  v7.1  ═══════",
                "",
                "  [Fix] Skin shop purchase",
                "  [Fix] Save file permission",
                "",
                "═══════  v7.0  ═══════",
                "",
                "  [New] 11 skin system",
                "  [New] Global FX toggle",
                "  [Adj] Hard ×1.5, Hell ×2.0",
                "",
                "═══════  v6.0  ═══════",
                "",
                "  [New] English language",
                "  [New] Death flash effect",
                "  [Opt] Game over screen redesign",
                "",
                "═══════  v5.9  ═══════",
                "",
                "  [New] Point shop system",
                "",
                "═══════  v5.8  ═══════",
                "",
                "  [New] Music control window",
                "",
                "═══════  v5.7  ═══════",
                "",
                "  [Fix] PyInstaller music missing",
                "",
                "═══════  v5.6  ═══════",
                "",
                "  [Fix] Music button overlap",
                "",
                "═══════  v5.5  ═══════",
                "",
                "  [Fix] Music button to bottom-right",
                "",
                "═══════  v5.4  ═══════",
                "",
                "  [Fix] Skip corrupt music files",
                "",
                "═══════  v5.3  ═══════",
                "",
                "  [Upd] Developer info",
                "",
                "═══════  v5.2  ═══════",
                "",
                "  [New] Background music system",
                "",
                "═══════  v5.1  ═══════",
                "",
                "  [New] Stats button",
                "",
                "═══════  v5.0  ═══════",
                "",
                "  [Adj] Removed account system",
                "",
                "═══════  v4.0  ═══════",
                "",
                "  [New] Dual mode system",
                "  [New] In-game controls",
                "  [New] Real-time score panel",
                "",
                "═══════  v3.0  ═══════",
                "",
                "  [New] Edge collision toggle",
                "  [New] Score double mechanic",
            ],
        },
        "ja": {
            "title": "ス  ネ  イ  ク",
            "subtitle": "経典再生 · ハイスコアに挑戦",
            "speed": "移動速度",
            "mode_prefix": "モード: ",
            "mode_endless": "エンドレス",
            "mode_timed": "タイム",
            "edge_slide": "边缘: スライド",
            "edge_death": "边缘: デス",
            "edge_wrap": "边缘: ワープ",
            "start": "ゲーム開始",
            "vs_mode": "VS AI",
            "shop": "ショップ",
            "skin_shop": "スキン",
            "achievements": "実績",
            "skin_label": "スキン",
            "help": "遊び方",
            "stats": "統計",
            "update": "履歴",
            "dev": "開発",
            "music": "音楽",
            "music_title": "音 楽 コ ン ト ロール",
            "volume": "音量",
            "no_music": "音楽なし",
            "playing_status": "再生中",
            "paused_status": "一時停止",
            "current_playing": "再生中の曲",
            "track_list": "曲リスト",
            "prev": "<<",
            "play": "再生",
            "pause_btn": "一時停止",
            "next": ">>",
            "help_title": "遊 び 方",
            "stats_title": "統 計 情 報",
            "update_title": "更 新 履 歴",
            "dev_title": "開 発 情 報",
            "effects_on": "FX: ON",
            "effects_off": "FX: OFF",
            "score": "スコア",
            "multiplier": "倍率",
            "mode_label": "モード",
            "mode_endless": "エンドレス",
            "mode_timed": "タイム",
            "time_label": "時間",
            "food_label": "エサ",
            "high_label": "ハイスコア",
            "pause": "一時停止",
            "paused_label": "一 時 停 止",
            "resume": "再開",
            "end": "終了",
            "game_over": "ゲ ー ム 終 了",
            "score_label": "今回のスコア",
            "max_endless": "エンドレス最高",
            "max_timed": "タイム最高",
            "total_score": "累計スコア",
            "new_record": "新 記 録 !",
            "restart": "もう一回",
            "back_menu": "メニューへ",
            "score_earned": "累計獲得スコア",
            "shop_title": "ポ イ ン ト シ ョ ッ プ",
            "exchange_rate": "交換比率: 累計スコア2 = ポイント1",
            "redeemable": "交換可能",
            "redeemed": "交換済み",
            "total": "累計スコア",
            "current_redeemable": "交換可能: {} pts",
            "history_total": "累計獲得: {} pts",
            "exchange_1": "1ポイント交換",
            "exchange_10": "10ポイント交換",
            "exchange_50": "50ポイント交換",
            "exchange_all": "全額交換",
            "exchange_success": "交換成功! {}ptsで{}pts獲得",
            "exchange_fail": "交換可能ptsが{}不足",
            "click_close": "外をクリックで閉じる",
            "scroll_close": "スクロール | 外をクリック",
            "skin_title": "ス キ ン シ ョ ッ プ",
            "skin_hint": "クリックで購入/装着 | スクロール | 外をクリック",
            "equipped": "装着中",
            "owned": "所持済み",
            "price_pts": "{} pts",
            "confirm_buy": "{}を購入?",
            "cost_pts": "消費: {} pts",
            "confirm_yes": "確認",
            "confirm_no": "キャンセル",
            "skin_click_equip": "クリックで装着",
            "skin_click_buy": "クリックで購入",
            "unlock_time": "プレイ3分で解放",
            "vs_player": "プレイヤー",
            "vs_ai": "AI",
            "vs_win": "プレイヤー勝利!",
            "vs_lose": "AI勝利!",
            "vs_draw": "引き分け!",
            "vs_food": "エサ",
            "diff_select": "AI難易度選択",
            "lang_select": "言語選択",
            "theme": "テーマ",
            "rank_bronze": "ブロンズ",
            "rank_silver": "シルバー",
            "rank_gold": "ゴールド",
            "rank_platinum": "プラチナ",
            "rank_diamond": "ダイヤ",
            "rank_master": "マスター",
            "rank_title": "ランク",
            "rank_xp": "XP",
            "rank_level": "レベル",
            "rank_next_reward": "次の報酬",
            "rank_xp_earned": "+{} XP",
            "rank_level_up": "レベルアップ! Lv.{}",
            "rank_progress": "{}/{} XP",
            "rank_streak": "連勝 x{}",
            "rank_bonus": "+{}% 連勝ボーナス",
            "daily_challenge": "デイリーチャレンジ",
            "daily_modifier": "今日のルール",
            "daily_best": "ベストスコア",
            "daily_play": "挑戦",
            "daily_result": "チャレンジ完了",
            "daily_xp_bonus": "ボーナス +{} XP",
            "daily_rewards": "報酬説明",
            "daily_reward_participate": "参加報酬 +20 XP",
            "daily_reward_score": "スコア報酬 +スコア÷10 XP",
            "daily_reward_modifier": "高倍率ボーナス",
            "daily_speed_storm": "スピードストーム",
            "daily_speed_storm_desc": "地獄速度、スコアx2.5",
            "daily_shrink": "縮小",
            "daily_shrink_desc": "10移動ごとに縮小",
            "daily_maze": "迷路",
            "daily_maze_desc": "8つの障害物",
            "daily_rush": "ラッシュ",
            "daily_rush_desc": "90秒制限、スコアx2",
            "daily_quad_food": "4倍エサ",
            "daily_quad_food_desc": "4つのエサ同時",
            "daily_skin_lock": "スキンロック",
            "daily_skin_lock_desc": "ランダムスキン固定",
            "daily_wrap_random": "ランダムワープ",
            "daily_wrap_random_desc": "壁でランダム出現",
            "daily_crit_chance": "クリティカル",
            "daily_crit_chance_desc": "20%クリティカルx5/10%ミス",
            "help_content": [
                "[ 操作方法 ]",
                "  矢印キー / WASD    移動",
                "  ESC               メニューに戻る",
                "  スペース           一時停止/再開",
                "",
                "[ ルール ]",
                "  エサを食べて成長＆スコアUP",
                "  边缘モードはメニューで切替",
                "  自分に当たればゲームオーバー",
                "",
                "[ モード ]",
                "  エンドレス - 無限プレイ",
                "  タイム     - 3分チャレンジ",
                "",
                "[ スコア倍率 ]",
                "  基本: Easy×0.8 Normal×1.0 Hard×1.5 Hell×2.0",
                "  倍加: エサ10個ごとにスコア2倍",
                "  スキン: 貪食×1.2 エントロピー×3",
                "  OFF時は全ボーナス無効",
                "",
                "[ VS AI ]",
                "  メニューで「VS AI」をクリック",
                "  難易度選択後に開始",
                "  結果は累計スコアに反映",
            ],
            "dev_content": [
                "[ 開発情報 ]",
                "",
                "  作者    :  WEZHCE",
                "  メール  :  wezhce055@outlook.com",
                "  B站 UID:  1309420497",
                "  GitHub  :  https://github.com/WEZHCE",
                "",
                "  バージョン:  7.10 (ランク&デイリー版)",
                "  エンジン  :  Python 3 + Pygame",
            ],
            "update_content": [
                "═══════  v7.10  ═══════",
                "",
                "  [追加] ランク/レベルシステム：XP、レベル、ランク、連勝ボーナス",
                "  [追加] 6つのランク：ブロンズ/シルバー/ゴールド/プラチナ/ダイヤ/マスター",
                "  [追加] 5つのランク専用スキン（Lv.10~50で解放）",
                "  [追加] ランクパネル：レベル、XPバー、連勝、マイルストーン",
                "  [追加] レベルアップ通知ポップアップ",
                "  [追加] デイリーチャレンジ：8つのModifierが日替わり",
                "  [追加] デイリーチャレンジ情報と結果画面",
                "  [追加] 実績ポイント報酬（難易度別5~50pts）",
                "  [修復] スキンショップのスクロールバー改善",
                "  [修復] スキンショップの新しいスキンの解放条件表示",
                "  [修復] 全ポップアップのスクロールバーがマウスドラッグ対応",
                "",
                "═══════  v7.9  ═══════",
                "",
                "  [追加] 日本語言語対応（中/英/日3言語切替）",
                "  [追加] テーマシステム：6種類のカラーテーマ",
                "  [追加] 言語選択ポップアップ",
                "  [追加] テーマ選択ポップアップ（配色プレビュー付き）",
                "  [追加] ボタンがテーマに合わせて自動切替",
                "  [追加] 文字の自動コントラスト（明暗適応）",
                "  [修復] 難易度選択ポップアップの外部クリック終了",
                "  [修復] 言語切替時ショップボタンのテキスト同期更新",
                "  [修復] ライテーマでボタン文字を自動的に暗色に変更",
                "  [修復] テーマ選択ポップアップのレイアウト修正",
                "  [修復] 日本語モードの音楽ポップアップ翻訳補完",
                "  [修復] 音楽リストの現在曲マークを共通記号に変更",
                "  [最適化] UI全体の美観向上、プロフェッショナルな配色",
                "  [追加] 実績システム：22個の実績（6個のシークレット）",
                "  [追加] 実績達成通知ポップアップ",
                "  [追加] 実績閲覧パネル",
                "",
                "  ※ 日本語の一部は機械翻訳を使用しています",
                "",
                "═══════  v7.8  ═══════",
                "",
                "  [修復] メニューボタンのホバー修正",
                "  [修復] VSモード逆走修正",
                "  [修復] VSモード時間集計修正",
                "  [修復] 满盤時無限ループ修正",
                "  [修復] 重力スキン修正",
                "  [追加] スキン購入確認ダイアログ",
                "  [最適化] オーバーレイサーフェスキャッシュ",
                "  [追加] 边缘モード3態: デス/スライド/ワープ",
                "  [修復] 真正的壁沿いスライド実装",
                "  [修復] 英語テキスト欠落修正",
                "  [修復] 全ボタンの言語切替対応",
                "  [修復] 音楽ボリュームバー修正",
                "  [修復] ショップボタン溢れ修正",
                "  [最適化] スキンショップUI再設計",
                "",
                "═══════  v7.7  ═══════",
                "",
                "  [修復] 通常モード操作不能修正",
                "  [修復] VSモード边缘修正",
                "  [修復] 一时停止/終了ボタン修正",
                "  [修復] 边缘スライドをワープに変更",
                "",
                "═══════  v7.6  ═══════",
                "",
                "  [調整] ワームホール120ptsに変更",
                "  [調整] DeepSeek-Flashを500ptsに変更",
                "  [修復] セカンドライフの復活修正",
                "  [修復] VSモードの集計修正",
                "  [修復] 对战中边缘衝突の修正",
                "  [追加] スコア倍率説明をヘルプに統合",
                "",
                "═══════  v7.5  ═══════",
                "",
                "  [修復] 重力/速度/ワームホール修正",
                "  [追加] AI難易度3段階選択",
                "",
                "═══════  v7.4  ═══════",
                "",
                "  [追加] VS AIモード (BFS AI)",
                "",
                "═══════  v7.3  ═══════",
                "",
                "  [修復] 簡單モード無スコア修正",
                "  [追加] スコア小数点表示",
                "",
                "═══════  v7.2  ═══════",
                "",
                "  [修復] 紅の情熱自動解放修正",
                "  [修復] スコア倍率修正",
                "  [追加] 簡單モード×0.8",
                "",
                "═══════  v7.1  ═══════",
                "",
                "  [修復] スキンショップ購入修正",
                "  [修復] セーブファイル権限修正",
                "",
                "═══════  v7.0  ═══════",
                "",
                "  [追加] 11種スキンシステム",
                "  [追加] エフェクトON/OFF",
                "  [調整] 難しい×1.5, 地獄×2.0",
                "",
                "═══════  v6.0  ═══════",
                "",
                "  [追加] 英語言語対応",
                "  [追加] 死亡フラッシュエフェクト",
                "  [最適化] ゲームオーバー画面再設計",
                "",
                "═══════  v5.9  ═══════",
                "",
                "  [追加] ポイントショップシステム",
                "",
                "═══════  v5.8  ═══════",
                "",
                "  [追加] 音楽コントロールウィンドウ",
                "",
                "═══════  v5.7  ═══════",
                "",
                "  [修復] PyInstaller音楽消失修正",
                "",
                "═══════  v5.6  ═══════",
                "",
                "  [修復] 音楽ボタン重なり修正",
                "",
                "═══════  v5.5  ═══════",
                "",
                "  [修復] 音楽ボタン位置修正",
                "",
                "═══════  v5.4  ═══════",
                "",
                "  [修復] 破損音楽ファイルスキップ",
                "",
                "═══════  v5.3  ═══════",
                "",
                "  [更新] 開発者情報",
                "",
                "═══════  v5.2  ═══════",
                "",
                "  [追加] バックグラウンド音楽",
                "",
                "═══════  v5.1  ═══════",
                "",
                "  [追加] 統計情報ボタン",
                "",
                "═══════  v5.0  ═══════",
                "",
                "  [調整] アカウントシステム削除",
                "",
                "═══════  v4.0  ═══════",
                "",
                "  [追加] デュアルモードシステム",
                "  [追加] ゲーム内コントロール",
                "  [追加] リアルタイムスコアパネル",
                "",
                "═══════  v3.0  ═══════",
                "",
                "  [追加] 边缘衝突モード切替",
                "  [追加] スコア倍加機能",
            ],
        }
    }

    def T(key, *args):
        text = LANG[current_lang].get(key, key)
        if args:
            try:
                return text.format(*args)
            except:
                return text
        return text

    # ==================================================================
    #  主题系统
    # ==================================================================
    current_theme = "nord"

    THEMES = {
        "nord": {
            "name": {"zh": "极地之夜", "en": "Nord", "ja": "ノルド"},
            "BG_DARK": (46, 52, 64), "BG_MID": (59, 66, 82), "BG_LIGHT": (67, 76, 94),
            "GRID_EVEN": (52, 60, 74), "GRID_ODD": (58, 67, 82),
            "ACCENT": (129, 161, 193), "ACCENT_HOVER": (136, 192, 208),
            "FOOD_MAIN": (191, 97, 106), "FOOD_GLOW": (208, 135, 112),
            "TEXT_MAIN": (216, 222, 233), "TEXT_DIM": (136, 142, 153), "TEXT_DARK": (97, 103, 116),
            "PANEL_BG": (49, 56, 68), "PANEL_BORDER": (70, 78, 90),
            "BTN_BG": (60, 68, 82), "BTN_HOVER": (72, 80, 95),
            "GOLD": (235, 203, 139), "GREEN_BTN": (163, 190, 140), "GREEN_BTN_H": (175, 205, 155),
            "RED_BTN": (191, 97, 106), "RED_BTN_H": (210, 115, 125),
            "BLUE_BTN": (129, 161, 193), "BLUE_BTN_H": (145, 175, 210),
            "SPEED_ACTIVE": (136, 192, 208), "VOLUME_TRACK": (65, 72, 85),
            "VOLUME_FILL": (129, 161, 193), "SHOP_GOLD": (235, 203, 139),
            "OVERLAY": (46, 52, 64, 210), "SCORE_PANEL": (49, 56, 68, 210),
            "SCROLL_BAR": (80, 88, 102), "SCROLL_BAR_BG": (55, 62, 75),
            "VS_PLAYER": (163, 190, 140), "VS_AI": (191, 97, 106),
            "PURPLE": (180, 142, 173),
        },
        "ocean": {
            "name": {"zh": "深海幻境", "en": "Ocean", "ja": "オーシャン"},
            "BG_DARK": (17, 24, 39), "BG_MID": (25, 35, 55), "BG_LIGHT": (32, 45, 68),
            "GRID_EVEN": (22, 32, 50), "GRID_ODD": (26, 38, 58),
            "ACCENT": (94, 234, 212), "ACCENT_HOVER": (134, 239, 188),
            "FOOD_MAIN": (251, 146, 60), "FOOD_GLOW": (253, 186, 116),
            "TEXT_MAIN": (190, 220, 235), "TEXT_DIM": (100, 150, 180), "TEXT_DARK": (60, 90, 120),
            "PANEL_BG": (20, 28, 45), "PANEL_BORDER": (35, 50, 75),
            "BTN_BG": (28, 40, 60), "BTN_HOVER": (35, 50, 75),
            "GOLD": (252, 211, 77), "GREEN_BTN": (52, 211, 153), "GREEN_BTN_H": (72, 225, 170),
            "RED_BTN": (239, 68, 68), "RED_BTN_H": (252, 100, 100),
            "BLUE_BTN": (59, 130, 246), "BLUE_BTN_H": (96, 165, 250),
            "SPEED_ACTIVE": (94, 234, 212), "VOLUME_TRACK": (35, 50, 75),
            "VOLUME_FILL": (52, 211, 153), "SHOP_GOLD": (252, 211, 77),
            "OVERLAY": (17, 24, 39, 210), "SCORE_PANEL": (20, 28, 45, 210),
            "SCROLL_BAR": (45, 60, 85), "SCROLL_BAR_BG": (25, 35, 55),
            "VS_PLAYER": (94, 234, 212), "VS_AI": (251, 146, 60),
            "PURPLE": (167, 139, 250),
        },
        "forest": {
            "name": {"zh": "迷雾森林", "en": "Forest", "ja": "フォレスト"},
            "BG_DARK": (20, 28, 22), "BG_MID": (28, 40, 32), "BG_LIGHT": (36, 50, 40),
            "GRID_EVEN": (25, 35, 28), "GRID_ODD": (30, 42, 34),
            "ACCENT": (134, 239, 172), "ACCENT_HOVER": (163, 255, 190),
            "FOOD_MAIN": (251, 191, 36), "FOOD_GLOW": (253, 211, 80),
            "TEXT_MAIN": (200, 235, 210), "TEXT_DIM": (110, 165, 125), "TEXT_DARK": (65, 100, 75),
            "PANEL_BG": (24, 32, 26), "PANEL_BORDER": (38, 55, 42),
            "BTN_BG": (32, 45, 35), "BTN_HOVER": (40, 55, 45),
            "GOLD": (252, 211, 77), "GREEN_BTN": (34, 197, 94), "GREEN_BTN_H": (52, 220, 115),
            "RED_BTN": (239, 68, 68), "RED_BTN_H": (252, 100, 100),
            "BLUE_BTN": (96, 165, 250), "BLUE_BTN_H": (130, 185, 252),
            "SPEED_ACTIVE": (134, 239, 172), "VOLUME_TRACK": (38, 55, 42),
            "VOLUME_FILL": (34, 197, 94), "SHOP_GOLD": (252, 211, 77),
            "OVERLAY": (20, 28, 22, 210), "SCORE_PANEL": (24, 32, 26, 210),
            "SCROLL_BAR": (45, 65, 50), "SCROLL_BAR_BG": (28, 40, 32),
            "VS_PLAYER": (134, 239, 172), "VS_AI": (251, 191, 36),
            "PURPLE": (192, 132, 252),
        },
        "sunset": {
            "name": {"zh": "落日余晖", "en": "Sunset", "ja": "サンセット"},
            "BG_DARK": (28, 18, 18), "BG_MID": (40, 25, 22), "BG_LIGHT": (52, 33, 28),
            "GRID_EVEN": (35, 22, 20), "GRID_ODD": (42, 28, 24),
            "ACCENT": (251, 146, 60), "ACCENT_HOVER": (253, 165, 90),
            "FOOD_MAIN": (239, 68, 68), "FOOD_GLOW": (252, 100, 100),
            "TEXT_MAIN": (235, 220, 200), "TEXT_DIM": (170, 140, 120), "TEXT_DARK": (110, 85, 70),
            "PANEL_BG": (32, 22, 20), "PANEL_BORDER": (55, 35, 30),
            "BTN_BG": (45, 28, 25), "BTN_HOVER": (55, 35, 30),
            "GOLD": (252, 211, 77), "GREEN_BTN": (34, 197, 94), "GREEN_BTN_H": (52, 220, 115),
            "RED_BTN": (220, 50, 50), "RED_BTN_H": (245, 75, 75),
            "BLUE_BTN": (96, 165, 250), "BLUE_BTN_H": (130, 185, 252),
            "SPEED_ACTIVE": (251, 146, 60), "VOLUME_TRACK": (55, 35, 30),
            "VOLUME_FILL": (251, 146, 60), "SHOP_GOLD": (252, 211, 77),
            "OVERLAY": (28, 18, 18, 210), "SCORE_PANEL": (32, 22, 20, 210),
            "SCROLL_BAR": (65, 42, 35), "SCROLL_BAR_BG": (40, 25, 22),
            "VS_PLAYER": (134, 239, 172), "VS_AI": (239, 68, 68),
            "PURPLE": (192, 132, 252),
        },
        "lavender": {
            "name": {"zh": "薰衣草梦", "en": "Lavender", "ja": "ラベンダー"},
            "BG_DARK": (24, 20, 32), "BG_MID": (32, 26, 44), "BG_LIGHT": (40, 33, 55),
            "GRID_EVEN": (28, 24, 38), "GRID_ODD": (34, 28, 46),
            "ACCENT": (192, 132, 252), "ACCENT_HOVER": (210, 155, 255),
            "FOOD_MAIN": (251, 113, 133), "FOOD_GLOW": (253, 140, 160),
            "TEXT_MAIN": (225, 215, 240), "TEXT_DIM": (145, 130, 170), "TEXT_DARK": (95, 85, 115),
            "PANEL_BG": (28, 24, 38), "PANEL_BORDER": (45, 38, 60),
            "BTN_BG": (36, 30, 50), "BTN_HOVER": (44, 36, 60),
            "GOLD": (252, 211, 77), "GREEN_BTN": (34, 197, 94), "GREEN_BTN_H": (52, 220, 115),
            "RED_BTN": (239, 68, 68), "RED_BTN_H": (252, 100, 100),
            "BLUE_BTN": (96, 165, 250), "BLUE_BTN_H": (130, 185, 252),
            "SPEED_ACTIVE": (192, 132, 252), "VOLUME_TRACK": (45, 38, 60),
            "VOLUME_FILL": (192, 132, 252), "SHOP_GOLD": (252, 211, 77),
            "OVERLAY": (24, 20, 32, 210), "SCORE_PANEL": (28, 24, 38, 210),
            "SCROLL_BAR": (55, 45, 70), "SCROLL_BAR_BG": (32, 26, 44),
            "VS_PLAYER": (134, 239, 172), "VS_AI": (251, 113, 133),
            "PURPLE": (192, 132, 252),
        },
        "light": {
            "name": {"zh": "明亮浅色", "en": "Light", "ja": "ライト"},
            "BG_DARK": (235, 235, 240), "BG_MID": (245, 245, 250), "BG_LIGHT": (255, 255, 255),
            "GRID_EVEN": (240, 240, 246), "GRID_ODD": (248, 248, 252),
            "ACCENT": (70, 130, 200), "ACCENT_HOVER": (90, 150, 220),
            "FOOD_MAIN": (220, 80, 80), "FOOD_GLOW": (240, 120, 120),
            "TEXT_MAIN": (30, 30, 40), "TEXT_DIM": (100, 100, 120), "TEXT_DARK": (160, 160, 170),
            "PANEL_BG": (248, 248, 252), "PANEL_BORDER": (210, 210, 220),
            "BTN_BG": (220, 220, 230), "BTN_HOVER": (200, 200, 215),
            "GOLD": (200, 160, 0), "GREEN_BTN": (50, 160, 100), "GREEN_BTN_H": (60, 180, 120),
            "RED_BTN": (200, 70, 70), "RED_BTN_H": (220, 90, 90),
            "BLUE_BTN": (60, 120, 200), "BLUE_BTN_H": (80, 140, 220),
            "SPEED_ACTIVE": (70, 130, 200), "VOLUME_TRACK": (210, 210, 220),
            "VOLUME_FILL": (70, 130, 200), "SHOP_GOLD": (200, 160, 0),
            "OVERLAY": (235, 235, 240, 210), "SCORE_PANEL": (248, 248, 252, 210),
            "SCROLL_BAR": (180, 180, 195), "SCROLL_BAR_BG": (220, 220, 230),
            "VS_PLAYER": (50, 160, 100), "VS_AI": (220, 80, 80),
            "PURPLE": (150, 100, 200),
        },
    }

    def apply_theme(theme_id):
        """应用主题到Colors类"""
        nonlocal current_theme
        current_theme = theme_id
        theme = THEMES[theme_id]
        for key, val in theme.items():
            if key == "name":
                continue
            setattr(Colors, key, val)
        # 更新缓存的overlay表面
        _overlay_cache.fill(Colors.OVERLAY)

    # ==================================================================
    #  成就系统
    # ==================================================================
    ACHIEVEMENTS = [
        # 常规成就 - 游戏局数
        {"id": "first_game", "icon": "[+]", "secret": False, "points": 5,
         "name": {"zh": "初出茅庐", "en": "First Step", "ja": "初めての一歩"},
         "desc": {"zh": "完成第一局游戏", "en": "Complete your first game", "ja": "初めてのゲームを完了"},
         "cond": {"type": "games_played", "value": 1}},
        {"id": "games_10", "icon": "[10]", "secret": False, "points": 10,
         "name": {"zh": "小试牛刀", "en": "Getting Started", "ja": "試しに一手"},
         "desc": {"zh": "累计游玩 10 局", "en": "Play 10 games", "ja": "累計10局プレイ"},
         "cond": {"type": "games_played", "value": 10}},
        {"id": "games_50", "icon": "[50]", "secret": False, "points": 20,
         "name": {"zh": "渐入佳境", "en": "Seasoned Player", "ja": "上達中"},
         "desc": {"zh": "累计游玩 50 局", "en": "Play 50 games", "ja": "累計50局プレイ"},
         "cond": {"type": "games_played", "value": 50}},
        {"id": "games_100", "icon": "[100]", "secret": False, "points": 40,
         "name": {"zh": "蛇场老将", "en": "Snake Veteran", "ja": "蛇のベテラン"},
         "desc": {"zh": "累计游玩 100 局", "en": "Play 100 games", "ja": "累計100局プレイ"},
         "cond": {"type": "games_played", "value": 100}},

        # 常规成就 - 单局得分
        {"id": "score_100", "icon": "S100", "secret": False, "points": 10,
         "name": {"zh": "百分达人", "en": "Centurion", "ja": "100点達成"},
         "desc": {"zh": "单局得分 >= 100", "en": "Score 100 in one game", "ja": "1回のゲームで100点"},
         "cond": {"type": "game_score", "value": 100}},
        {"id": "score_500", "icon": "S500", "secret": False, "points": 25,
         "name": {"zh": "五百分先生", "en": "High Scorer", "ja": "500点の偉業"},
         "desc": {"zh": "单局得分 >= 500", "en": "Score 500 in one game", "ja": "1回のゲームで500点"},
         "cond": {"type": "game_score", "value": 500}},
        {"id": "score_1000", "icon": "S1K", "secret": False, "points": 50,
         "name": {"zh": "千分传奇", "en": "Legendary", "ja": "1000点の伝説"},
         "desc": {"zh": "单局得分 >= 1000", "en": "Score 1000 in one game", "ja": "1回のゲームで1000点"},
         "cond": {"type": "game_score", "value": 1000}},

        # 常规成就 - 蛇身长度
        {"id": "length_15", "icon": "L15", "secret": False, "points": 10,
         "name": {"zh": "小有长进", "en": "Growing Up", "ja": "少し成長"},
         "desc": {"zh": "蛇身长度 >= 15", "en": "Reach length 15", "ja": "長さ15に到達"},
         "cond": {"type": "snake_length", "value": 15}},
        {"id": "length_30", "icon": "L30", "secret": False, "points": 20,
         "name": {"zh": "蛇王降临", "en": "Snake King", "ja": "蛇王降臨"},
         "desc": {"zh": "蛇身长度 >= 30", "en": "Reach length 30", "ja": "長さ30に到達"},
         "cond": {"type": "snake_length", "value": 30}},
        {"id": "length_50", "icon": "L50", "secret": False, "points": 40,
         "name": {"zh": "巨蟒之姿", "en": "Giant Python", "ja": "巨大な蛇"},
         "desc": {"zh": "蛇身长度 >= 50", "en": "Reach length 50", "ja": "長さ50に到達"},
         "cond": {"type": "snake_length", "value": 50}},

        # 常规成就 - 累计食物
        {"id": "food_50", "icon": "F50", "secret": False, "points": 5,
         "name": {"zh": "初尝甜头", "en": "First Bite", "ja": "初の一口"},
         "desc": {"zh": "累计吃 50 个食物", "en": "Eat 50 foods total", "ja": "累計50個のエサ"},
         "cond": {"type": "total_food", "value": 50}},
        {"id": "food_200", "icon": "F200", "secret": False, "points": 15,
         "name": {"zh": "贪食蛇", "en": "Glutton", "ja": "貪欲な蛇"},
         "desc": {"zh": "累计吃 200 个食物", "en": "Eat 200 foods total", "ja": "累計200個のエサ"},
         "cond": {"type": "total_food", "value": 200}},
        {"id": "food_500", "icon": "F500", "secret": False, "points": 30,
         "name": {"zh": "无底深渊", "en": "Bottomless Pit", "ja": "底なしの胃"},
         "desc": {"zh": "累计吃 500 个食物", "en": "Eat 500 foods total", "ja": "累計500個のエサ"},
         "cond": {"type": "total_food", "value": 500}},

        # 常规成就 - 累计时长
        {"id": "time_10min", "icon": "T10", "secret": False, "points": 10,
         "name": {"zh": "片刻欢愉", "en": "Quick Session", "ja": "ひとときの楽しみ"},
         "desc": {"zh": "累计游戏 10 分钟", "en": "Play 10 minutes total", "ja": "累計10分プレイ"},
         "cond": {"type": "total_time", "value": 600}},
        {"id": "time_1hour", "icon": "T60", "secret": False, "points": 25,
         "name": {"zh": "蛇迷心窍", "en": "Addicted", "ja": "蛇に夢中"},
         "desc": {"zh": "累计游戏 1 小时", "en": "Play 1 hour total", "ja": "累計1時間プレイ"},
         "cond": {"type": "total_time", "value": 3600}},

        # 常规成就 - 人机对战
        {"id": "vs_win", "icon": "V1", "secret": False, "points": 15,
         "name": {"zh": "首胜告捷", "en": "First Victory", "ja": "初勝利"},
         "desc": {"zh": "首次战胜 AI", "en": "Beat AI once", "ja": "AIに初勝利"},
         "cond": {"type": "vs_wins", "value": 1}},
        {"id": "vs_win_10", "icon": "V10", "secret": False, "points": 30,
         "name": {"zh": "常胜将军", "en": "Champion", "ja": "勝ち組"},
         "desc": {"zh": "累计战胜 AI 10 次", "en": "Beat AI 10 times", "ja": "AIに10回勝利"},
         "cond": {"type": "vs_wins", "value": 10}},
        {"id": "vs_hell", "icon": "V!", "secret": False, "points": 50,
         "name": {"zh": "地狱征服者", "en": "Hell Conqueror", "ja": "地獄を制す者"},
         "desc": {"zh": "地狱难度战胜 AI", "en": "Beat AI on Hell", "ja": "地獄難易度でAIに勝利"},
         "cond": {"type": "vs_hell_win", "value": 1}},

        # 常规成就 - 收集/探索
        {"id": "all_speeds", "icon": "[A]", "secret": False, "points": 25,
         "name": {"zh": "全能选手", "en": "All-Rounder", "ja": "万能選手"},
         "desc": {"zh": "所有难度都玩过", "en": "Play all difficulties", "ja": "全難易度をプレイ"},
         "cond": {"type": "speeds_played", "value": 4}},
        {"id": "all_themes", "icon": "[T]", "secret": False, "points": 20,
         "name": {"zh": "彩虹鉴赏家", "en": "Theme Explorer", "ja": "テーマ探索者"},
         "desc": {"zh": "使用过所有主题", "en": "Use all themes", "ja": "全テーマを使用"},
         "cond": {"type": "themes_used", "value": 6}},

        # 隐藏彩蛋成就
        {"id": "die_first", "icon": "[?]", "secret": True, "points": 10,
         "name": {"zh": "出师未捷", "en": "Premature Demise", "ja": "出師未捷"},
         "desc": {"zh": "开局 5 秒内死亡", "en": "Die within 5 seconds", "ja": "5秒以内に死亡"},
         "cond": {"type": "fast_death", "value": 5}},
        {"id": "wall_hugger", "icon": "[?]", "secret": True, "points": 20,
         "name": {"zh": "墙头草", "en": "Wall Hugger", "ja": "壁党"},
         "desc": {"zh": "沿墙滑行超过 15 次", "en": "Slide along wall 15+ times", "ja": "壁沿いを15回以上スライド"},
         "cond": {"type": "wall_slides", "value": 15}},
        {"id": "corners", "icon": "[?]", "secret": True, "points": 25,
         "name": {"zh": "四角俱全", "en": "Corner Collector", "ja": "四隅制覇"},
         "desc": {"zh": "一局内访问全部 4 个角", "en": "Visit all 4 corners in one game", "ja": "1局で4隅全てを訪問"},
         "cond": {"type": "corners_visited", "value": 4}},
        {"id": "reverse_master", "icon": "[?]", "secret": True, "points": 30,
         "name": {"zh": "倒行逆施", "en": "Reverse Master", "ja": "逆走の達人"},
         "desc": {"zh": "使用熵减蛇皮肤完成一局", "en": "Finish a game with Entropy Snake", "ja": "エントロピースキンで完了"},
         "cond": {"type": "skin_game_complete", "value": 6}},
    ]

    # 成就解锁状态 (运行时)
    unlocked_achievements = set()
    achievement_popup = None  # 当前显示的成就弹窗
    achievement_popup_timer = 0

    def unlock_achievement(ach_id):
        """解锁成就，返回是否新解锁"""
        nonlocal unlocked_achievements, achievement_popup, achievement_popup_timer
        if ach_id in unlocked_achievements:
            return False
        unlocked_achievements.add(ach_id)
        stats["unlocked_achievements"] = list(unlocked_achievements)
        # 奖励积分
        ach = next((a for a in ACHIEVEMENTS if a["id"] == ach_id), None)
        if ach:
            pts = ach.get("points", 0)
            if pts > 0:
                stats["total_score"] += pts * SCORE_SCALE
                ach["_earned_points"] = pts  # 记录用于弹窗显示
        save_stats()
        # 显示解锁弹窗
        if ach:
            achievement_popup = ach
            achievement_popup_timer = 180  # 3秒 (60fps)
        return True

    def check_achievements(ctx):
        """检查成就条件，ctx 为字典包含当前状态"""
        nonlocal unlocked_achievements
        for ach in ACHIEVEMENTS:
            if ach["id"] in unlocked_achievements:
                continue
            c = ach["cond"]
            t = c["type"]
            v = c["value"]
            unlocked = False
            if t == "games_played" and ctx.get("games_played", 0) >= v:
                unlocked = True
            elif t == "game_score" and ctx.get("game_score", 0) >= v:
                unlocked = True
            elif t == "snake_length" and ctx.get("snake_length", 0) >= v:
                unlocked = True
            elif t == "total_food" and ctx.get("total_food", 0) >= v:
                unlocked = True
            elif t == "total_time" and ctx.get("total_time", 0) >= v:
                unlocked = True
            elif t == "vs_wins" and ctx.get("vs_wins", 0) >= v:
                unlocked = True
            elif t == "vs_hell_win" and ctx.get("vs_hell_win", False):
                unlocked = True
            elif t == "speeds_played" and len(ctx.get("speeds_played", set())) >= v:
                unlocked = True
            elif t == "themes_used" and len(ctx.get("themes_used", set())) >= v:
                unlocked = True
            elif t == "fast_death" and ctx.get("game_duration", 999) <= v:
                unlocked = True
            elif t == "wall_slides" and ctx.get("wall_slides", 0) >= v:
                unlocked = True
            elif t == "corners_visited" and len(ctx.get("corners_visited", set())) >= v:
                unlocked = True
            elif t == "skin_game_complete" and ctx.get("skin_id") == v and ctx.get("game_completed"):
                unlocked = True
            if unlocked:
                unlock_achievement(ach["id"])

    # ==================================================================
    #  段位/等级系统
    # ==================================================================
    def xp_for_level(level):
        return 100 + (level - 1) * 60

    def xp_to_level(total_xp):
        level = 1
        remaining = total_xp
        while True:
            need = xp_for_level(level)
            if remaining < need:
                return (level, remaining, need)
            remaining -= need
            level += 1

    def get_rank_tier(level):
        if level <= 5:
            return {"name_key": "rank_bronze", "color": (205, 127, 50)}
        elif level <= 10:
            return {"name_key": "rank_silver", "color": (192, 192, 192)}
        elif level <= 25:
            return {"name_key": "rank_gold", "color": (255, 215, 0)}
        elif level <= 35:
            return {"name_key": "rank_platinum", "color": (0, 206, 209)}
        elif level <= 45:
            return {"name_key": "rank_diamond", "color": (185, 242, 255)}
        else:
            return {"name_key": "rank_master", "color": (255, 69, 0)}

    def award_xp(amount, reason=""):
        nonlocal unlocked_skins, rank_levelup_popup, rank_levelup_timer
        streak = stats.get("xp_streak", 0)
        bonus_pct = 0
        if streak >= 10:
            amount = int(amount * 1.3)
            bonus_pct = 30
        elif streak >= 5:
            amount = int(amount * 1.2)
            bonus_pct = 20
        elif streak >= 3:
            amount = int(amount * 1.1)
            bonus_pct = 10
        stats["xp"] = stats.get("xp", 0) + amount
        old_level = stats.get("level", 1)
        new_level, _, _ = xp_to_level(stats["xp"])
        leveled_up = None
        if new_level > old_level:
            stats["level"] = new_level
            _apply_rank_rewards(new_level)
            rank_levelup_popup = new_level
            rank_levelup_timer = 180
            leveled_up = new_level
        return (leveled_up, amount, bonus_pct)

    def _apply_rank_rewards(level):
        nonlocal unlocked_skins
        reward_map = {10: 11, 20: 12, 30: 13, 40: 14, 50: 15}
        for lv, skin_id in reward_map.items():
            if level >= lv and skin_id not in unlocked_skins:
                unlocked_skins.append(skin_id)
                stats["unlocked_skins"] = unlocked_skins

    # 升级通知
    rank_levelup_popup = None
    rank_levelup_timer = 0

    # ==================================================================
    #  每日挑战系统
    # ==================================================================
    def get_daily_date_str():
        import datetime
        return datetime.datetime.now().strftime("%Y%m%d")

    def generate_daily_challenge(date_str):
        seed = int(date_str)
        modifier_id = seed % 8
        rng = random.Random(seed)
        skin_lock_id = rng.choice(list(range(len(SKINS)))) if modifier_id == 5 else None
        maze_walls = set()
        if modifier_id == 2:
            for _ in range(8):
                wx = rng.randint(2, GRID_SIZE - 3)
                wy = rng.randint(2, GRID_SIZE - 3)
                maze_walls.add((wx, wy))
        return {
            "date": date_str,
            "modifier_id": modifier_id,
            "skin_lock_id": skin_lock_id,
            "maze_walls": maze_walls,
        }

    DAILY_MODIFIERS = [
        {"id": 0, "name_key": "daily_speed_storm", "desc_key": "daily_speed_storm_desc", "timed_limit": 180, "score_mult": 2.5, "speed_fps": 19},
        {"id": 1, "name_key": "daily_shrink", "desc_key": "daily_shrink_desc", "timed_limit": 180, "score_mult": 1.0, "speed_fps": 9},
        {"id": 2, "name_key": "daily_maze", "desc_key": "daily_maze_desc", "timed_limit": 180, "score_mult": 1.5, "speed_fps": 9},
        {"id": 3, "name_key": "daily_rush", "desc_key": "daily_rush_desc", "timed_limit": 90, "score_mult": 2.0, "speed_fps": 14},
        {"id": 4, "name_key": "daily_quad_food", "desc_key": "daily_quad_food_desc", "timed_limit": 180, "score_mult": 1.0, "speed_fps": 9},
        {"id": 5, "name_key": "daily_skin_lock", "desc_key": "daily_skin_lock_desc", "timed_limit": 180, "score_mult": 1.2, "speed_fps": 9},
        {"id": 6, "name_key": "daily_wrap_random", "desc_key": "daily_wrap_random_desc", "timed_limit": 180, "score_mult": 1.3, "speed_fps": 9},
        {"id": 7, "name_key": "daily_crit_chance", "desc_key": "daily_crit_chance_desc", "timed_limit": 180, "score_mult": 1.0, "speed_fps": 9},
    ]

    def calc_daily_xp(score, modifier_id):
        """计算每日挑战XP奖励"""
        base_xp = score // SCORE_SCALE // 10
        mod = DAILY_MODIFIERS[modifier_id]
        mult = mod.get("score_mult", 1.0)
        # 高倍率挑战给予更多XP
        bonus_xp = int(base_xp * (mult - 1.0) * 0.5)
        return base_xp + bonus_xp + 20  # 基础参与奖励20XP

    # ==================================================================
    #  AI 难度配置
    # ==================================================================
    AI_DIFFICULTIES = [
        {"id": 0, "name": {"zh": "简单", "en": "Easy", "ja": "簡単"},
         "desc": {"zh": "随机移动，偶尔吃食物", "en": "Random moves", "ja": "ランダム移動"}},
        {"id": 1, "name": {"zh": "普通", "en": "Normal", "ja": "普通"},
         "desc": {"zh": "BFS寻路，主动追食物", "en": "BFS pathfinding", "ja": "BFS探索"}},
        {"id": 2, "name": {"zh": "地狱", "en": "Hell", "ja": "地獄"},
         "desc": {"zh": "BFS + 主动追击玩家", "en": "BFS + hunt player", "ja": "BFS + 追跡"}},
    ]
    current_ai_difficulty = 1
    diff_rects = []

    # ==================================================================
    #  皮肤配置
    # ==================================================================
    SKINS = [
        {"id":0,"name":{"zh":"经典绿","en":"Classic Green","ja":"クラシック緑"},"head_color":(144,238,144),"body_color":(120,210,120),"rainbow":False,"price":0,"default":True,"special":{"type":None,"params":None,"desc":{"zh":"经典外观","en":"Classic look","ja":"クラシック外観"}}},
        {"id":1,"name":{"zh":"烈艳红","en":"Blazing Red","ja":"紅の情熱"},"head_color":(255,182,193),"body_color":(255,150,170),"rainbow":False,"price":-1,"default":False,"unlock_condition":"time_3min","special":{"type":"speed_boost","params":1.15,"desc":{"zh":"速度提升15%","en":"Speed +15%","ja":"速度+15%"}}},
        {"id":2,"name":{"zh":"重力蛇","en":"Gravity Snake","ja":"重力ヘビ"},"head_color":(173,216,230),"body_color":(150,200,220),"rainbow":False,"price":120,"default":False,"special":{"type":"food_attract","params":3,"desc":{"zh":"食物吸附3x3","en":"Food attract 3x3","ja":"エサ吸引3x3"}}},
        {"id":3,"name":{"zh":"贪吃蛇","en":"Glutton","ja":"貪食ヘビ"},"head_color":(200,180,240),"body_color":(180,160,220),"rainbow":False,"price":400,"default":False,"special":{"type":"score_multiply","params":1.2,"desc":{"zh":"得分x1.2","en":"Score x1.2","ja":"スコアx1.2"}}},
        {"id":4,"name":{"zh":"双头蛇","en":"Two-Headed","ja":"双頭ヘビ"},"head_color":(255,250,205),"body_color":(240,235,190),"rainbow":False,"price":300,"default":False,"special":{"type":"reverse_direction","params":None,"desc":{"zh":"空格反转方向","en":"Space to reverse","ja":"スペースで反転"}}},
        {"id":5,"name":{"zh":"虫洞核心蛇","en":"Wormhole Core","ja":"ワームホール"},"head_color":(180,230,200),"body_color":(160,210,180),"rainbow":False,"price":120,"default":False,"special":{"type":None,"params":None,"desc":{"zh":"纯外观，无特效","en":"Visual only, no effect","ja":"装飾のみ"}}},
        {"id":6,"name":{"zh":"熵减蛇","en":"Entropy Snake","ja":"エントロピー"},"head_color":(255,200,210),"body_color":(235,180,190),"rainbow":False,"price":240,"default":False,"special":{"type":"reverse_controls","params":3,"desc":{"zh":"操作反向，总积分x3","en":"Reverse controls x3","ja":"操作反転x3"}}},
        {"id":7,"name":{"zh":"饥饿的蛇","en":"Hungry Snake","ja":"飢餓のヘビ"},"head_color":(255,220,180),"body_color":(240,205,165),"rainbow":False,"price":250,"default":False,"special":{"type":"double_food","params":None,"desc":{"zh":"同时存在两个食物","en":"Double food","ja":"エサ2個同時"}}},
        {"id":8,"name":{"zh":"窃时蛇","en":"Time Thief","ja":"時間泥棒"},"head_color":(210,190,230),"body_color":(195,175,215),"rainbow":False,"price":300,"default":False,"special":{"type":"time_add","params":(1,3),"desc":{"zh":"限时模式+1~3秒","en":"Timed +1~3s","ja":"タイム+1~3秒"}}},
        {"id":9,"name":{"zh":"彩虹","en":"Rainbow","ja":"虹"},"head_color":None,"body_color":None,"rainbow":True,"price":350,"default":False,"special":{"type":None,"params":None,"desc":{"zh":"浅色动态彩虹","en":"Light rainbow","ja":"ライトレインボー"}}},
        {"id":10,"name":{"zh":"DeepSeek-Flash","en":"DeepSeek-Flash","ja":"DeepSeek-Flash"},"head_color":(135,206,235),"body_color":(179,229,252),"rainbow":False,"price":500,"default":False,"special":{"type":"extra_life","params":1.0,"desc":{"zh":"两条命，死亡后随机位置全新复活","en":"2 lives, random revive","ja":"2ライフ、ランダム復活"}}},
        {"id":11,"name":{"zh":"白银之蛇","en":"Silver Serpent","ja":"シルバースネーク"},"head_color":(192,192,192),"body_color":(160,160,160),"rainbow":False,"price":-1,"default":False,"unlock_condition":"level_10","special":{"type":None,"params":None,"desc":{"zh":"白银之姿","en":"Silver Grace","ja":"シルバーの輝き"}}},
        {"id":12,"name":{"zh":"黄金巨蟒","en":"Golden Python","ja":"ゴールデンパイソン"},"head_color":(255,215,0),"body_color":(220,180,0),"rainbow":False,"price":-1,"default":False,"unlock_condition":"level_20","special":{"type":None,"params":None,"desc":{"zh":"黄金之躯","en":"Golden Body","ja":"ゴールデンの体"}}},
        {"id":13,"name":{"zh":"铂金幻影","en":"Platinum Phantom","ja":"プラチナファントム"},"head_color":(0,206,209),"body_color":(0,170,170),"rainbow":False,"price":-1,"default":False,"unlock_condition":"level_30","special":{"type":None,"params":None,"desc":{"zh":"铂金幻影","en":"Platinum Phantom","ja":"プラチナの幻影"}}},
        {"id":14,"name":{"zh":"钻石龙蛇","en":"Diamond Drake","ja":"ダイヤモンドドレイク"},"head_color":(185,242,255),"body_color":(140,220,255),"rainbow":False,"price":-1,"default":False,"unlock_condition":"level_40","special":{"type":None,"params":None,"desc":{"zh":"钻石龙蛇","en":"Diamond Drake","ja":"ダイヤモンドドレイク"}}},
        {"id":15,"name":{"zh":"至尊大师","en":"Grand Master","ja":"グランドマスター"},"head_color":(255,69,0),"body_color":(200,50,0),"rainbow":True,"price":-1,"default":False,"unlock_condition":"level_50","special":{"type":None,"params":None,"desc":{"zh":"至尊大师，彩虹特效","en":"Grand Master, Rainbow FX","ja":"グランドマスター、レインボーエフェクト"}}},
    ]

    effects_enabled = True
    current_skin_id = 0
    unlocked_skins = [0]
    teleport_target = None
    teleport_cooldown = 0
    extra_life_used = False
    second_food = None

    # ==================================================================
    #  音乐系统
    # ==================================================================
    def get_music_dir():
        if getattr(sys,'frozen',False) and hasattr(sys,'_MEIPASS'):
            p = os.path.join(sys._MEIPASS,"music")
            if os.path.isdir(p): return p
        base = os.path.dirname(sys.executable) if getattr(sys,'frozen',False) else os.path.dirname(os.path.abspath(__file__))
        for d in [os.path.join(base,"music"),os.path.join(os.getcwd(),"music")]:
            if os.path.isdir(d): return d
        return os.path.join(base,"music")

    MUSIC_DIR = get_music_dir()
    music_list, music_names = [], []
    music_index = 0
    music_playing = False
    music_volume = 0.5
    music_total = 0

    if os.path.isdir(MUSIC_DIR):
        for f in sorted(os.listdir(MUSIC_DIR)):
            if f.lower().endswith(('.mp3','.wav','.ogg')):
                fp = os.path.join(MUSIC_DIR,f)
                if os.path.getsize(fp) > 1024:
                    music_list.append(fp); music_names.append(f)
    music_total = len(music_list)

    def play_music(index=None):
        nonlocal music_index, music_playing
        if music_total == 0: return
        if index is not None: music_index = max(0, min(index, music_total-1))
        try:
            pygame.mixer.music.load(music_list[music_index])
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1); music_playing = True
        except: music_playing = False

    def stop_music():
        nonlocal music_playing; pygame.mixer.music.stop(); music_playing = False
    def pause_music():
        nonlocal music_playing
        if music_playing and pygame.mixer.music.get_busy(): pygame.mixer.music.pause(); music_playing = False
    def resume_music():
        nonlocal music_playing
        if not music_playing and music_total > 0: pygame.mixer.music.unpause(); music_playing = True
    def next_music():
        nonlocal music_index
        if music_total > 0: music_index = (music_index+1)%music_total; play_music()
    def prev_music():
        nonlocal music_index
        if music_total > 0: music_index = (music_index-1)%music_total; play_music()
    def set_volume(vol):
        nonlocal music_volume; music_volume = max(0.0, min(1.0, vol)); pygame.mixer.music.set_volume(music_volume)
    if music_total > 0: play_music(0)

    dragging_volume = False
    scrollbar_dragging = False
    scrollbar_drag_info = None
    music_list_scroll = 0

    # ==================================================================
    #  配色
    # ==================================================================
    class Colors:
        BG_DARK = (13, 13, 28)
        BG_MID = (20, 20, 45)
        BG_LIGHT = (30, 30, 60)
        GRID_EVEN = (23, 23, 50)
        GRID_ODD = (28, 28, 58)
        ACCENT = (255, 82, 112)
        ACCENT_HOVER = (255, 110, 140)
        FOOD_MAIN = (255, 82, 112)
        FOOD_GLOW = (255, 130, 150)
        TEXT_MAIN = (240, 240, 248)
        TEXT_DIM = (140, 140, 170)
        TEXT_DARK = (80, 80, 110)
        PANEL_BG = (17, 17, 38)
        PANEL_BORDER = (35, 35, 65)
        BTN_BG = (40, 40, 75)
        BTN_HOVER = (55, 55, 95)
        GOLD = (255, 215, 0)
        GREEN_BTN = (0, 180, 120)
        GREEN_BTN_H = (0, 210, 150)
        RED_BTN = (200, 60, 60)
        RED_BTN_H = (230, 80, 80)
        BLUE_BTN = (40, 100, 200)
        BLUE_BTN_H = (60, 130, 230)
        SPEED_ACTIVE = (60, 150, 255)
        VOLUME_TRACK = (50, 50, 80)
        VOLUME_FILL = (100, 200, 255)
        SHOP_GOLD = (255, 180, 50)
        OVERLAY = (13, 13, 28, 200)
        SCORE_PANEL = (17, 17, 38, 200)
        SCROLL_BAR = (60, 60, 100)
        SCROLL_BAR_BG = (30, 30, 50)
        VS_PLAYER = (0, 220, 160)
        VS_AI = (255, 150, 170)
        PURPLE = (140, 100, 200)

    # ==================================================================
    #  字体
    # ==================================================================
    def _find_font():
        candidates = []
        wd = "C:/Windows/Fonts"
        if os.path.isdir(wd):
            for fn in ["msyh.ttc","msyhbd.ttc","simhei.ttf","simsun.ttc"]:
                fp = os.path.join(wd, fn)
                if os.path.isfile(fp): candidates.append(fp)
        for d in ["/System/Library/Fonts","/Library/Fonts",os.path.expanduser("~/Library/Fonts")]:
            if os.path.isdir(d):
                for fn in ["PingFang.ttc","STHeiti Light.ttc","STHeiti Medium.ttc"]:
                    fp = os.path.join(d, fn)
                    if os.path.isfile(fp): candidates.append(fp)
        candidates += ["/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                       "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]
        for fp in candidates:
            if os.path.isfile(fp):
                try:
                    tf = pygame.font.Font(fp, 12)
                    if tf.render("中", True, (255,255,255)).get_width() > 5:
                        return fp
                except: pass
        return None

    FONT_PATH = _find_font()
    def _f(size):
        if FONT_PATH:
            try: return pygame.font.Font(FONT_PATH, size)
            except: pass
        return pygame.font.Font(None, size)

    FONT_TITLE = _f(54)
    FONT_LARGE = _f(32)
    FONT_MEDIUM = _f(24)
    FONT_SMALL = _f(19)
    FONT_TINY = _f(14)
    FONT_MICRO = _f(12)

    # ==================================================================
    #  速度预设
    # ==================================================================
    SPEED_PRESETS = [
        {"name":{"zh":"简单","en":"Easy","ja":"簡単"},"fps":5,"base_mult":0.8},
        {"name":{"zh":"普通","en":"Normal","ja":"普通"},"fps":9,"base_mult":1.0},
        {"name":{"zh":"困难","en":"Hard","ja":"難しい"},"fps":14,"base_mult":1.5},
        {"name":{"zh":"地狱","en":"Hell","ja":"地獄"},"fps":19,"base_mult":2.0},
    ]
    current_speed_index = 1
    # 边缘模式: 0=死亡, 1=滑动(贴墙滑行), 2=穿墙环绕
    EDGE_DEATH = 0
    EDGE_SLIDE = 1
    EDGE_WRAP = 2
    edge_mode = EDGE_SLIDE
    game_mode = "endless"
    TIMED_LIMIT = 180

    # ==================================================================
    #  状态常量
    # ==================================================================
    (ST_MENU, ST_PLAYING, ST_PAUSED, ST_GAME_OVER, ST_POPUP,
     ST_VS_PLAYING, ST_VS_PAUSED, ST_VS_OVER, ST_DIFFICULTY_SELECT,
     ST_LANG_SELECT, ST_THEME_SELECT, ST_RANK_PANEL,
     ST_DAILY_PLAYING, ST_DAILY_OVER) = range(14)

    game_state = ST_MENU
    popup_type = None
    flash_alpha = 0

    # ==================================================================
    #  存档
    # ==================================================================
    stats = {
        "total_score": 0, "redeemed_points": 0, "games_played": 0,
        "endless_high": 0, "timed_high": 0, "total_time": 0,
        "vs_wins": 0, "vs_losses": 0,
        "unlocked_skins": [0], "current_skin": 0,
        "effects_enabled": True, "score_version": 2,
        "unlocked_achievements": [], "total_food_eaten": 0,
        "themes_used": ["nord"], "speeds_played": [1],
        "xp": 0, "level": 1, "xp_streak": 0,
        "daily_first_win_date": "", "rank_rewards_unlocked": [],
        "daily_challenges": {}
    }
    current_score = 0
    session_time = 0

    def get_redeemable():
        return max(0, stats['total_score'] - stats['redeemed_points'] * 2 * SCORE_SCALE)

    def load_stats():
        nonlocal stats
        for fname in [SAVE_FILE, SAVE_FILE_BACKUP]:
            if os.path.exists(fname):
                try:
                    with open(fname, 'r', encoding='utf-8') as f:
                        loaded = json.load(f)
                        if loaded.get("score_version", 1) == 1:
                            loaded["total_score"] = loaded.get("total_score", 0) * SCORE_SCALE
                            loaded["endless_high"] = loaded.get("endless_high", 0) * SCORE_SCALE
                            loaded["timed_high"] = loaded.get("timed_high", 0) * SCORE_SCALE
                            loaded["score_version"] = 2
                        for k in stats:
                            if k not in loaded: loaded[k] = stats[k]
                        stats = loaded
                    return
                except: pass

    def save_stats():
        for fname in [SAVE_FILE, SAVE_FILE_BACKUP]:
            try:
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(stats, f, ensure_ascii=False, indent=2)
                return
            except: pass

    load_stats()
    if "unlocked_skins" in stats: unlocked_skins = stats["unlocked_skins"]
    if "current_skin" in stats: current_skin_id = stats["current_skin"]
    if "effects_enabled" in stats: effects_enabled = stats["effects_enabled"]
    if "unlocked_achievements" in stats:
        unlocked_achievements = set(stats["unlocked_achievements"])
    if 1 not in unlocked_skins and stats['total_time'] >= 180:
        unlocked_skins.append(1)
        stats["unlocked_skins"] = unlocked_skins
        save_stats()

    # ==================================================================
    #  按钮类
    # ==================================================================
    class Button:
        def __init__(self, x, y, w, h, text, font=FONT_MEDIUM,
                     bg="BTN_BG", hover="BTN_HOVER",
                     tc=None, accent=False, radius=10,
                     toggle=False, active_color=None):
            self.rect = pygame.Rect(x, y, w, h)
            self.text = text
            self.font = font
            self.bg_key = bg
            self.hover_key = hover
            self.tc_key = tc  # None = auto contrast
            self.accent = accent
            self.radius = radius
            self.toggle = toggle
            self.active_color_key = active_color if active_color else "SPEED_ACTIVE"
            self.is_hovered = False
            self.active = False

        def _get_color(self, key):
            """动态获取当前主题颜色，支持字符串键或直接颜色元组"""
            if isinstance(key, str):
                return getattr(Colors, key, (128, 128, 128))
            return key  # 直接返回颜色元组

        def _luminance(self, color):
            """计算颜色相对亮度 (0-1)"""
            r, g, b = color[0] / 255.0, color[1] / 255.0, color[2] / 255.0
            return 0.299 * r + 0.587 * g + 0.114 * b

        def _text_color(self, bg_color):
            """根据背景亮度自动选择文字颜色"""
            if self.tc_key:
                return self._get_color(self.tc_key)
            return Colors.TEXT_DARK if self._luminance(bg_color) > 0.5 else Colors.TEXT_MAIN

        def draw(self, surface):
            if self.toggle and self.active:
                color = self._get_color(self.active_color_key)
            elif self.accent:
                color = Colors.ACCENT_HOVER if self.is_hovered else Colors.ACCENT
            elif self.active and not self.toggle:
                color = Colors.SPEED_ACTIVE
            else:
                color = self._get_color(self.hover_key) if self.is_hovered else self._get_color(self.bg_key)
            shadow = self.rect.copy()
            shadow.y += 2
            pygame.draw.rect(surface, (0, 0, 0, 30), shadow, border_radius=self.radius)
            pygame.draw.rect(surface, color, self.rect, border_radius=self.radius)
            if self.active:
                pygame.draw.rect(surface, Colors.ACCENT, self.rect, 2, border_radius=self.radius)
            txt = self.font.render(self.text, True, self._text_color(color))
            surface.blit(txt, txt.get_rect(center=self.rect.center))

        def update(self, mp):
            self.is_hovered = self.rect.collidepoint(mp)

        def clicked(self, event):
            return (event.type == MOUSEBUTTONDOWN and event.button == 1
                    and self.rect.collidepoint(event.pos))

    class ScrollablePopup:
        def __init__(self, w, h):
            self.W = w
            self.H = h
            self.rect = pygame.Rect((WINDOW_WIDTH-w)//2, (WINDOW_HEIGHT-h)//2, w, h)
            self.scroll_offset = 0
            self.max_scroll = 0
            self.content_height = 0
            self.line_h = 20

        def reset_scroll(self):
            self.scroll_offset = 0
            self.max_scroll = 0

        def scroll(self, d):
            self.scroll_offset += d * 30
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

        def handle_wheel(self, event):
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.scroll(-1)
                    return True
                elif event.button == 5:
                    self.scroll(1)
                    return True
            return False

        def draw(self, surface, title_text, lines):
            self.content_height = len(lines) * self.line_h + 20
            visible_height = self.H - 90
            self.max_scroll = max(0, self.content_height - visible_height)
            ov = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
            ov.fill(Colors.OVERLAY)
            surface.blit(ov, (0,0))
            pygame.draw.rect(surface, Colors.BG_MID, self.rect, border_radius=16)
            pygame.draw.rect(surface, Colors.PANEL_BORDER, self.rect, 2, border_radius=16)
            ts = FONT_LARGE.render(title_text, True, Colors.ACCENT)
            surface.blit(ts, ts.get_rect(center=(self.rect.centerx, self.rect.y+30)))
            pygame.draw.line(surface, Colors.PANEL_BORDER,
                             (self.rect.x+30, self.rect.y+60),
                             (self.rect.right-30, self.rect.y+60), 1)
            cr = pygame.Rect(self.rect.x+4, self.rect.y+66, self.W-8, visible_height)
            surface.set_clip(cr)
            y0 = self.rect.y + 76 - self.scroll_offset
            for i, line in enumerate(lines):
                yy = y0 + i * self.line_h
                if yy+self.line_h < self.rect.y+66 or yy > self.rect.y+66+visible_height:
                    continue
                if line.startswith("═══"):
                    c = Colors.ACCENT
                elif line.startswith("  v"):
                    c = Colors.GOLD
                elif line.startswith("  [") or line.startswith("  ["):
                    c = Colors.TEXT_MAIN
                elif line.startswith("    "):
                    c = Colors.TEXT_DIM
                else:
                    c = Colors.TEXT_DIM
                txt = FONT_TINY.render(line, True, c)
                surface.blit(txt, (self.rect.x+32, yy))
            surface.set_clip(None)
            if self.max_scroll > 0:
                bx = self.rect.right - 14
                by = self.rect.y + 66
                bh = visible_height
                pygame.draw.rect(surface, Colors.SCROLL_BAR_BG, (bx,by,8,bh), border_radius=4)
                th = max(20, int(bh * (visible_height / self.content_height)))
                ty = by + int((self.scroll_offset / self.max_scroll) * (bh - th))
                pygame.draw.rect(surface, Colors.SCROLL_BAR, (bx,ty,8,th), border_radius=4)
            hint = FONT_MICRO.render(T("scroll_close"), True, Colors.TEXT_DARK)
            surface.blit(hint, hint.get_rect(center=(self.rect.centerx, self.rect.bottom-16)))

    # ==================================================================
    #  AI 对决策略函数 (BFS + 三级难度)
    # ==================================================================
    def bfs_find_path(start, target, obstacles):
        if start == target or not target:
            return None
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        queue = deque()
        queue.append((start, []))
        visited = {start}
        obstacle_set = set(obstacles)
        while queue:
            current, path = queue.popleft()
            if current == target:
                if path:
                    dx = path[0][0] - start[0]
                    dy = path[0][1] - start[1]
                    return (dx, dy)
                return None
            for dx, dy in directions:
                nx, ny = current[0] + dx, current[1] + dy
                next_pos = (nx, ny)
                if (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and
                    next_pos not in obstacle_set and next_pos not in visited):
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        return None

    def find_closest_food(head, foods):
        if not foods:
            return None
        min_dist = float('inf')
        closest = None
        for f in foods:
            dist = abs(f[0]-head[0]) + abs(f[1]-head[1])
            if dist < min_dist:
                min_dist = dist
                closest = f
        return closest

    def find_random_safe_dir(head, obstacles):
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(dirs)
        for d in dirs:
            nx, ny = head[0]+d[0], head[1]+d[1]
            if (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and
                (nx, ny) not in obstacles):
                return d
        return (1, 0)

    def find_safest_dir(head, obstacles):
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        best_dir = (1, 0)
        best_space = -1
        for d in dirs:
            nx, ny = head[0]+d[0], head[1]+d[1]
            if (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and
                (nx, ny) not in obstacles):
                space = 0
                q = deque()
                q.append((nx, ny))
                vis = {(nx, ny)}
                obs_set = set(obstacles)
                while q and space < 20:
                    cx, cy = q.popleft()
                    space += 1
                    for dd in dirs:
                        nnx, nny = cx+dd[0], cy+dd[1]
                        if (0 <= nnx < GRID_SIZE and 0 <= nny < GRID_SIZE and
                            (nnx, nny) not in obs_set and (nnx, nny) not in vis):
                            vis.add((nnx, nny))
                            q.append((nnx, nny))
                if space > best_space:
                    best_space = space
                    best_dir = d
        return best_dir

    def ai_get_direction(head, body, foods, player, difficulty):
        obstacles = set(body)
        if player:
            for seg in player:
                obstacles.add(seg)
        if difficulty == 0:
            if random.random() < 0.3:
                target = find_closest_food(head, foods)
                if target:
                    d = bfs_find_path(head, target, obstacles)
                    if d:
                        return d
            return find_random_safe_dir(head, obstacles)
        elif difficulty == 1:
            target = find_closest_food(head, foods)
            if target:
                d = bfs_find_path(head, target, obstacles)
                if d:
                    return d
            return find_safest_dir(head, obstacles)
        else:
            target = find_closest_food(head, foods)
            if target:
                d = bfs_find_path(head, target, obstacles)
                if d and random.random() < 0.8:
                    return d
            if player:
                d = bfs_find_path(head, player[0], obstacles)
                if d:
                    return d
            return find_safest_dir(head, obstacles)

    # ==================================================================
    #  AI 蛇实体
    # ==================================================================
    class AISnake:
        def __init__(self):
            self.snake = [
                (GRID_SIZE-3, GRID_SIZE-3),
                (GRID_SIZE-4, GRID_SIZE-3),
                (GRID_SIZE-5, GRID_SIZE-3)
            ]
            self.direction = (-1, 0)
            self.score = 0
            self.food_eaten = 0
            self.alive = True

        def reset(self):
            self.snake = [
                (GRID_SIZE-3, GRID_SIZE-3),
                (GRID_SIZE-4, GRID_SIZE-3),
                (GRID_SIZE-5, GRID_SIZE-3)
            ]
            self.direction = (-1, 0)
            self.score = 0
            self.food_eaten = 0
            self.alive = True

        def get_head(self):
            return self.snake[0]

    # ==================================================================
    #  对战管理器 (修复: 滑动模式改为穿墙环绕)
    # ==================================================================
    class VSGame:
        def __init__(self):
            self.player = None
            self.ai = AISnake()
            self.foods = []
            self.vs_game_over = False
            self.result = None
            self.player_score = 0
            self.player_direction = (1, 0)
            self.ai_difficulty = 1
            self.reset()

        def reset(self):
            self.player = self._create_player_snake()
            self.ai.reset()
            self.foods = []
            self.vs_game_over = False
            self.result = None
            self.player_score = 0
            self.player_direction = (1, 0)
            for _ in range(3):
                self._spawn_food()

        def _create_player_snake(self):
            return [(2, GRID_SIZE-3), (1, GRID_SIZE-3), (0, GRID_SIZE-3)]

        def _wrap_position(self, pos):
            """穿墙环绕：将坐标限制在网格内，从对侧出现"""
            x, y = pos
            if x < 0:
                x = GRID_SIZE - 1
            elif x >= GRID_SIZE:
                x = 0
            if y < 0:
                y = GRID_SIZE - 1
            elif y >= GRID_SIZE:
                y = 0
            return (x, y)

        def _get_all_obstacles(self, exclude_head_players=None):
            """exclude_head_players: 如果传了蛇列表，排除其头部"""
            obs = set()
            if self.player:
                for i, seg in enumerate(self.player):
                    if exclude_head_players is self.player and i == 0:
                        continue
                    obs.add(seg)
            if self.ai and self.ai.alive:
                for i, seg in enumerate(self.ai.snake):
                    if exclude_head_players is self.ai and i == 0:
                        continue
                    obs.add(seg)
            return obs

        def _spawn_food(self):
            obs = self._get_all_obstacles()
            for f in self.foods:
                obs.add(f)
            for _ in range(100):
                p = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
                if p not in obs:
                    self.foods.append(p)
                    return

        def _check_result(self):
            pa = self.player is not None
            aa = self.ai is not None and self.ai.alive
            if not pa and not aa:
                self.result = "draw"
            elif not pa:
                self.result = "lose"
            elif not aa:
                self.result = "win"
            if self.result is not None:
                self.vs_game_over = True

        @property
        def snake_set(self):
            """玩家蛇身位置集合（用于滑动碰撞检测）"""
            if self.player:
                return set(self.player)
            return set()

        def _is_out_of_bounds(self, pos):
            """检查坐标是否越界"""
            return pos[0] < 0 or pos[0] >= GRID_SIZE or pos[1] < 0 or pos[1] >= GRID_SIZE

        def _move_vs_snake(self, snake_obj, head, direction, score_list, is_player):
            """
            统一移动逻辑（支持三种边缘模式）
            """
            nonlocal edge_mode
            dx, dy = direction
            nh = (head[0] + dx, head[1] + dy)
            wrapped = False
            # ---- 边界检测 ----
            if self._is_out_of_bounds(nh):
                if edge_mode == EDGE_DEATH:
                    return False  # 死亡模式
                elif edge_mode == EDGE_WRAP:
                    nh = self._wrap_position(nh)
                    wrapped = True
                else:
                    # 滑动模式：尝试沿墙滑动（仅玩家蛇）
                    if is_player:
                        slide_dir, slide_pos = self._get_slide_direction_player(
                            head, direction)
                        if slide_pos is not None:
                            # 更新玩家方向
                            if is_player:
                                self.player_direction = slide_dir
                            nh = slide_pos
                        else:
                            return False  # 静止一帧
                    else:
                        # AI蛇在滑动模式下使用穿墙
                        nh = self._wrap_position(nh)
                        wrapped = True

            # ---- 碰撞检测（排除自身头部）----
            if is_player:
                obs = self._get_all_obstacles(exclude_head_players=self.player)
            else:
                obs = self._get_all_obstacles(exclude_head_players=self.ai)

            if nh in obs:
                return False

            # ---- 移动 ----
            snake_obj.insert(0, nh)
            ate = False
            for f in self.foods[:]:
                if nh == f:
                    self.foods.remove(f)
                    score_list[0] += 1
                    ate = True
                    break
            if not ate:
                snake_obj.pop()
            return True

        def _get_slide_direction_player(self, head, current_dir):
            """
            玩家蛇滑动：优先当前方向的垂直方向，其次反方向，最后静止
            """
            hx, hy = head
            dx, dy = current_dir
            # 碰撞检测排除头部（蛇在移动，头部位置会释放）
            body_set = set(self.player[1:]) if self.player else set()
            # 垂直方向
            perp_dirs = [(dy, dx), (-dy, -dx)]
            for pdx, pdy in perp_dirs:
                nx, ny = hx + pdx, hy + pdy
                if not self._is_out_of_bounds((nx, ny)) and (nx, ny) not in body_set:
                    return (pdx, pdy), (nx, ny)
            # 反方向
            rdx, rdy = -dx, -dy
            nx, ny = hx + rdx, hy + rdy
            if not self._is_out_of_bounds((nx, ny)) and (nx, ny) not in body_set:
                return (rdx, rdy), (nx, ny)
            return None, None

        def update(self):
            nonlocal edge_mode
            if self.vs_game_over:
                return
            # ---- 更新玩家 ----
            if self.player:
                score_ref = [self.player_score]
                alive = self._move_vs_snake(
                    self.player, self.player[0], self.player_direction,
                    score_ref, is_player=True
                )
                self.player_score = score_ref[0]
                if not alive:
                    self.player = None
            # ---- 更新 AI ----
            if self.ai and self.ai.alive:
                head = self.ai.get_head()
                direction = ai_get_direction(
                    head, self.ai.snake, self.foods,
                    self.player if self.player else None,
                    self.ai_difficulty
                )
                if direction:
                    self.ai.direction = direction
                score_ref = [self.ai.score]
                alive = self._move_vs_snake(
                    self.ai.snake, head, self.ai.direction,
                    score_ref, is_player=False
                )
                self.ai.score = score_ref[0]
                if not alive:
                    self.ai.alive = False
            # ---- 补充食物 ----
            while len(self.foods) < 3:
                self._spawn_food()
            self._check_result()

    vs_game = VSGame()
    vs_paused = False

    # ==================================================================
    #  SnakeGame (单人模式, 修复: 滑动改为穿墙环绕)
    # ==================================================================
    class SnakeGame:
        def __init__(self):
            self.reset()

        def reset(self):
            nonlocal second_food, extra_life_used, teleport_target, teleport_cooldown
            cx, cy = GRID_SIZE//2, GRID_SIZE//2
            self.snake = [(cx,cy), (cx-1,cy), (cx-2,cy)]
            self.direction = (1,0)
            self.next_direction = (1,0)
            self.input_queue = []
            self.score = 0
            self.food_eaten = 0
            self.food = self._spawn_food()
            self.game_over = False
            self.multiplier = 1
            self.mode = game_mode
            self.time_left = TIMED_LIMIT
            self.wall_slide_count = 0
            self.corners_visited = set()
            second_food = None
            extra_life_used = False
            teleport_target = None
            teleport_cooldown = 0

        def _wrap_position(self, pos):
            """穿墙环绕"""
            x, y = pos
            if x < 0:
                x = GRID_SIZE - 1
            elif x >= GRID_SIZE:
                x = 0
            if y < 0:
                y = GRID_SIZE - 1
            elif y >= GRID_SIZE:
                y = 0
            return (x, y)

        def _spawn_food(self, exclude=None):
            """生成食物，满盘时回退到全网格扫描"""
            occ = set(self.snake)
            if exclude and exclude in occ:
                occ.remove(exclude)
            if second_food:
                occ.add(second_food)
            # 先尝试随机
            for _ in range(100):
                p = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
                if p not in occ:
                    return p
            # 满盘回退：扫描所有空格
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    p = (x, y)
                    if p not in occ:
                        return p
            # 真满盘，返回 None（调用方需处理）
            return None

        def change_direction(self, nd):
            skin = SKINS[current_skin_id]
            if effects_enabled and skin["special"]["type"] == "reverse_controls":
                nd = (-nd[0], -nd[1])
            dx, dy = nd
            if len(self.snake) > 1:
                h = self.snake[0]
                if (h[0]+dx, h[1]+dy) == self.snake[1]:
                    return
            if not self.input_queue or self.input_queue[-1] != nd:
                if len(self.input_queue) < 4:
                    self.input_queue.append(nd)

        def _try_dir(self, nd):
            h = self.snake[0]
            nx, ny = h[0]+nd[0], h[1]+nd[1]
            if (nx, ny) in self.snake[1:]:
                return False
            self.direction = nd
            self.next_direction = nd
            self.input_queue.clear()
            return True

        def reverse_snake(self):
            if len(self.snake) > 1:
                self.snake.reverse()
                if len(self.snake) >= 2:
                    h = self.snake[0]
                    h2 = self.snake[1]
                    self.direction = (h[0]-h2[0], h[1]-h2[1])
                    self.next_direction = self.direction
                    self.input_queue.clear()

        def revive_snake(self):
            """DeepSeek-Flash: 随机位置全新复活"""
            nonlocal extra_life_used
            if extra_life_used:
                return False
            rx = random.randint(2, GRID_SIZE-3)
            ry = random.randint(2, GRID_SIZE-3)
            occupied = set(self.snake)
            attempts = 0
            while (rx, ry) in occupied and attempts < 50:
                rx = random.randint(2, GRID_SIZE-3)
                ry = random.randint(2, GRID_SIZE-3)
                attempts += 1
            dirs = [(1,0), (-1,0), (0,1), (0,-1)]
            d = random.choice(dirs)
            self.snake = [(rx, ry), (rx-d[0], ry-d[1]), (rx-2*d[0], ry-2*d[1])]
            self.direction = d
            self.next_direction = d
            self.input_queue.clear()
            self.game_over = False
            extra_life_used = True
            self.score = int(self.score * 0.7)
            return True

        def _is_out_of_bounds(self, pos):
            """检查坐标是否越界"""
            return pos[0] < 0 or pos[0] >= GRID_SIZE or pos[1] < 0 or pos[1] >= GRID_SIZE

        def _get_slide_direction(self, head, current_dir, input_dir):
            """
            滑动模式：蛇头撞墙时尝试沿墙滑动。
            优先级：玩家输入方向 > 当前方向 > 反方向 > 静止
            返回: (新方向, 新头部位置)
            """
            hx, hy = head
            # 尝试玩家输入方向（如果不撞墙）
            if input_dir:
                nx, ny = hx + input_dir[0], hy + input_dir[1]
                if not self._is_out_of_bounds((nx, ny)) and (nx, ny) not in self.snake[1:]:
                    return input_dir, (nx, ny)
            # 尝试当前方向（如果不撞墙）— 这里应该已经撞了，所以尝试垂直方向
            # 实际上当前方向一定是撞墙的，所以尝试与当前方向垂直的两个方向
            dx, dy = current_dir
            # 垂直方向：将 (dx,dy) 旋转90度得到两个垂直方向
            perp_dirs = [(dy, dx), (-dy, -dx)]
            # 先尝试与输入方向一致的垂直方向
            if input_dir and input_dir in perp_dirs:
                perp_dirs.remove(input_dir)
                perp_dirs.insert(0, input_dir)
            for pdx, pdy in perp_dirs:
                nx, ny = hx + pdx, hy + pdy
                if not self._is_out_of_bounds((nx, ny)) and (nx, ny) not in self.snake[1:]:
                    return (pdx, pdy), (nx, ny)
            # 所有垂直方向都被挡，尝试反方向
            rdx, rdy = -dx, -dy
            nx, ny = hx + rdx, hy + rdy
            if not self._is_out_of_bounds((nx, ny)) and (nx, ny) not in self.snake[1:]:
                return (rdx, rdy), (nx, ny)
            # 完全被包围，静止
            return None, None

        def update(self, dt_sec):
            nonlocal edge_mode, session_time, second_food, flash_alpha, teleport_cooldown
            if self.game_over:
                return True
            if teleport_cooldown > 0:
                teleport_cooldown -= 1
            if self.mode == "timed":
                self.time_left -= dt_sec
                if self.time_left <= 0:
                    self.time_left = 0
                    self.game_over = True
                    return True
            # 获取玩家输入方向（如果有）
            input_dir = None
            if self.input_queue:
                input_dir = self.input_queue.pop(0)
                self.next_direction = input_dir
            self.direction = self.next_direction
            hx, hy = self.snake[0]
            dx, dy = self.direction
            nh = (hx+dx, hy+dy)
            wrapped = False
            sliding = False
            # ---- 边界检测 ----
            if self._is_out_of_bounds(nh):
                if edge_mode == EDGE_DEATH:
                    if (effects_enabled and
                        SKINS[current_skin_id]["special"]["type"] == "extra_life" and
                        not extra_life_used):
                        if self.revive_snake():
                            return False
                    self.game_over = True
                    return True
                elif edge_mode == EDGE_WRAP:
                    # 穿墙环绕
                    nh = self._wrap_position(nh)
                    wrapped = True
                else:
                    # 滑动模式：尝试沿墙滑动
                    slide_dir, slide_pos = self._get_slide_direction(
                        (hx, hy), self.direction, input_dir)
                    if slide_pos is not None:
                        self.direction = slide_dir
                        self.next_direction = slide_dir
                        nh = slide_pos
                        sliding = True
                        self.wall_slide_count += 1
                    else:
                        # 完全被挡，静止一帧
                        return False

            # ---- 碰撞检测（排除头部自身）----
            if not wrapped and not sliding:
                if nh in self.snake:
                    if (effects_enabled and
                        SKINS[current_skin_id]["special"]["type"] == "extra_life" and
                        not extra_life_used):
                        if self.revive_snake():
                            return False
                    self.game_over = True
                    return True
            elif wrapped:
                if nh in self.snake[1:]:
                    if (effects_enabled and
                        SKINS[current_skin_id]["special"]["type"] == "extra_life" and
                        not extra_life_used):
                        if self.revive_snake():
                            return False
                    self.game_over = True
                    return True
            else:
                # 滑动模式已做过碰撞检测，无需重复
                pass

            # ---- 移动 ----
            self.snake.insert(0, nh)
            # 追踪角落访问
            if nh == (0, 0) or nh == (0, GRID_SIZE-1) or nh == (GRID_SIZE-1, 0) or nh == (GRID_SIZE-1, GRID_SIZE-1):
                self.corners_visited.add(nh)
            ate = False
            ate_main = False  # 标记是否吃了主食物
            if nh == self.food:
                ate = True
                ate_main = True
            elif second_food and nh == second_food:
                ate = True
                second_food = None
            if not ate and effects_enabled and SKINS[current_skin_id]["special"]["type"] == "food_attract":
                ar = SKINS[current_skin_id]["special"]["params"]
                head = self.snake[0]
                fx, fy = self.food
                if abs(fx - head[0]) <= ar and abs(fy - head[1]) <= ar:
                    ate = True
                    ate_main = True
                if not ate and second_food:
                    fx2, fy2 = second_food
                    if abs(fx2 - head[0]) <= ar and abs(fy2 - head[1]) <= ar:
                        ate = True
                        second_food = None
            if ate:
                self.food_eaten += 1
                award_xp(5, "eat_food")
                self.multiplier = 2 ** (self.food_eaten // 10)
                bm = SPEED_PRESETS[current_speed_index]["base_mult"]
                sm = 1.0
                if (effects_enabled and
                    SKINS[current_skin_id]["special"]["type"] == "score_multiply"):
                    sm = SKINS[current_skin_id]["special"]["params"]
                cm = 1.0
                if (effects_enabled and
                    SKINS[current_skin_id]["special"]["type"] == "reverse_controls"):
                    cm = SKINS[current_skin_id]["special"]["params"]
                raw = self.multiplier * bm * sm * cm
                add_score = max(SCORE_SCALE, int(raw * SCORE_SCALE))
                self.score += add_score
                # 修复：只有吃了主食物时才重新生成主食物
                if ate_main:
                    self.food = self._spawn_food()
                if (effects_enabled and
                    SKINS[current_skin_id]["special"]["type"] == "double_food" and
                    second_food is None):
                    second_food = self._spawn_food()
                if (effects_enabled and
                    SKINS[current_skin_id]["special"]["type"] == "time_add" and
                    self.mode == "timed"):
                    self.time_left += random.randint(
                        SKINS[current_skin_id]["special"]["params"][0],
                        SKINS[current_skin_id]["special"]["params"][1]
                    )
            else:
                self.snake.pop()
            return False

        def get_skin_color(self, si, tn, ms):
            skin = SKINS[current_skin_id]
            if skin["rainbow"]:
                h = (ms/2000 + si/tn) % 1.0
                r, g, b = colorsys.hsv_to_rgb(h, 0.5, 0.85)
                return (int(r*255), int(g*255), int(b*255))
            else:
                if si == 0:
                    return skin["head_color"]
                t = si / max(tn, 1)
                base = skin["body_color"]
                return tuple(min(255, int(c*(1-t*0.3))) for c in base)

        def draw(self, surface):
            tms = pygame.time.get_ticks()
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    r = (GRID_X+x*CELL_SIZE, GRID_Y+y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    c = Colors.GRID_EVEN if (x+y)%2==0 else Colors.GRID_ODD
                    pygame.draw.rect(surface, c, r)
            foods = [self.food]
            if second_food:
                foods.append(second_food)
            for fx, fy in foods:
                fc = (GRID_X+fx*CELL_SIZE+CELL_SIZE//2,
                      GRID_Y+fy*CELL_SIZE+CELL_SIZE//2)
                for rad in range(14, 6, -2):
                    g = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
                    pygame.draw.circle(g, (*Colors.FOOD_MAIN, max(0,40-rad*2)), fc, rad)
                    surface.blit(g, (0,0))
                pygame.draw.circle(surface, Colors.FOOD_MAIN, fc, 9)
                pygame.draw.circle(surface, Colors.FOOD_GLOW, fc, 5)
            seg_n = len(self.snake)
            for i, (sx, sy) in enumerate(self.snake):
                color = self.get_skin_color(i, seg_n, tms)
                r = (GRID_X+sx*CELL_SIZE+2, GRID_Y+sy*CELL_SIZE+2,
                     CELL_SIZE-4, CELL_SIZE-4)
                if i == 0:
                    pygame.draw.rect(surface, color, r, border_radius=7)
                    dx, dy = self.direction
                    e1 = (GRID_X+sx*CELL_SIZE+7, GRID_Y+sy*CELL_SIZE+7)
                    e2 = (GRID_X+sx*CELL_SIZE+CELL_SIZE-9, GRID_Y+sy*CELL_SIZE+7)
                    pygame.draw.circle(surface, (255,255,255), e1, 4)
                    pygame.draw.circle(surface, (255,255,255), e2, 4)
                    pygame.draw.circle(surface, (20,20,20),
                                       (e1[0]+dx, e1[1]+dy), 2)
                    pygame.draw.circle(surface, (20,20,20),
                                       (e2[0]+dx, e2[1]+dy), 2)
                else:
                    pygame.draw.rect(surface, color, r, border_radius=5)
            pygame.draw.rect(surface, Colors.PANEL_BORDER,
                             (GRID_X, GRID_Y, GRID_PX, GRID_PX), 2, border_radius=6)

    snake_game = SnakeGame()

    # ==================================================================
    #  缓存遮罩表面 (优化: 避免每帧创建)
    # ==================================================================
    _overlay_cache = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    _overlay_cache.fill(Colors.OVERLAY)
    _score_panel_cache = pygame.Surface((160, 160), pygame.SRCALPHA)
    _score_panel_cache.fill(Colors.SCORE_PANEL)

    # ==================================================================
    #  弹窗对象
    # ==================================================================
    help_popup = ScrollablePopup(560, 420)
    dev_popup = ScrollablePopup(580, 400)
    update_popup = ScrollablePopup(600, 520)
    stats_popup = ScrollablePopup(560, 400)
    ach_popup = ScrollablePopup(520, 440)
    # ==================================================================
    #  按钮创建
    # ==================================================================
    SBW, SBH, SG = 95, 38, 8
    SPEED_TOTAL = 4*SBW + 3*SG
    sx0 = WINDOW_WIDTH//2 - SPEED_TOTAL//2
    speed_btns = []
    for i, sp in enumerate(SPEED_PRESETS):
        btn = Button(sx0+i*(SBW+SG), 205, SBW, SBH,
                     sp["name"][current_lang], FONT_SMALL, radius=6)
        btn.speed_index = i
        btn.active = (i == current_speed_index)
        speed_btns.append(btn)

    speed_card_rect = pygame.Rect((WINDOW_WIDTH-440)//2, 150, 440, 106)
    mode_btn = Button(WINDOW_WIDTH//2-200, 285, 180, 38,
                      T("mode_prefix") + T("mode_endless"), FONT_SMALL, radius=8,
                      toggle=True, active_color="BLUE_BTN")
    mode_btn.active = True
    edge_btn = Button(WINDOW_WIDTH//2+20, 285, 180, 38,
                      T("edge_slide"), FONT_SMALL, radius=8,
                      toggle=True, active_color="GREEN_BTN")
    edge_btn.active = True
    # 边缘模式名称和颜色映射
    _edge_mode_names = {0: "edge_death", 1: "edge_slide", 2: "edge_wrap"}
    _edge_mode_colors = {0: "RED_BTN", 1: "GREEN_BTN", 2: "BLUE_BTN"}
    start_btn = Button((WINDOW_WIDTH-170)//2, 350, 170, 50,
                       T("start"), FONT_MEDIUM, accent=True, radius=12)
    vs_btn = Button((WINDOW_WIDTH-170)//2, 410, 170, 46,
                    T("vs_mode"), FONT_SMALL, radius=8,
                    toggle=True, active_color="ACCENT")

    btn_y = 530
    help_btn = Button(WINDOW_WIDTH//2-230, btn_y, 100, 36,
                      T("help"), FONT_SMALL, radius=8)
    stats_btn = Button(WINDOW_WIDTH//2-115, btn_y, 100, 36,
                       T("stats"), FONT_SMALL, radius=8)
    update_btn = Button(WINDOW_WIDTH//2, btn_y, 100, 36,
                        T("update"), FONT_SMALL, radius=8)
    dev_btn = Button(WINDOW_WIDTH//2+115, btn_y, 100, 36,
                     T("dev"), FONT_SMALL, radius=8)

    shop_btn = Button(15, 160, 100, 42, T("shop"), FONT_SMALL,
                      bg=(60,40,20), hover=(80,60,30),
                      tc=Colors.SHOP_GOLD, radius=8)
    skin_btn = Button(15, 210, 100, 42, T("skin_shop"), FONT_SMALL,
                      bg=(40,40,60), hover=(55,55,80),
                      tc=Colors.ACCENT, radius=8)
    effects_btn = Button(15, 260, 100, 36, T("effects_on"), FONT_SMALL,
                         radius=8, toggle=True, active_color="GREEN_BTN")
    effects_btn.active = effects_enabled

    mx = WINDOW_WIDTH - 160
    my = WINDOW_HEIGHT - 50
    music_btn = Button(mx, my, 90, 36, T("music"), FONT_SMALL, radius=8)
    lang_btn = Button(mx-5, my-42, 100, 36,
                      {"zh": "中文", "en": "English", "ja": "日本語"}[current_lang],
                      FONT_SMALL, radius=8,
                      toggle=True, active_color="SPEED_ACTIVE")
    lang_btn.active = True
    theme_btn = Button(mx-5, my-84, 100, 36,
                       T("theme"), FONT_SMALL, radius=8,
                       toggle=True, active_color="PURPLE")
    theme_btn.active = True
    ach_btn = Button(mx-5, my-126, 100, 36,
                     T("achievements"), FONT_SMALL, radius=8,
                     toggle=True, active_color="GOLD")
    ach_btn.active = True
    rank_btn = Button(mx-5, my-168, 100, 36,
                      T("rank_title"), FONT_SMALL, radius=8,
                      toggle=True, active_color="GOLD")
    rank_btn.active = True
    daily_btn = Button(mx-5, my-210, 100, 36,
                       T("daily_challenge"), FONT_SMALL, radius=8,
                       toggle=True, active_color="GREEN_BTN")
    daily_btn.active = True

    pause_btn = Button(GRID_X+GRID_PX+15, GRID_Y, 70, 34,
                       T("pause"), FONT_SMALL, radius=8)
    end_btn = Button(GRID_X+GRID_PX+15, GRID_Y+48, 70, 34,
                     T("end"), FONT_SMALL,
                     bg=Colors.RED_BTN, hover=Colors.RED_BTN_H, radius=8)
    go_restart = Button((WINDOW_WIDTH-170)//2, 340, 170, 46,
                        T("restart"), FONT_MEDIUM, accent=True, radius=12)
    go_menu = Button((WINDOW_WIDTH-170)//2, 400, 170, 46,
                     T("back_menu"), FONT_MEDIUM, radius=12)

    vs_restart = Button((WINDOW_WIDTH-170)//2, 300, 170, 46,
                        T("restart"), FONT_MEDIUM, accent=True, radius=12)
    vs_menu = Button((WINDOW_WIDTH-170)//2, 360, 170, 46,
                     T("back_menu"), FONT_MEDIUM, radius=12)

    # 音乐弹窗按钮
    MPW, MPH = 480, 430
    mpr = pygame.Rect((WINDOW_WIDTH-MPW)//2, (WINDOW_HEIGHT-MPH)//2, MPW, MPH)
    mby = mpr.y + 130
    mp_prev = Button(mpr.x+80, mby, 70, 36, T("prev"), FONT_SMALL, radius=8)
    mp_play = Button(mpr.x+175, mby, 90, 36,
                     T("pause_btn") if music_playing else T("play"),
                     FONT_SMALL, accent=True, radius=8)
    mp_next = Button(mpr.x+290, mby, 70, 36, T("next"), FONT_SMALL, radius=8)

    # 商店弹窗矩形
    SPW, SPH = 500, 420
    shop_pr = pygame.Rect((WINDOW_WIDTH-SPW)//2, (WINDOW_HEIGHT-SPH)//2, SPW, SPH)
    SKPW, SKPH = 480, 560
    skin_pr = pygame.Rect((WINDOW_WIDTH-SKPW)//2, (WINDOW_HEIGHT-SKPH)//2, SKPW, SKPH)

    # ==================================================================
    #  商店弹窗
    # ==================================================================
    shop_btns_created = False
    eb = e10 = e50 = eall = None
    shop_msg = ""
    shop_msg_timer = 0

    def draw_shop_popup(surface):
        nonlocal shop_btns_created, eb, e10, e50, eall, shop_msg, shop_msg_timer
        surface.blit(_overlay_cache, (0, 0))
        pygame.draw.rect(surface, Colors.BG_MID, shop_pr, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, shop_pr, 2, border_radius=16)
        t = FONT_LARGE.render(T("shop_title"), True, Colors.SHOP_GOLD)
        surface.blit(t, t.get_rect(center=(shop_pr.centerx, shop_pr.y+28)))
        pygame.draw.line(surface, Colors.PANEL_BORDER,
                         (shop_pr.x+30, shop_pr.y+58),
                         (shop_pr.right-30, shop_pr.y+58), 1)
        rt = FONT_TINY.render(T("exchange_rate"), True, Colors.TEXT_DIM)
        surface.blit(rt, (shop_pr.x+40, shop_pr.y+72))
        cy = shop_pr.y + 105
        cw, ch, cgap = 110, 80, 10
        tcw = 3*cw + 2*cgap
        sx = shop_pr.x + (SPW-tcw)//2
        rdm = get_redeemable()//SCORE_SCALE
        rded = stats['redeemed_points']
        ts = stats['total_score']//SCORE_SCALE
        for i, (lb, vl, cl) in enumerate([
            (T("redeemable"), str(rdm), Colors.GREEN_BTN),
            (T("redeemed"), str(rded), Colors.RED_BTN),
            (T("total"), str(ts), Colors.SHOP_GOLD)
        ]):
            cx = sx + i*(cw+cgap)
            pygame.draw.rect(surface, Colors.PANEL_BG, (cx,cy,cw,ch), border_radius=10)
            pygame.draw.rect(surface, Colors.PANEL_BORDER, (cx,cy,cw,ch), 1, border_radius=10)
            l = FONT_MICRO.render(lb, True, Colors.TEXT_DIM)
            surface.blit(l, l.get_rect(center=(cx+cw//2, cy+18)))
            v = FONT_LARGE.render(vl, True, cl)
            surface.blit(v, v.get_rect(center=(cx+cw//2, cy+50)))
        iy = shop_pr.y + 200
        ct = FONT_SMALL.render(T("current_redeemable", rdm), True, Colors.GOLD)
        surface.blit(ct, (shop_pr.x+35, iy))
        ht = FONT_SMALL.render(T("history_total", ts), True, Colors.TEXT_DIM)
        surface.blit(ht, (shop_pr.right-35-ht.get_width(), iy))
        if not shop_btns_created:
            eb = Button(shop_pr.x+140, shop_pr.y+245, 220, 46,
                        T("exchange_1"), FONT_MEDIUM, accent=True, radius=12)
            by_ = shop_pr.y + 305
            bw = 140
            bgap = 25
            tbw = 3*bw + 2*bgap
            bsx = shop_pr.x + (SPW-tbw)//2
            e10 = Button(bsx, by_, bw, 32, T("exchange_10"), FONT_SMALL, radius=8)
            e50 = Button(bsx+bw+bgap, by_, bw, 32, T("exchange_50"), FONT_SMALL, radius=8)
            eall = Button(bsx+2*(bw+bgap), by_, bw, 32, T("exchange_all"), FONT_SMALL, radius=8)
            shop_btns_created = True
        eb.draw(surface)
        e10.draw(surface)
        e50.draw(surface)
        eall.draw(surface)
        if shop_msg_timer > 0:
            m = FONT_TINY.render(shop_msg, True, Colors.GOLD)
            surface.blit(m, m.get_rect(center=(shop_pr.centerx, shop_pr.y+365)))
        h = FONT_MICRO.render(T("click_close"), True, Colors.TEXT_DARK)
        surface.blit(h, h.get_rect(center=(shop_pr.centerx, shop_pr.bottom-14)))
        return eb, e10, e50, eall

    # ==================================================================
    #  皮肤商店弹窗
    # ==================================================================
    skin_scroll_offset = 0
    skin_max_scroll = 0
    skin_confirm_popup = False
    skin_confirm_id = None

    # 皮肤确认按钮
    skin_confirm_yes = Button(0, 0, 80, 32, T("confirm_yes"), FONT_SMALL,
                              bg="GREEN_BTN", hover="GREEN_BTN_H", radius=6)
    skin_confirm_no = Button(0, 0, 80, 32, T("confirm_no"), FONT_SMALL,
                             bg="RED_BTN", hover="RED_BTN_H", radius=6)

    def draw_skin_popup(surface):
        nonlocal skin_scroll_offset, skin_max_scroll, skin_confirm_popup, skin_confirm_id
        surface.blit(_overlay_cache, (0, 0))
        pygame.draw.rect(surface, Colors.BG_MID, skin_pr, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, skin_pr, 2, border_radius=16)
        t = FONT_LARGE.render(T("skin_title"), True, Colors.ACCENT)
        surface.blit(t, t.get_rect(center=(skin_pr.centerx, skin_pr.y+25)))
        pygame.draw.line(surface, Colors.PANEL_BORDER,
                         (skin_pr.x+20, skin_pr.y+55),
                         (skin_pr.right-20, skin_pr.y+55), 1)
        item_h = 90
        header_h = 60
        footer_h = 36
        visible_h = SKPH - header_h - footer_h
        total_h = len(SKINS) * item_h
        skin_max_scroll = max(0, total_h - visible_h)
        scroll_bar_visual_w = 8
        scroll_bar_click_w = 18
        content_x = skin_pr.x + 15
        content_w = SKPW - 30 - scroll_bar_click_w - 4
        cr = pygame.Rect(content_x, skin_pr.y+header_h, content_w, visible_h)
        surface.set_clip(cr)
        tms = pygame.time.get_ticks()
        for idx, skin in enumerate(SKINS):
            yy = skin_pr.y + header_h + idx*item_h - skin_scroll_offset
            if yy+item_h < skin_pr.y+header_h or yy > skin_pr.y+header_h+visible_h:
                continue
            card_r = pygame.Rect(content_x, yy, content_w, item_h-6)
            owned = skin["id"] in unlocked_skins
            cur = skin["id"] == current_skin_id
            if cur:
                bgc, bdc = (25,50,80), Colors.GOLD
            elif owned:
                bgc, bdc = (20,30,45), Colors.GREEN_BTN
            else:
                bgc, bdc = (15,20,35), Colors.RED_BTN
            pygame.draw.rect(surface, bgc, card_r, border_radius=8)
            pygame.draw.rect(surface, bdc, card_r, 2, border_radius=8)
            px = card_r.x + 12
            py = card_r.y + 10
            if skin["rainbow"]:
                c0 = snake_game.get_skin_color(0,3,tms)
                c1 = snake_game.get_skin_color(1,3,tms)
                c2 = snake_game.get_skin_color(2,3,tms)
            else:
                c0 = skin["head_color"]
                c1 = skin["body_color"]
                c2 = tuple(min(255,int(c*0.85)) for c in skin["body_color"])
            sq = 20
            pygame.draw.rect(surface, c0, (px,py,sq,sq), border_radius=4)
            pygame.draw.rect(surface, c1, (px+sq+4,py,sq,sq), border_radius=4)
            pygame.draw.rect(surface, c2, (px+2*(sq+4),py,sq,sq), border_radius=4)
            nm_text = skin["name"][current_lang]
            nm = FONT_SMALL.render(nm_text, True, Colors.TEXT_MAIN)
            surface.blit(nm, (px, py+sq+6))
            dc = FONT_TINY.render(skin["special"]["desc"][current_lang], True, Colors.TEXT_DIM)
            max_desc_w = content_w - 120
            if dc.get_width() > max_desc_w:
                while len(nm_text) > 10:
                    nm_text = nm_text[:-1]
                    dc = FONT_TINY.render(nm_text+"...", True, Colors.TEXT_DIM)
                    if dc.get_width() <= max_desc_w:
                        break
            surface.blit(dc, (px, py+sq+28))
            if cur:
                st = FONT_SMALL.render(T("equipped"), True, Colors.GOLD)
            elif owned:
                st = FONT_SMALL.render(T("owned"), True, Colors.GREEN_BTN)
            elif skin.get("unlock_condition") == "time_3min":
                st = FONT_TINY.render(T("unlock_time"), True, Colors.TEXT_DIM)
            elif skin.get("unlock_condition", "").startswith("level_"):
                lvl = skin["unlock_condition"].split("_")[1]
                st = FONT_SMALL.render(f"Lv.{lvl}", True, Colors.TEXT_DIM)
            elif skin["price"] == -1:
                st = FONT_TINY.render(skin["special"]["desc"][current_lang], True, Colors.TEXT_DIM)
            else:
                st = FONT_SMALL.render(T("price_pts", skin["price"]), True, Colors.SHOP_GOLD)
            surface.blit(st, st.get_rect(right=card_r.right-12, top=card_r.y+10))
        surface.set_clip(None)
        if skin_max_scroll > 0:
            bx = skin_pr.right - 20 + (scroll_bar_click_w - scroll_bar_visual_w) // 2
            by = skin_pr.y + header_h
            bh = visible_h
            pygame.draw.rect(surface, Colors.SCROLL_BAR_BG, (skin_pr.right - 20, by, scroll_bar_click_w, bh), border_radius=4)
            th = max(24, int(bh * min(1.0, visible_h / total_h)))
            ty = by + int((skin_scroll_offset / skin_max_scroll) * (bh - th)) if skin_max_scroll > 0 else by
            pygame.draw.rect(surface, Colors.SCROLL_BAR, (bx, ty, scroll_bar_visual_w, th), border_radius=4)
        # 绘制确认弹窗
        if skin_confirm_popup and skin_confirm_id is not None:
            sk = SKINS[skin_confirm_id]
            crw, crh = 300, 140
            cpr = pygame.Rect((WINDOW_WIDTH-crw)//2, (WINDOW_HEIGHT-crh)//2, crw, crh)
            pygame.draw.rect(surface, Colors.BG_MID, cpr, border_radius=12)
            pygame.draw.rect(surface, Colors.PANEL_BORDER, cpr, 2, border_radius=12)
            nm = sk["name"][current_lang]
            pt = sk["price"]
            txt1 = FONT_SMALL.render(T("confirm_buy", nm), True, Colors.TEXT_MAIN)
            surface.blit(txt1, txt1.get_rect(center=(cpr.centerx, cpr.y+35)))
            txt2 = FONT_TINY.render(T("cost_pts", pt), True, Colors.TEXT_DIM)
            surface.blit(txt2, txt2.get_rect(center=(cpr.centerx, cpr.y+65)))
            skin_confirm_yes.rect.center = (cpr.centerx-50, cpr.y+105)
            skin_confirm_no.rect.center = (cpr.centerx+50, cpr.y+105)
            skin_confirm_yes.draw(surface)
            skin_confirm_no.draw(surface)
        hint = FONT_MICRO.render(T("skin_hint"), True, Colors.TEXT_DARK)
        surface.blit(hint, hint.get_rect(center=(skin_pr.centerx, skin_pr.bottom-12)))

    # ==================================================================
    #  音乐弹窗
    # ==================================================================
    def draw_music_popup(surface):
        surface.blit(_overlay_cache, (0, 0))
        pygame.draw.rect(surface, Colors.BG_MID, mpr, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, mpr, 2, border_radius=16)
        tt = FONT_LARGE.render(T("music_title"), True, Colors.ACCENT)
        surface.blit(tt, tt.get_rect(center=(mpr.centerx, mpr.y+28)))
        pygame.draw.line(surface, Colors.PANEL_BORDER,
                         (mpr.x+30, mpr.y+58), (mpr.right-30, mpr.y+58), 1)
        cn = music_names[music_index] if music_total>0 else T("no_music")
        if len(cn) > 35:
            cn = cn[:32] + "..."
        np = FONT_SMALL.render(f"{T('current_playing')}: {cn}", True, Colors.TEXT_MAIN)
        surface.blit(np, (mpr.x+30, mpr.y+72))
        sc = Colors.GREEN_BTN if music_playing else Colors.TEXT_DIM
        st = FONT_SMALL.render(
            f"{T('status')}: {T('playing_status') if music_playing else T('paused_status')}",
            True, sc)
        surface.blit(st, (mpr.x+30, mpr.y+98))
        mp_prev.draw(surface)
        mp_play.draw(surface)
        mp_next.draw(surface)
        vl = FONT_SMALL.render(T("volume"), True, Colors.TEXT_DIM)
        surface.blit(vl, (mpr.x+30, mpr.y+180))
        sx = mpr.x + 80
        sy = mpr.y + 200
        sw = 320
        sh = 10
        pygame.draw.rect(surface, Colors.VOLUME_TRACK, (sx,sy,sw,sh), border_radius=5)
        fw = int(sw * music_volume)
        if fw > 0:
            pygame.draw.rect(surface, Colors.VOLUME_FILL, (sx,sy,fw,sh), border_radius=5)
        pygame.draw.rect(surface, Colors.ACCENT, (sx+fw-6, sy-4, 12, 18), border_radius=4)
        vp = FONT_TINY.render(f"{int(music_volume*100)}%", True, Colors.TEXT_MAIN)
        surface.blit(vp, (mpr.x+30, mpr.y+218))
        tl = FONT_SMALL.render(T("track_list"), True, Colors.TEXT_DIM)
        surface.blit(tl, (mpr.x+30, mpr.y+245))
        lx = mpr.x + 30
        ly = mpr.y + 265
        lw = MPW - 80
        lh = 120
        ih = 22
        clip = pygame.Rect(lx, ly, lw, lh)
        surface.set_clip(clip)
        ms = max(0, music_total*ih - lh)
        for i, name in enumerate(music_names):
            yy = ly + i*ih - music_list_scroll
            if yy+ih < ly or yy > ly+lh:
                continue
            dn = name if len(name)<=28 else name[:25]+"..."
            mk = "▶ " if i==music_index else "   "
            c = Colors.GOLD if i==music_index else Colors.TEXT_DIM
            txt = FONT_TINY.render(f"{mk}{i+1}. {dn}", True, c)
            surface.blit(txt, (lx+5, yy+2))
        surface.set_clip(None)
        if ms > 0:
            bx = lx + lw + 5
            by = ly
            bh = lh
            pygame.draw.rect(surface, Colors.SCROLL_BAR_BG, (bx,by,6,bh), border_radius=3)
            th = max(12, int(bh*(lh/(music_total*ih))))
            ty = by + int((music_list_scroll/ms)*(bh-th))
            pygame.draw.rect(surface, Colors.SCROLL_BAR, (bx,ty,6,th), border_radius=3)
        h = FONT_MICRO.render(T("scroll_close"), True, Colors.TEXT_DARK)
        surface.blit(h, h.get_rect(center=(mpr.centerx, mpr.bottom-16)))

    # ==================================================================
    #  段位面板
    # ==================================================================
    rank_popup = ScrollablePopup(500, 400)

    def draw_rank_panel(surface):
        nonlocal rank_popup
        cw, ch = 500, 400
        cpr = pygame.Rect((WINDOW_WIDTH - cw) // 2, (WINDOW_HEIGHT - ch) // 2, cw, ch)
        surface.blit(_overlay_cache, (0, 0))
        pygame.draw.rect(surface, Colors.BG_MID, cpr, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, cpr, 2, border_radius=16)
        title = FONT_LARGE.render(T("rank_title"), True, Colors.GOLD)
        surface.blit(title, title.get_rect(center=(cpr.centerx, cpr.y + 28)))
        pygame.draw.line(surface, Colors.PANEL_BORDER,
                         (cpr.x + 20, cpr.y + 55), (cpr.right - 20, cpr.y + 55), 1)
        # 段位信息
        level = stats.get("level", 1)
        total_xp = stats.get("xp", 0)
        cur_level, progress, need = xp_to_level(total_xp)
        tier = get_rank_tier(level)
        tier_name = T(tier["name_key"])
        tier_color = tier["color"]
        # 段位图标
        icon_x = cpr.centerx - 40
        icon_y = cpr.y + 90
        pygame.draw.rect(surface, tier_color, (icon_x, icon_y, 80, 50), border_radius=8)
        tier_surf = FONT_SMALL.render(tier_name, True, (30, 30, 30))
        surface.blit(tier_surf, tier_surf.get_rect(center=(cpr.centerx, icon_y + 25)))
        # 等级
        lvl_surf = FONT_LARGE.render(f"Lv.{level}", True, Colors.TEXT_MAIN)
        surface.blit(lvl_surf, lvl_surf.get_rect(center=(cpr.centerx, icon_y + 80)))
        # XP进度条
        bar_x = cpr.x + 40
        bar_y = icon_y + 110
        bar_w = cw - 80
        bar_h = 20
        pygame.draw.rect(surface, Colors.VOLUME_TRACK, (bar_x, bar_y, bar_w, bar_h), border_radius=10)
        if need > 0:
            fill_w = int(bar_w * progress / need)
            if fill_w > 0:
                pygame.draw.rect(surface, tier_color, (bar_x, bar_y, fill_w, bar_h), border_radius=10)
        progress_text = T("rank_progress", progress, need)
        prog_surf = FONT_TINY.render(progress_text, True, Colors.TEXT_DIM)
        surface.blit(prog_surf, prog_surf.get_rect(center=(cpr.centerx, bar_y + 35)))
        # 连胜
        streak = stats.get("xp_streak", 0)
        if streak > 0:
            streak_text = T("rank_streak", streak)
            streak_surf = FONT_TINY.render(streak_text, True, Colors.GOLD)
            surface.blit(streak_surf, streak_surf.get_rect(center=(cpr.centerx, bar_y + 55)))
        # 段位里程碑
        milestones_y = bar_y + 80
        milestones = [
            (5, "rank_bronze"), (10, "rank_silver"), (25, "rank_gold"),
            (35, "rank_platinum"), (45, "rank_diamond"), (999, "rank_master")
        ]
        for i, (lv, name_key) in enumerate(milestones):
            by = milestones_y + i * 28
            if by > cpr.bottom - 40:
                break
            tier_info = get_rank_tier(lv if lv < 999 else 50)
            mc = tier_info["color"]
            mn = T(name_key)
            reached = level >= lv
            if not reached and i > 0 and level >= milestones[i-1][0]:
                # 当前等级段位
                pygame.draw.rect(surface, mc, (cpr.x + 30, by, 20, 20), border_radius=4)
            elif reached:
                pygame.draw.rect(surface, mc, (cpr.x + 30, by, 20, 20), border_radius=4)
            else:
                pygame.draw.rect(surface, Colors.TEXT_DARK, (cpr.x + 30, by, 20, 20), border_radius=4)
            ms = FONT_TINY.render(f"Lv.{lv} {mn}", True, Colors.TEXT_MAIN if reached else Colors.TEXT_DIM)
            surface.blit(ms, (cpr.x + 60, by + 2))
        hint = FONT_MICRO.render(T("scroll_close"), True, Colors.TEXT_DARK)
        surface.blit(hint, hint.get_rect(center=(cpr.centerx, cpr.bottom - 12)))

    # ==================================================================
    #  每日挑战
    # ==================================================================
    daily_popup_rect = pygame.Rect(0, 0, 0, 0)

    def draw_daily_challenge_info(surface):
        nonlocal daily_popup_rect
        cw, ch = 420, 340
        cpr = pygame.Rect((WINDOW_WIDTH - cw) // 2, (WINDOW_HEIGHT - ch) // 2, cw, ch)
        daily_popup_rect = cpr
        surface.blit(_overlay_cache, (0, 0))
        pygame.draw.rect(surface, Colors.BG_MID, cpr, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, cpr, 2, border_radius=16)
        title = FONT_LARGE.render(T("daily_challenge"), True, Colors.GREEN_BTN)
        surface.blit(title, title.get_rect(center=(cpr.centerx, cpr.y + 28)))
        pygame.draw.line(surface, Colors.PANEL_BORDER,
                         (cpr.x + 20, cpr.y + 55), (cpr.right - 20, cpr.y + 55), 1)
        # 今日挑战
        date_str = get_daily_date_str()
        challenge = generate_daily_challenge(date_str)
        mod = DAILY_MODIFIERS[challenge["modifier_id"]]
        mod_name = T(mod["name_key"])
        mod_desc = T(mod["desc_key"])
        # 规则名称
        rule_title = FONT_SMALL.render(T("daily_modifier"), True, Colors.ACCENT)
        surface.blit(rule_title, (cpr.x + 30, cpr.y + 70))
        rule_name_surf = FONT_MEDIUM.render(mod_name, True, Colors.TEXT_MAIN)
        surface.blit(rule_name_surf, (cpr.x + 30, cpr.y + 95))
        # 描述
        desc_surf = FONT_TINY.render(mod_desc, True, Colors.TEXT_DIM)
        surface.blit(desc_surf, (cpr.x + 30, cpr.y + 125))
        # 得分倍率
        mult = mod.get("score_mult", 1.0)
        if mult > 1.0:
            mult_text = f"Score x{mult}"
            mult_surf = FONT_TINY.render(mult_text, True, Colors.GOLD)
            surface.blit(mult_surf, (cpr.x + 30, cpr.y + 150))
        # 奖励说明
        reward_title = FONT_SMALL.render(T("daily_rewards"), True, Colors.ACCENT)
        surface.blit(reward_title, (cpr.x + 30, cpr.y + 180))
        rewards_y = cpr.y + 205
        reward_items = [
            T("daily_reward_participate"),
            T("daily_reward_score"),
        ]
        if mult > 1.0:
            reward_items.append(T("daily_reward_modifier"))
        for i, item in enumerate(reward_items):
            item_surf = FONT_TINY.render(f"  - {item}", True, Colors.TEXT_DIM)
            surface.blit(item_surf, (cpr.x + 30, rewards_y + i * 20))
        # 历史最佳
        daily_records = stats.get("daily_challenges", {})
        best_score = daily_records.get(date_str, {}).get("score", 0)
        if best_score > 0:
            best_text = f"{T('daily_best')}: {best_score // SCORE_SCALE}"
            best_surf = FONT_TINY.render(best_text, True, Colors.GOLD)
            surface.blit(best_surf, (cpr.x + 30, cpr.bottom - 45))
        hint = FONT_MICRO.render(T("click_close"), True, Colors.TEXT_DARK)
        surface.blit(hint, hint.get_rect(center=(cpr.centerx, cpr.bottom - 12)))

    def draw_daily_result(surface, score, is_record, xp_earned=0):
        cw, ch = 360, 220
        cpr = pygame.Rect((WINDOW_WIDTH - cw) // 2, (WINDOW_HEIGHT - ch) // 2, cw, ch)
        surface.blit(_overlay_cache, (0, 0))
        pygame.draw.rect(surface, Colors.BG_MID, cpr, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, cpr, 2, border_radius=16)
        title = FONT_LARGE.render(T("daily_result"), True, Colors.GREEN_BTN)
        surface.blit(title, title.get_rect(center=(cpr.centerx, cpr.y + 30)))
        # 得分
        score_text = f"{score // SCORE_SCALE}"
        score_surf = FONT_TITLE.render(score_text, True, Colors.GOLD)
        surface.blit(score_surf, score_surf.get_rect(center=(cpr.centerx, cpr.y + 80)))
        if is_record:
            rec_surf = FONT_SMALL.render(T("new_record"), True, Colors.ACCENT)
            surface.blit(rec_surf, rec_surf.get_rect(center=(cpr.centerx, cpr.y + 115)))
        # XP奖励
        if xp_earned > 0:
            xp_text = T("daily_xp_bonus", xp_earned)
            xp_surf = FONT_TINY.render(xp_text, True, Colors.GOLD)
            surface.blit(xp_surf, xp_surf.get_rect(center=(cpr.centerx, cpr.y + 145)))
        hint = FONT_MICRO.render(T("click_close"), True, Colors.TEXT_DARK)
        surface.blit(hint, hint.get_rect(center=(cpr.centerx, cpr.bottom - 15)))

    # ==================================================================
    #  AI 难度选择弹窗
    # ==================================================================
    def draw_difficulty_popup(surface):
        nonlocal diff_rects
        cw, ch = 400, 280
        cpr = pygame.Rect((WINDOW_WIDTH-cw)//2, (WINDOW_HEIGHT-ch)//2, cw, ch)
        surface.blit(_overlay_cache, (0, 0))
        pygame.draw.rect(surface, Colors.BG_MID, cpr, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, cpr, 2, border_radius=16)
        title = FONT_LARGE.render(T("diff_select"), True, Colors.ACCENT)
        surface.blit(title, title.get_rect(center=(cpr.centerx, cpr.y+30)))
        btn_w, btn_h = 160, 40
        start_y = cpr.y + 80
        diff_rects = []
        colors = [Colors.GREEN_BTN, Colors.BLUE_BTN, Colors.RED_BTN]
        for i, diff in enumerate(AI_DIFFICULTIES):
            by = start_y + i * (btn_h + 30)
            bx = cpr.x + (cw-btn_w)//2
            pygame.draw.rect(surface, colors[i], (bx, by, btn_w, btn_h), border_radius=8)
            txt = FONT_SMALL.render(diff["name"][current_lang], True, Colors.TEXT_MAIN)
            surface.blit(txt, txt.get_rect(center=(bx+btn_w//2, by+btn_h//2)))
            desc = FONT_TINY.render(diff["desc"][current_lang], True, Colors.TEXT_DIM)
            surface.blit(desc, desc.get_rect(center=(cpr.centerx, by+btn_h+12)))
            diff_rects.append(pygame.Rect(bx, by, btn_w, btn_h))
        hint = FONT_MICRO.render(T("click_close"), True, Colors.TEXT_DARK)
        surface.blit(hint, hint.get_rect(center=(cpr.centerx, cpr.bottom-20)))
        return diff_rects

    # ==================================================================
    #  语言选择弹窗
    # ==================================================================
    lang_rects = []

    def draw_lang_popup(surface):
        nonlocal lang_rects
        cw, ch = 300, 240
        cpr = pygame.Rect((WINDOW_WIDTH-cw)//2, (WINDOW_HEIGHT-ch)//2, cw, ch)
        surface.blit(_overlay_cache, (0, 0))
        pygame.draw.rect(surface, Colors.BG_MID, cpr, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, cpr, 2, border_radius=16)
        title = FONT_LARGE.render(T("lang_select"), True, Colors.ACCENT)
        surface.blit(title, title.get_rect(center=(cpr.centerx, cpr.y+30)))
        btn_w, btn_h = 180, 38
        start_y = cpr.y + 70
        lang_rects = []
        lang_ids = ["zh", "en", "ja"]
        lang_names = {"zh": "中文", "en": "English", "ja": "日本語"}
        colors = [Colors.GREEN_BTN, Colors.BLUE_BTN, Colors.PURPLE]
        for i, lid in enumerate(lang_ids):
            by = start_y + i * (btn_h + 15)
            bx = cpr.x + (cw-btn_w)//2
            rect = pygame.Rect(bx, by, btn_w, btn_h)
            bgc = colors[i] if current_lang != lid else Colors.SPEED_ACTIVE
            pygame.draw.rect(surface, bgc, rect, border_radius=8)
            pygame.draw.rect(surface, Colors.ACCENT if current_lang == lid else Colors.PANEL_BORDER, rect, 2 if current_lang == lid else 1, border_radius=8)
            txt = FONT_SMALL.render(lang_names[lid], True, Colors.TEXT_MAIN)
            surface.blit(txt, txt.get_rect(center=(bx+btn_w//2, by+btn_h//2)))
            lang_rects.append(rect)
        hint = FONT_MICRO.render(T("click_close"), True, Colors.TEXT_DARK)
        surface.blit(hint, hint.get_rect(center=(cpr.centerx, cpr.bottom-16)))
        return lang_rects

    # ==================================================================
    #  主题选择弹窗
    # ==================================================================
    theme_rects = []

    def draw_theme_popup(surface):
        nonlocal theme_rects
        theme_ids = list(THEMES.keys())
        n_themes = len(theme_ids)
        item_w, item_h = 340, 44
        gap = 6
        header_h = 65
        footer_h = 30
        ch = header_h + n_themes * (item_h + gap) - gap + footer_h + 10
        cw = 420
        cpr = pygame.Rect((WINDOW_WIDTH - cw) // 2, (WINDOW_HEIGHT - ch) // 2, cw, ch)
        surface.blit(_overlay_cache, (0, 0))
        pygame.draw.rect(surface, Colors.BG_MID, cpr, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, cpr, 2, border_radius=16)
        title = FONT_LARGE.render(T("theme"), True, Colors.ACCENT)
        surface.blit(title, title.get_rect(center=(cpr.centerx, cpr.y + 28)))
        pygame.draw.line(surface, Colors.PANEL_BORDER,
                         (cpr.x + 20, cpr.y + 55), (cpr.right - 20, cpr.y + 55), 1)
        start_y = cpr.y + header_h
        theme_rects = []
        swatch_colors = ["ACCENT", "FOOD_MAIN", "GREEN_BTN", "RED_BTN", "BLUE_BTN"]
        swatch_x_gap = 26
        swatch_size = 18
        swatch_offset_x = 12
        text_offset_x = swatch_offset_x + len(swatch_colors) * swatch_x_gap + 15
        for i, tid in enumerate(theme_ids):
            by = start_y + i * (item_h + gap)
            bx = cpr.x + (cw - item_w) // 2
            rect = pygame.Rect(bx, by, item_w, item_h)
            selected = (current_theme == tid)
            bgc = Colors.SPEED_ACTIVE if selected else Colors.BG_DARK
            pygame.draw.rect(surface, bgc, rect, border_radius=8)
            border_w = 2 if selected else 1
            border_c = Colors.ACCENT if selected else Colors.PANEL_BORDER
            pygame.draw.rect(surface, border_c, rect, border_w, border_radius=8)
            # 绘制主题色块预览（左侧）
            px = bx + swatch_offset_x
            py_cen = by + item_h // 2
            for j, ckey in enumerate(swatch_colors):
                c = THEMES[tid].get(ckey, (128, 128, 128))
                sx = px + j * swatch_x_gap
                pygame.draw.rect(surface, c, (sx, py_cen - swatch_size // 2, swatch_size, swatch_size), border_radius=3)
            # 主题名称（右侧，与色块分离）
            tname = THEMES[tid]["name"].get(current_lang, THEMES[tid]["name"]["en"])
            max_text_w = item_w - text_offset_x - 10
            txt_color = Colors.TEXT_MAIN
            txt = FONT_SMALL.render(tname, True, txt_color)
            if txt.get_width() > max_text_w:
                while len(tname) > 1 and txt.get_width() > max_text_w:
                    tname = tname[:-1]
                    txt = FONT_SMALL.render(tname + "...", True, txt_color)
            surface.blit(txt, (bx + text_offset_x, py_cen - txt.get_height() // 2))
            theme_rects.append(rect)
        hint = FONT_MICRO.render(T("click_close"), True, Colors.TEXT_DARK)
        surface.blit(hint, hint.get_rect(center=(cpr.centerx, cpr.bottom - 10)))
        return theme_rects

    # ==================================================================
    #  成就面板
    # ==================================================================
    def draw_achievement_popup(surface):
        cw, ch = 520, 440
        cpr = pygame.Rect((WINDOW_WIDTH - cw) // 2, (WINDOW_HEIGHT - ch) // 2, cw, ch)
        surface.blit(_overlay_cache, (0, 0))
        pygame.draw.rect(surface, Colors.BG_MID, cpr, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, cpr, 2, border_radius=16)
        title = FONT_LARGE.render(T("achievements"), True, Colors.GOLD)
        surface.blit(title, title.get_rect(center=(cpr.centerx, cpr.y + 28)))
        pygame.draw.line(surface, Colors.PANEL_BORDER,
                         (cpr.x + 20, cpr.y + 55), (cpr.right - 20, cpr.y + 55), 1)
        # 统计
        unlocked_count = len(unlocked_achievements)
        total_count = len(ACHIEVEMENTS)
        stat_text = f"{unlocked_count}/{total_count}"
        stat_surf = FONT_SMALL.render(stat_text, True, Colors.TEXT_DIM)
        surface.blit(stat_surf, stat_surf.get_rect(center=(cpr.centerx, cpr.y + 72)))
        # 成就列表
        list_x = cpr.x + 20
        list_y = cpr.y + 85
        list_w = cw - 40
        item_h = 50
        visible_h = ch - 130
        cr = pygame.Rect(list_x, list_y, list_w, visible_h)
        surface.set_clip(cr)
        for i, ach in enumerate(ACHIEVEMENTS):
            by = list_y + i * (item_h + 4) - ach_popup.scroll_offset
            if by + item_h < list_y or by > list_y + visible_h:
                continue
            unlocked = ach["id"] in unlocked_achievements
            is_secret = ach["secret"] and not unlocked
            # 背景
            bg_rect = pygame.Rect(list_x, by, list_w, item_h)
            bg_c = Colors.SPEED_ACTIVE if unlocked else Colors.BG_DARK
            pygame.draw.rect(surface, bg_c, bg_rect, border_radius=6)
            pygame.draw.rect(surface, Colors.ACCENT if unlocked else Colors.PANEL_BORDER, bg_rect, 1, border_radius=6)
            # 图标（固定宽度区域）
            icon_char = "?" if is_secret else ach["icon"]
            icon_surf = FONT_TINY.render(icon_char, True, Colors.TEXT_MAIN if unlocked else Colors.TEXT_DIM)
            icon_x = list_x + 8
            surface.blit(icon_surf, (icon_x, by + (item_h - 14) // 2))
            # 名称（从固定位置开始，避免与图标重叠）
            name_text = "???" if is_secret else ach["name"].get(current_lang, ach["name"]["en"])
            name_surf = FONT_SMALL.render(name_text, True, Colors.TEXT_MAIN if unlocked else Colors.TEXT_DIM)
            name_x = list_x + 45
            surface.blit(name_surf, (name_x, by + 5))
            # 描述
            desc_text = "???" if is_secret else ach["desc"].get(current_lang, ach["desc"]["en"])
            desc_surf = FONT_TINY.render(desc_text, True, Colors.TEXT_DIM)
            surface.blit(desc_surf, (name_x, by + 26))
            # 积分奖励
            pts = ach.get("points", 0)
            if pts > 0 and not is_secret:
                pts_text = f"+{pts}pts"
                pts_surf = FONT_TINY.render(pts_text, True, Colors.GOLD if unlocked else Colors.TEXT_DIM)
                surface.blit(pts_surf, (list_x + list_w - 55, by + 16))
        surface.set_clip(None)
        # 滚动条
        total_h = len(ACHIEVEMENTS) * (item_h + 4)
        if total_h > visible_h:
            bx = cpr.right - 12
            by_s = list_y
            bh = visible_h
            pygame.draw.rect(surface, Colors.SCROLL_BAR_BG, (bx, by_s, 6, bh), border_radius=3)
            th = max(15, int(bh * (visible_h / total_h)))
            ty = by_s + int((ach_popup.scroll_offset / (total_h - visible_h)) * (bh - th))
            pygame.draw.rect(surface, Colors.SCROLL_BAR, (bx, ty, 6, th), border_radius=3)
        hint = FONT_MICRO.render(T("scroll_close"), True, Colors.TEXT_DARK)
        surface.blit(hint, hint.get_rect(center=(cpr.centerx, cpr.bottom - 12)))

    # ==================================================================
    #  统计信息
    # ==================================================================
    def get_stat_lines():
        h = stats['total_time'] // 3600
        m = (stats['total_time'] % 3600) // 60
        s = stats['total_time'] % 60
        ts = f"{h}h{m}m{s}s" if current_lang=="en" else f"{h}时{m}分{s}秒"
        if h == 0:
            ts = f"{m}m{s}s" if current_lang=="en" else f"{m}分{s}秒"
        avg = stats['total_score'] // max(stats['games_played'], 1) // SCORE_SCALE
        return [
            f"[ {T('stats_title')} ]", "",
            f"  {T('total_score')}: {stats['total_score']//SCORE_SCALE}",
            f"  {T('games_played')}: {stats['games_played']}",
            f"  {T('play_time')}: {ts}",
            f"  {T('avg_score')}: {avg}", "",
            f"═══   {T('mode_title')}   ═══", "",
            f"  {T('max_endless')}: {fmt_score(stats['endless_high'])}",
            f"  {T('max_timed')}: {fmt_score(stats['timed_high'])}",
        ]

    # ==================================================================
    #  绘制主菜单
    # ==================================================================
    def draw_menu(surface):
        for i in range(0, WINDOW_WIDTH, 60):
            ls = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(ls, (*Colors.BG_LIGHT, 4), (i,0), (i,WINDOW_HEIGHT), 1)
            surface.blit(ls, (0,0))
        t = FONT_TITLE.render(T("title"), True, Colors.ACCENT)
        tr = t.get_rect(center=(WINDOW_WIDTH//2, 55))
        ts = FONT_TITLE.render(T("title"), True, (0,0,0,30))
        tsr = ts.get_rect(center=(WINDOW_WIDTH//2+2, 57))
        surface.blit(ts, tsr)
        surface.blit(t, tr)
        sub = FONT_SMALL.render(T("subtitle"), True, Colors.TEXT_DIM)
        surface.blit(sub, sub.get_rect(center=(WINDOW_WIDTH//2, 100)))
        pygame.draw.rect(surface, Colors.PANEL_BG, speed_card_rect, border_radius=10)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, speed_card_rect, 1, border_radius=10)
        lbl = FONT_SMALL.render(T("speed"), True, Colors.TEXT_DIM)
        surface.blit(lbl, lbl.get_rect(center=(WINDOW_WIDTH//2, speed_card_rect.y+18)))
        for b in speed_btns:
            b.draw(surface)
        mode_btn.draw(surface)
        edge_btn.draw(surface)
        start_btn.draw(surface)
        vs_btn.draw(surface)
        sy = 490
        sr = pygame.Rect(WINDOW_WIDTH//2-200, sy-12, 400, 42)
        pygame.draw.rect(surface, Colors.PANEL_BG, sr, border_radius=8)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, sr, 1, border_radius=8)
        st = FONT_MICRO.render(
            f"{T('total_score')}:{stats['total_score']//SCORE_SCALE}  "
            f"{T('max_endless')}:{fmt_score(stats['endless_high'])}  "
            f"{T('max_timed')}:{fmt_score(stats['timed_high'])}  "
            f"{T('games_played')}:{stats['games_played']}",
            True, Colors.TEXT_MAIN)
        surface.blit(st, st.get_rect(center=(WINDOW_WIDTH//2, sy+9)))
        shop_btn.draw(surface)
        skin_btn.draw(surface)
        effects_btn.draw(surface)
        help_btn.draw(surface)
        stats_btn.draw(surface)
        update_btn.draw(surface)
        dev_btn.draw(surface)
        lang_btn.draw(surface)
        theme_btn.draw(surface)
        ach_btn.draw(surface)
        rank_btn.draw(surface)
        daily_btn.draw(surface)
        music_btn.draw(surface)
        if music_total > 0:
            tip = FONT_MICRO.render(f"{T('track_label')}{music_index+1}/{music_total}",
                                    True, Colors.TEXT_DARK)
            surface.blit(tip, (mx-75, my+10))
        ver = FONT_MICRO.render("v7.10", True, Colors.TEXT_DARK)
        surface.blit(ver, (WINDOW_WIDTH-60, WINDOW_HEIGHT-18))

    # ==================================================================
    #  单人游戏界面
    # ==================================================================
    def draw_playing(surface, paused=False):
        snake_game.draw(surface)
        pygame.draw.rect(surface, Colors.PANEL_BG, (0,0,WINDOW_WIDTH,TOP_BAR_HEIGHT))
        pygame.draw.line(surface, Colors.BG_LIGHT, (0,TOP_BAR_HEIGHT),
                         (WINDOW_WIDTH,TOP_BAR_HEIGHT), 2)
        skn = SKINS[current_skin_id]["name"][current_lang]
        skt = FONT_MICRO.render(f"{T('skin_label')}: {skn}", True, Colors.TEXT_DIM)
        surface.blit(skt, (18,18))
        sc = FONT_MEDIUM.render(f"{T('score')}: {fmt_score(snake_game.score)}",
                                True, Colors.TEXT_MAIN)
        surface.blit(sc, (18,40))
        mc = Colors.GOLD if snake_game.multiplier>1 else Colors.TEXT_DIM
        mu = FONT_TINY.render(f"{T('multiplier')}: {snake_game.multiplier}x", True, mc)
        surface.blit(mu, (18,66))
        mn = T("mode_endless") if snake_game.mode=="endless" else T("mode_timed")
        mt = FONT_TINY.render(f"{T('mode_label')}: {mn}", True, Colors.TEXT_DIM)
        surface.blit(mt, (GRID_X+5, 16))
        if snake_game.mode == "timed":
            mi = int(snake_game.time_left // 60)
            se = int(snake_game.time_left % 60)
            ts = f"{T('time_label')}: {mi:02d}:{se:02d}"
            tc = Colors.RED_BTN if snake_game.time_left<30 else Colors.GOLD
            tt = FONT_MEDIUM.render(ts, True, tc)
            surface.blit(tt, (GRID_X+5, 40))
        px = GRID_X + GRID_PX + 15
        pw = WINDOW_WIDTH - px - 15
        py_ = GRID_Y + 95
        ph = 160
        ps = pygame.Surface((pw, ph), pygame.SRCALPHA)
        ps.fill(Colors.SCORE_PANEL)
        surface.blit(ps, (px, py_))
        pt = FONT_SMALL.render(T("real_time"), True, Colors.ACCENT)
        surface.blit(pt, (px+6, py_+6))
        p1 = FONT_TINY.render(f"{T('current')}: {fmt_score(snake_game.score)}",
                              True, Colors.TEXT_MAIN)
        surface.blit(p1, (px+6, py_+32))
        hs = stats["endless_high"] if snake_game.mode=="endless" else stats["timed_high"]
        p2 = FONT_TINY.render(f"{T('high_label')}: {fmt_score(hs)}", True, Colors.GOLD)
        surface.blit(p2, (px+6, py_+52))
        p3 = FONT_TINY.render(f"{T('food_label')}: {snake_game.food_eaten}",
                              True, Colors.TEXT_DIM)
        surface.blit(p3, (px+6, py_+72))
        pause_btn.draw(surface)
        end_btn.draw(surface)
        if paused:
            po = pygame.Surface((GRID_PX,GRID_PX), pygame.SRCALPHA)
            po.fill((0,0,0,180))
            surface.blit(po, (GRID_X,GRID_Y))
            pt2 = FONT_TITLE.render(T("paused_label"), True, Colors.TEXT_MAIN)
            surface.blit(pt2, pt2.get_rect(center=(GRID_X+GRID_PX//2, GRID_Y+GRID_PX//2)))

    # ==================================================================
    #  对战游戏界面
    # ==================================================================
    def draw_vs_playing(surface, paused=False):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                r = (GRID_X+x*CELL_SIZE, GRID_Y+y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                c = Colors.GRID_EVEN if (x+y)%2==0 else Colors.GRID_ODD
                pygame.draw.rect(surface, c, r)
        for fx, fy in vs_game.foods:
            fc = (GRID_X+fx*CELL_SIZE+CELL_SIZE//2, GRID_Y+fy*CELL_SIZE+CELL_SIZE//2)
            for rad in range(14,6,-2):
                g = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
                pygame.draw.circle(g, (*Colors.FOOD_MAIN, max(0,40-rad*2)), fc, rad)
                surface.blit(g, (0,0))
            pygame.draw.circle(surface, Colors.FOOD_MAIN, fc, 9)
            pygame.draw.circle(surface, Colors.FOOD_GLOW, fc, 5)
        if vs_game.player:
            tms = pygame.time.get_ticks()
            for i, (sx, sy) in enumerate(vs_game.player):
                color = snake_game.get_skin_color(i, len(vs_game.player), tms)
                r = (GRID_X+sx*CELL_SIZE+2, GRID_Y+sy*CELL_SIZE+2, CELL_SIZE-4, CELL_SIZE-4)
                if i == 0:
                    pygame.draw.rect(surface, color, r, border_radius=7)
                    dx, dy = vs_game.player_direction
                    e1 = (GRID_X+sx*CELL_SIZE+7, GRID_Y+sy*CELL_SIZE+7)
                    e2 = (GRID_X+sx*CELL_SIZE+CELL_SIZE-9, GRID_Y+sy*CELL_SIZE+7)
                    pygame.draw.circle(surface, (255,255,255), e1, 4)
                    pygame.draw.circle(surface, (255,255,255), e2, 4)
                    pygame.draw.circle(surface, (20,20,20), (e1[0]+dx, e1[1]+dy), 2)
                    pygame.draw.circle(surface, (20,20,20), (e2[0]+dx, e2[1]+dy), 2)
                else:
                    pygame.draw.rect(surface, color, r, border_radius=5)
        if vs_game.ai and vs_game.ai.alive:
            for i, (sx, sy) in enumerate(vs_game.ai.snake):
                if i == 0:
                    color = (255, 100, 100)
                else:
                    t = i / max(len(vs_game.ai.snake), 1)
                    color = (int(255*(1-t*0.5)), 60, 60)
                r = (GRID_X+sx*CELL_SIZE+2, GRID_Y+sy*CELL_SIZE+2, CELL_SIZE-4, CELL_SIZE-4)
                if i == 0:
                    pygame.draw.rect(surface, color, r, border_radius=7)
                    dx, dy = vs_game.ai.direction
                    e1 = (GRID_X+sx*CELL_SIZE+7, GRID_Y+sy*CELL_SIZE+7)
                    e2 = (GRID_X+sx*CELL_SIZE+CELL_SIZE-9, GRID_Y+sy*CELL_SIZE+7)
                    pygame.draw.circle(surface, (255,255,255), e1, 4)
                    pygame.draw.circle(surface, (255,255,255), e2, 4)
                    pygame.draw.circle(surface, (20,20,20), (e1[0]+dx, e1[1]+dy), 2)
                    pygame.draw.circle(surface, (20,20,20), (e2[0]+dx, e2[1]+dy), 2)
                else:
                    pygame.draw.rect(surface, color, r, border_radius=5)
        pygame.draw.rect(surface, Colors.PANEL_BORDER,
                         (GRID_X, GRID_Y, GRID_PX, GRID_PX), 2, border_radius=6)
        pygame.draw.rect(surface, Colors.PANEL_BG, (0,0,WINDOW_WIDTH,TOP_BAR_HEIGHT))
        pygame.draw.line(surface, Colors.BG_LIGHT, (0,TOP_BAR_HEIGHT),
                         (WINDOW_WIDTH,TOP_BAR_HEIGHT), 2)
        pl = FONT_MEDIUM.render(T("vs_player"), True, Colors.VS_PLAYER)
        surface.blit(pl, (18,12))
        ps = FONT_SMALL.render(f"{T('score')}: {vs_game.player_score}",
                               True, Colors.TEXT_MAIN)
        surface.blit(ps, (18,45))
        al = FONT_MEDIUM.render(T("vs_ai"), True, Colors.VS_AI)
        surface.blit(al, (WINDOW_WIDTH-180, 12))
        as_ = FONT_SMALL.render(f"{T('score')}: {vs_game.ai.score if vs_game.ai else 0}",
                                True, Colors.TEXT_MAIN)
        surface.blit(as_, (WINDOW_WIDTH-180, 45))
        fc = FONT_TINY.render(f"{T('vs_food')}: {len(vs_game.foods)}",
                              True, Colors.TEXT_DIM)
        surface.blit(fc, (WINDOW_WIDTH//2-30, 30))
        if paused:
            po = pygame.Surface((GRID_PX,GRID_PX), pygame.SRCALPHA)
            po.fill((0,0,0,180))
            surface.blit(po, (GRID_X,GRID_Y))
            pt2 = FONT_TITLE.render(T("paused_label"), True, Colors.TEXT_MAIN)
            surface.blit(pt2, pt2.get_rect(center=(GRID_X+GRID_PX//2, GRID_Y+GRID_PX//2)))

    # ==================================================================
    #  对战结算界面
    # ==================================================================
    def draw_vs_over(surface):
        draw_vs_playing(surface, False)
        surface.blit(_overlay_cache, (0, 0))
        if vs_game.result == "win":
            rt = T("vs_win")
            rc = Colors.VS_PLAYER
        elif vs_game.result == "lose":
            rt = T("vs_lose")
            rc = Colors.VS_AI
        else:
            rt = T("vs_draw")
            rc = Colors.TEXT_DIM
        go = FONT_TITLE.render(rt, True, rc)
        surface.blit(go, go.get_rect(center=(WINDOW_WIDTH//2, 70)))
        sc = pygame.Rect(WINDOW_WIDTH//2-170, 100, 340, 100)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, sc, 1, border_radius=12)
        p_t = FONT_SMALL.render(f"{T('vs_player')}: {vs_game.player_score}",
                                True, Colors.VS_PLAYER)
        surface.blit(p_t, (sc.x+20, sc.y+20))
        a_t = FONT_SMALL.render(f"{T('vs_ai')}: {vs_game.ai.score if vs_game.ai else 0}",
                                True, Colors.VS_AI)
        surface.blit(a_t, (sc.x+20, sc.y+55))
        vs_restart.draw(surface)
        vs_menu.draw(surface)

    # ==================================================================
    #  单人结算界面
    # ==================================================================
    def draw_game_over(surface):
        snake_game.draw(surface)
        nonlocal flash_alpha
        if flash_alpha > 0:
            fs = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
            fs.fill((255,255,255,flash_alpha))
            surface.blit(fs, (0,0))
        surface.blit(_overlay_cache, (0, 0))
        go = FONT_TITLE.render(T("game_over"), True, Colors.ACCENT)
        gor = go.get_rect(center=(WINDOW_WIDTH//2, 70))
        gs = FONT_TITLE.render(T("game_over"), True, (0,0,0,30))
        gsr = gs.get_rect(center=(WINDOW_WIDTH//2+2, 72))
        surface.blit(gs, gsr)
        surface.blit(go, gor)
        cw, ch = 380, 120
        cx = WINDOW_WIDTH//2 - cw//2
        cy = 95
        pygame.draw.rect(surface, Colors.PANEL_BG, (cx,cy,cw,ch), border_radius=12)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, (cx,cy,cw,ch), 2, border_radius=12)
        sl = FONT_TINY.render(T("score_label"), True, Colors.TEXT_DIM)
        surface.blit(sl, (cx+18, cy+10))
        sv = FONT_TITLE.render(fmt_score(current_score), True, Colors.GOLD)
        surface.blit(sv, sv.get_rect(midleft=(cx+18, cy+70)))
        ix = cx + cw - 180
        iy = cy + 15
        mn = "Endless" if snake_game.mode=="endless" else "Timed"
        for i, t in enumerate([
            f"{T('mode_label')}: {mn}",
            f"{T('multiplier')}: {snake_game.multiplier}x",
            f"{T('food_label')}: {snake_game.food_eaten}",
        ]):
            it = FONT_TINY.render(t, True, Colors.TEXT_DIM)
            surface.blit(it, (ix, iy+i*22))
        scy = cy + ch + 12
        pygame.draw.rect(surface, Colors.PANEL_BG, (cx,scy,cw,72), border_radius=10)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, (cx,scy,cw,72), 1, border_radius=10)
        col = cw // 3
        for i, (l, v) in enumerate([
            (T("max_endless"), fmt_score(stats['endless_high'])),
            (T("max_timed"), fmt_score(stats['timed_high'])),
            (T("total_score"), str(stats['total_score']//SCORE_SCALE)),
        ]):
            cc = cx + i*col + col//2
            lb = FONT_MICRO.render(l, True, Colors.TEXT_DIM)
            surface.blit(lb, lb.get_rect(center=(cc, scy+18)))
            va = FONT_SMALL.render(v, True, Colors.TEXT_MAIN)
            surface.blit(va, va.get_rect(center=(cc, scy+48)))
        ny = scy + 85
        hr_ = stats['endless_high'] if snake_game.mode=='endless' else stats['timed_high']
        if current_score >= hr_ and current_score > 0:
            pulse = abs(math.sin(pygame.time.get_ticks()/300))
            gc = (255, int(215*pulse), 0)
            rec = FONT_LARGE.render(T("new_record"), True, gc)
            rcr = rec.get_rect(center=(WINDOW_WIDTH//2, ny))
            gs2 = pygame.Surface((rec.get_width()+20, rec.get_height()+10), pygame.SRCALPHA)
            gs2.fill((*gc, 30))
            surface.blit(gs2, (rcr.x-10, rcr.y-5))
            surface.blit(rec, rcr)
            ny += 55
        pt3 = FONT_TINY.render(f"{T('score_earned')}: +{fmt_score(current_score)}",
                               True, Colors.GREEN_BTN)
        surface.blit(pt3, pt3.get_rect(center=(WINDOW_WIDTH//2, ny)))
        ny += 25
        # XP显示
        _xp = stats.get("xp", 0)
        _lvl, _prog, _need = xp_to_level(_xp)
        _tier = get_rank_tier(_lvl)
        xp_text = f"{T('rank_level')}: {_lvl}  |  {T('rank_xp')}: {_prog}/{_need}"
        xp_surf = FONT_TINY.render(xp_text, True, _tier["color"])
        surface.blit(xp_surf, xp_surf.get_rect(center=(WINDOW_WIDTH//2, ny)))
        ny += 30
        go_restart.rect.y = ny
        go_menu.rect.y = ny + 55
        go_restart.draw(surface)
        go_menu.draw(surface)

    # ==================================================================
    #  主循环
    # ==================================================================
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("贪吃蛇 v7.10")
    clock = pygame.time.Clock()
    running = True
    move_timer = 0
    paused = False
    vs_move_timer = 0

    # 菜单按钮列表 (用于统一更新)
    menu_buttons = [start_btn, vs_btn, mode_btn, edge_btn, shop_btn, skin_btn,
                    effects_btn, lang_btn, theme_btn, ach_btn, rank_btn, daily_btn,
                    music_btn, help_btn, stats_btn, update_btn, dev_btn] + speed_btns

    while running:
        dt = clock.tick(FPS)
        dt_sec = dt / 1000.0
        mp = pygame.mouse.get_pos()
        if flash_alpha > 0:
            flash_alpha -= 15
            if flash_alpha < 0:
                flash_alpha = 0
        if 1 not in unlocked_skins and stats['total_time'] >= 180:
            unlocked_skins.append(1)
            stats["unlocked_skins"] = unlocked_skins
            save_stats()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break

            if game_state == ST_POPUP:
                if popup_type == "shop":
                    if event.type == MOUSEBUTTONDOWN:
                        if not shop_pr.collidepoint(event.pos):
                            game_state = ST_MENU
                            popup_type = None
                            continue
                        if eall and eall.clicked(event):
                            r = get_redeemable()
                            if r >= 2*SCORE_SCALE:
                                g_ = r // (2 * SCORE_SCALE)
                                stats['redeemed_points'] += g_
                                save_stats()
                                shop_msg = T("exchange_success", g_*2, g_)
                                shop_msg_timer = 180
                            else:
                                shop_msg = T("exchange_fail", 2)
                                shop_msg_timer = 120
                        elif e50 and e50.clicked(event):
                            r = get_redeemable()
                            if r >= 100*SCORE_SCALE:
                                stats['redeemed_points'] += 50
                                save_stats()
                                shop_msg = T("exchange_success", 100, 50)
                                shop_msg_timer = 180
                            else:
                                shop_msg = T("exchange_fail", 100)
                                shop_msg_timer = 120
                        elif e10 and e10.clicked(event):
                            r = get_redeemable()
                            if r >= 20*SCORE_SCALE:
                                stats['redeemed_points'] += 10
                                save_stats()
                                shop_msg = T("exchange_success", 20, 10)
                                shop_msg_timer = 180
                            else:
                                shop_msg = T("exchange_fail", 20)
                                shop_msg_timer = 120
                        elif eb and eb.clicked(event):
                            r = get_redeemable()
                            if r >= 2*SCORE_SCALE:
                                stats['redeemed_points'] += 1
                                save_stats()
                                shop_msg = T("exchange_success", 2, 1)
                                shop_msg_timer = 180
                            else:
                                shop_msg = T("exchange_fail", 2)
                                shop_msg_timer = 120
                    if shop_msg_timer > 0:
                        shop_msg_timer -= 1

                elif popup_type == "skin":
                    _skin_header_h = 60
                    _skin_footer_h = 36
                    _skin_item_h = 90
                    _skin_visible_h = SKPH - _skin_header_h - _skin_footer_h
                    _skin_total_h = len(SKINS) * _skin_item_h
                    _skin_max_s = max(0, _skin_total_h - _skin_visible_h)
                    skin_max_scroll = _skin_max_s
                    _bar_click_w = 18
                    _bar_visual_w = 8
                    _bar_bx = skin_pr.right - 20
                    _bar_by = skin_pr.y + _skin_header_h
                    _bar_bh = _skin_visible_h
                    _th = max(24, int(_bar_bh * min(1.0, _skin_visible_h / _skin_total_h)))
                    if event.type == MOUSEBUTTONDOWN and event.button in (4, 5):
                        if event.button == 4:
                            skin_scroll_offset = max(0, skin_scroll_offset - 40)
                        else:
                            skin_scroll_offset = min(_skin_max_s, skin_scroll_offset + 40)
                        continue
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        # 检查是否点击滚动条（加宽点击区域）
                        if _skin_max_s > 0:
                            _ty = _bar_by + int((skin_scroll_offset / _skin_max_s) * (_bar_bh - _th)) if _skin_max_s > 0 else _bar_by
                            _click_rect = pygame.Rect(_bar_bx, _ty, _bar_click_w, _th)
                            if _click_rect.collidepoint(event.pos):
                                scrollbar_dragging = True
                                scrollbar_drag_info = ("skin", event.pos[1], skin_scroll_offset, _skin_max_s, (_bar_bx, _bar_by, _bar_bh, _th))
                                continue
                    if event.type == MOUSEBUTTONUP:
                        scrollbar_dragging = False
                        scrollbar_drag_info = None
                    elif event.type == MOUSEMOTION and scrollbar_dragging and scrollbar_drag_info:
                        if scrollbar_drag_info[0] == "skin":
                            _, _start_my, _start_off, max_s, bar = scrollbar_drag_info
                            _bx, _by, _bh, _h = bar
                            # 计算鼠标在手柄内的初始点击偏移
                            _handle_start_y = _by + int((_start_off / max_s) * (_bh - _h)) if max_s > 0 else _by
                            _click_offset = _start_my - _handle_start_y
                            # 当前鼠标对应的手柄顶部位置
                            _target_y = event.pos[1] - _by - _click_offset
                            _target_y = max(0, min(_target_y, _bh - _h))
                            if _bh - _h > 0:
                                skin_scroll_offset = int(_target_y * max_s / (_bh - _h))
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        # 确认弹窗优先处理
                        if skin_confirm_popup and skin_confirm_id is not None:
                            if skin_confirm_yes.clicked(event):
                                sk = SKINS[skin_confirm_id]
                                pt = sk["price"]
                                r = get_redeemable()
                                if r >= pt * SCORE_SCALE:
                                    stats['redeemed_points'] += pt
                                    unlocked_skins.append(skin_confirm_id)
                                    stats["unlocked_skins"] = unlocked_skins
                                    save_stats()
                                skin_confirm_popup = False
                                skin_confirm_id = None
                                continue
                            elif skin_confirm_no.clicked(event):
                                skin_confirm_popup = False
                                skin_confirm_id = None
                                continue
                        if not skin_pr.collidepoint(event.pos):
                            game_state = ST_MENU
                            popup_type = None
                            skin_confirm_popup = False
                            continue
                        item_h = 120
                        click_y = event.pos[1] - (skin_pr.y+64) + skin_scroll_offset
                        idx = click_y // item_h
                        if 0 <= idx < len(SKINS):
                            sk = SKINS[idx]
                            if sk["id"] in unlocked_skins:
                                current_skin_id = sk["id"]
                                stats["current_skin"] = current_skin_id
                                save_stats()
                            elif (sk["price"] >= 0 and
                                  get_redeemable() >= sk["price"]*SCORE_SCALE):
                                skin_confirm_popup = True
                                skin_confirm_id = sk["id"]

                elif popup_type == "music":
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button in (4,5):
                            ms = max(0, music_total*22-120)
                            if event.button == 4:
                                music_list_scroll = max(0, music_list_scroll-40)
                            else:
                                music_list_scroll = min(ms, music_list_scroll+40)
                            continue
                        if event.button == 1:
                            if not mpr.collidepoint(event.pos):
                                game_state = ST_MENU
                                popup_type = None
                                continue
                            if mp_prev.clicked(event):
                                prev_music()
                                mp_play.text = T("pause_btn")
                            if mp_play.clicked(event):
                                if music_playing:
                                    pause_music()
                                    mp_play.text = T("play")
                                else:
                                    resume_music()
                                    mp_play.text = T("pause_btn")
                            if mp_next.clicked(event):
                                next_music()
                                mp_play.text = T("pause_btn")
                            sx2 = mpr.x + 80
                            sy2 = mpr.y + 188
                            sw2 = 320
                            tr2 = pygame.Rect(
                                sx2+int(sw2*music_volume)-6, sy2-4, 12, 18)
                            if (tr2.collidepoint(event.pos) or
                                pygame.Rect(sx2,sy2,sw2,10).collidepoint(event.pos)):
                                dragging_volume = True
                                rel_x = max(0, min(event.pos[0]-sx2, sw2))
                                set_volume(rel_x/sw2)
                            lx2 = mpr.x + 30
                            ly2 = mpr.y + 265
                            if ly2 <= event.pos[1] < ly2+120:
                                idx2 = (event.pos[1]-ly2+music_list_scroll)//22
                                if 0 <= idx2 < music_total:
                                    play_music(idx2)
                                    mp_play.text = T("pause_btn")
                    elif event.type == MOUSEMOTION and dragging_volume:
                        sx2 = mpr.x + 80
                        sw2 = 320
                        rel_x = max(0, min(event.pos[0]-sx2, sw2))
                        set_volume(rel_x/sw2)
                    elif event.type == MOUSEBUTTONUP:
                        dragging_volume = False
                        scrollbar_dragging = False
                        scrollbar_drag_info = None

                elif popup_type == "achievements":
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button in (4, 5):
                            item_total_h = 50 + 4  # item_h + gap
                            visible_h = 440 - 130  # ch - header - footer
                            ach_max = max(0, len(ACHIEVEMENTS) * item_total_h - visible_h)
                            if event.button == 4:
                                ach_popup.scroll_offset = max(0, ach_popup.scroll_offset - 40)
                            else:
                                ach_popup.scroll_offset = min(ach_max, ach_popup.scroll_offset + 40)
                            continue
                        if event.button == 1:
                            # 检查是否点击滚动条
                            ach_max = max(0, len(ACHIEVEMENTS) * 54 - 310)
                            if ach_max > 0:
                                bar_bx = ach_popup.rect.right - 12
                                bar_by = ach_popup.rect.y + 85
                                bar_bh = 310
                                th = max(15, int(bar_bh * (310 / (len(ACHIEVEMENTS) * 54))))
                                ty = bar_by + int((ach_popup.scroll_offset / ach_max) * (bar_bh - th))
                                bar_rect = pygame.Rect(bar_bx, ty, 6, th)
                                if bar_rect.collidepoint(event.pos):
                                    scrollbar_dragging = True
                                    scrollbar_drag_info = ("ach", event.pos[1], ach_popup.scroll_offset, ach_max, (bar_bx, bar_by, bar_bh, th))
                                    continue
                            if not ach_popup.rect.collidepoint(event.pos):
                                game_state = ST_MENU
                                popup_type = None
                                continue
                    elif event.type == MOUSEBUTTONUP:
                        scrollbar_dragging = False
                        scrollbar_drag_info = None
                    elif event.type == MOUSEMOTION and scrollbar_dragging and scrollbar_drag_info:
                        if scrollbar_drag_info[0] == "ach":
                            _, _start_my, _start_off, max_s, bar = scrollbar_drag_info
                            bar_bx, bar_by, bar_bh, th = bar
                            _handle_start_y = bar_by + int((_start_off / max_s) * (bar_bh - th)) if max_s > 0 else bar_by
                            _click_offset = _start_my - _handle_start_y
                            _target_y = event.pos[1] - bar_by - _click_offset
                            _target_y = max(0, min(_target_y, bar_bh - th))
                            if bar_bh - th > 0:
                                ach_popup.scroll_offset = int(_target_y * max_s / (bar_bh - th))

                elif popup_type == "daily_info":
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if not daily_popup_rect.collidepoint(event.pos):
                            game_state = ST_MENU
                            popup_type = None
                            continue

                else:
                    cp = None
                    if popup_type == "help":
                        cp = help_popup
                    elif popup_type == "dev":
                        cp = dev_popup
                    elif popup_type == "update":
                        cp = update_popup
                    elif popup_type == "stats":
                        cp = stats_popup
                    if event.type == MOUSEBUTTONDOWN and event.button == 1 and cp:
                        # 计算滚动条参数（与draw方法一致）
                        _visible_h = cp.H - 90
                        _line_h = 20
                        if popup_type == "help":
                            _content_h = len(LANG[current_lang]["help_content"]) * _line_h + 20
                        elif popup_type == "dev":
                            _content_h = len(LANG[current_lang]["dev_content"]) * _line_h + 20
                        elif popup_type == "update":
                            _content_h = len(LANG[current_lang]["update_content"]) * _line_h + 20
                        elif popup_type == "stats":
                            _content_h = len(get_stat_lines()) * _line_h + 20
                        else:
                            _content_h = cp.content_height
                        _max_s = max(0, _content_h - _visible_h)
                        # 检查是否点击滚动条
                        if _max_s > 0:
                            bar_bx = cp.rect.right - 14
                            bar_by = cp.rect.y + 66
                            bar_bh = _visible_h
                            th = max(20, int(bar_bh * (_visible_h / _content_h)))
                            ty = bar_by + int((cp.scroll_offset / _max_s) * (bar_bh - th))
                            bar_rect = pygame.Rect(bar_bx, ty, 8, th)
                            if bar_rect.collidepoint(event.pos):
                                scrollbar_dragging = True
                                scrollbar_drag_info = (popup_type, event.pos[1], cp.scroll_offset, _max_s, (bar_bx, bar_by, bar_bh, th))
                                continue
                        if not cp.rect.collidepoint(event.pos):
                            game_state = ST_MENU
                            popup_type = None
                            cp.reset_scroll()
                    elif event.type == MOUSEBUTTONUP:
                        scrollbar_dragging = False
                        scrollbar_drag_info = None
                    elif event.type == MOUSEMOTION and scrollbar_dragging and scrollbar_drag_info:
                        if scrollbar_drag_info[0] == popup_type:
                            _, _start_my, _start_off, max_s, bar = scrollbar_drag_info
                            bar_bx, bar_by, bar_bh, th = bar
                            _handle_start_y = bar_by + int((_start_off / max_s) * (bar_bh - th)) if max_s > 0 else bar_by
                            _click_offset = _start_my - _handle_start_y
                            _target_y = event.pos[1] - bar_by - _click_offset
                            _target_y = max(0, min(_target_y, bar_bh - th))
                            if bar_bh - th > 0:
                                cp.scroll_offset = int(_target_y * max_s / (bar_bh - th))
                    elif event.type == MOUSEBUTTONDOWN and event.button in (4, 5) and cp:
                        cp.handle_wheel(event)

            elif game_state == ST_MENU:
                for b in speed_btns:
                    if b.clicked(event):
                        current_speed_index = b.speed_index
                        for b2 in speed_btns:
                            b2.active = False
                        b.active = True
                if start_btn.clicked(event):
                    snake_game.reset()
                    snake_game.mode = game_mode
                    game_state = ST_PLAYING
                    paused = False
                    session_time = 0
                if vs_btn.clicked(event):
                    game_state = ST_DIFFICULTY_SELECT
                    diff_rects = []
                if mode_btn.clicked(event):
                    if game_mode == "endless":
                        game_mode = "timed"
                        mode_btn.text = T("mode_prefix") + T("mode_timed")
                        mode_btn.active_color = "RED_BTN"
                    else:
                        game_mode = "endless"
                        mode_btn.text = T("mode_prefix") + T("mode_endless")
                        mode_btn.active_color = "BLUE_BTN"
                    mode_btn.active = True
                if edge_btn.clicked(event):
                    edge_mode = (edge_mode + 1) % 3
                    edge_btn.active = (edge_mode != EDGE_DEATH)
                    edge_btn.text = T(_edge_mode_names[edge_mode])
                    edge_btn.active_color = _edge_mode_colors[edge_mode]
                if shop_btn.clicked(event):
                    game_state = ST_POPUP
                    popup_type = "shop"
                    shop_msg = ""
                    shop_msg_timer = 0
                if skin_btn.clicked(event):
                    game_state = ST_POPUP
                    popup_type = "skin"
                    skin_scroll_offset = 0
                    skin_confirm_popup = False
                if effects_btn.clicked(event):
                    effects_enabled = not effects_enabled
                    effects_btn.active = effects_enabled
                    effects_btn.text = T("effects_on") if effects_enabled else T("effects_off")
                    stats["effects_enabled"] = effects_enabled
                    save_stats()
                if lang_btn.clicked(event):
                    game_state = ST_LANG_SELECT
                    lang_rects = []
                if theme_btn.clicked(event):
                    game_state = ST_THEME_SELECT
                    theme_rects = []
                if music_btn.clicked(event):
                    game_state = ST_POPUP
                    popup_type = "music"
                    music_list_scroll = 0
                    mp_play.text = T("pause_btn") if music_playing else T("play")
                if help_btn.clicked(event):
                    game_state = ST_POPUP
                    popup_type = "help"
                    help_popup.reset_scroll()
                elif stats_btn.clicked(event):
                    game_state = ST_POPUP
                    popup_type = "stats"
                    stats_popup.reset_scroll()
                elif update_btn.clicked(event):
                    game_state = ST_POPUP
                    popup_type = "update"
                    update_popup.reset_scroll()
                elif dev_btn.clicked(event):
                    game_state = ST_POPUP
                    popup_type = "dev"
                    dev_popup.reset_scroll()
                if ach_btn.clicked(event):
                    game_state = ST_POPUP
                    popup_type = "achievements"
                    ach_popup.reset_scroll()
                if rank_btn.clicked(event):
                    game_state = ST_RANK_PANEL
                    rank_popup.reset_scroll()
                if daily_btn.clicked(event):
                    game_state = ST_POPUP
                    popup_type = "daily_info"
                if event.type == KEYDOWN:
                    if event.key in (K_PLUS, K_EQUALS):
                        set_volume(music_volume + 0.1)
                    elif event.key == K_MINUS:
                        set_volume(music_volume - 0.1)

            elif game_state == ST_DIFFICULTY_SELECT:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    clicked_diff = False
                    for i, rect in enumerate(diff_rects):
                        if rect.collidepoint(event.pos):
                            current_ai_difficulty = i
                            vs_game = VSGame()
                            vs_game.ai_difficulty = i
                            vs_game.player = vs_game._create_player_snake()
                            vs_game.player_direction = (1, 0)
                            vs_game.player_score = 0
                            vs_paused = False
                            game_state = ST_VS_PLAYING
                            clicked_diff = True
                            break
                    # 点击外部关闭弹窗
                    if not clicked_diff:
                        popup_rect = pygame.Rect((WINDOW_WIDTH - 400) // 2, (WINDOW_HEIGHT - 280) // 2, 400, 280)
                        if not popup_rect.collidepoint(event.pos):
                            game_state = ST_MENU

            elif game_state == ST_LANG_SELECT:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    lang_ids = ["zh", "en", "ja"]
                    clicked = False
                    for i, rect in enumerate(lang_rects):
                        if rect.collidepoint(event.pos):
                            current_lang = lang_ids[i]
                            clicked = True
                            break
                    if clicked or not pygame.Rect((WINDOW_WIDTH-300)//2, (WINDOW_HEIGHT-240)//2, 300, 240).collidepoint(event.pos):
                        # 更新所有按钮文本
                        lang_btn.text = {"zh": "中文", "en": "English", "ja": "日本語"}[current_lang]
                        start_btn.text = T("start")
                        vs_btn.text = T("vs_mode")
                        mode_btn.text = T("mode_prefix") + (T("mode_timed") if game_mode == "timed" else T("mode_endless"))
                        edge_btn.text = T(_edge_mode_names[edge_mode])
                        edge_btn.active_color = _edge_mode_colors[edge_mode]
                        shop_btn.text = T("shop")
                        skin_btn.text = T("skin_shop")
                        effects_btn.text = T("effects_on") if effects_enabled else T("effects_off")
                        music_btn.text = T("music")
                        help_btn.text = T("help")
                        stats_btn.text = T("stats")
                        update_btn.text = T("update")
                        dev_btn.text = T("dev")
                        pause_btn.text = T("pause")
                        end_btn.text = T("end")
                        go_restart.text = T("restart")
                        go_menu.text = T("back_menu")
                        vs_restart.text = T("restart")
                        vs_menu.text = T("back_menu")
                        mp_prev.text = T("prev")
                        mp_play.text = T("pause_btn") if music_playing else T("play")
                        mp_next.text = T("next")
                        theme_btn.text = T("theme")
                        ach_btn.text = T("achievements")
                        # 更新积分商店按钮文本
                        if eb: eb.text = T("exchange_1")
                        if e10: e10.text = T("exchange_10")
                        if e50: e50.text = T("exchange_50")
                        if eall: eall.text = T("exchange_all")
                        # 更新皮肤确认按钮文本
                        skin_confirm_yes.text = T("confirm_yes")
                        skin_confirm_no.text = T("confirm_no")
                        for i, b in enumerate(speed_btns):
                            b.text = SPEED_PRESETS[i]["name"].get(current_lang, SPEED_PRESETS[i]["name"]["en"])
                        game_state = ST_MENU

            elif game_state == ST_THEME_SELECT:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    theme_ids = list(THEMES.keys())
                    clicked = False
                    for i, rect in enumerate(theme_rects):
                        if rect.collidepoint(event.pos):
                            apply_theme(theme_ids[i])
                            clicked = True
                            break
                    if clicked or not pygame.Rect((WINDOW_WIDTH-360)//2, (WINDOW_HEIGHT-320)//2, 360, 320).collidepoint(event.pos):
                        game_state = ST_MENU

            elif game_state == ST_RANK_PANEL:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button in (4, 5):
                        rank_max = max(0, 6 * 28 - 200)
                        if event.button == 4:
                            rank_popup.scroll_offset = max(0, rank_popup.scroll_offset - 40)
                        else:
                            rank_popup.scroll_offset = min(rank_max, rank_popup.scroll_offset + 40)
                        continue
                    if event.button == 1:
                        if not rank_popup.rect.collidepoint(event.pos):
                            game_state = ST_MENU
                            continue
                elif event.type == MOUSEBUTTONUP:
                    scrollbar_dragging = False
                    scrollbar_drag_info = None
                elif event.type == MOUSEMOTION and scrollbar_dragging and scrollbar_drag_info:
                    if scrollbar_drag_info[0] == "rank":
                        _, start_y, start_offset, max_s, bar = scrollbar_drag_info
                        bar_bx, bar_by, bar_bh, th = bar
                        dy = event.pos[1] - start_y
                        scroll_range = max_s
                        pixel_range = bar_bh - th
                        if pixel_range > 0:
                            rank_popup.scroll_offset = max(0, min(max_s, start_offset + int(dy * scroll_range / pixel_range)))

            elif game_state in (ST_VS_PLAYING, ST_VS_PAUSED):
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game_state = ST_MENU
                    elif event.key == K_SPACE:
                        vs_paused = not vs_paused
                        game_state = ST_VS_PAUSED if vs_paused else ST_VS_PLAYING
                    elif not vs_paused:
                        # 修复: 防止玩家反向移动（180度掉头）
                        new_dir = None
                        if event.key in (K_UP, K_w):
                            new_dir = (0, -1)
                        elif event.key in (K_DOWN, K_s):
                            new_dir = (0, 1)
                        elif event.key in (K_LEFT, K_a):
                            new_dir = (-1, 0)
                        elif event.key in (K_RIGHT, K_d):
                            new_dir = (1, 0)
                        if new_dir:
                            cur = vs_game.player_direction
                            # 防止与当前方向相反
                            if (cur[0] + new_dir[0], cur[1] + new_dir[1]) != (0, 0):
                                vs_game.player_direction = new_dir

            elif game_state == ST_VS_OVER:
                if vs_restart.clicked(event):
                    vs_game = VSGame()
                    vs_game.ai_difficulty = current_ai_difficulty
                    vs_game.player = vs_game._create_player_snake()
                    vs_game.player_direction = (1, 0)
                    vs_game.player_score = 0
                    vs_paused = False
                    game_state = ST_VS_PLAYING
                elif vs_menu.clicked(event):
                    game_state = ST_MENU

            elif game_state in (ST_PLAYING, ST_PAUSED):
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        game_state = ST_MENU
                        paused = False
                    elif event.key == K_SPACE:
                        paused = not paused
                        game_state = ST_PAUSED if paused else ST_PLAYING
                    elif not paused:
                        if event.key in (K_UP, K_w):
                            snake_game.change_direction((0, -1))
                        elif event.key in (K_DOWN, K_s):
                            snake_game.change_direction((0, 1))
                        elif event.key in (K_LEFT, K_a):
                            snake_game.change_direction((-1, 0))
                        elif event.key in (K_RIGHT, K_d):
                            snake_game.change_direction((1, 0))
                if pause_btn.clicked(event):
                    paused = not paused
                    game_state = ST_PAUSED if paused else ST_PLAYING
                if end_btn.clicked(event):
                    snake_game.game_over = True
                    current_score = snake_game.score
                    stats["total_score"] += current_score
                    stats["games_played"] += 1
                    stats["total_time"] += int(session_time)
                    if snake_game.mode == "endless":
                        if current_score > stats["endless_high"]:
                            stats["endless_high"] = current_score
                    else:
                        if current_score > stats["timed_high"]:
                            stats["timed_high"] = current_score
                    save_stats()
                    # 成就追踪
                    _speeds = set(stats.get("speeds_played", []))
                    _speeds.add(current_speed_index)
                    stats["speeds_played"] = list(_speeds)
                    _themes = set(stats.get("themes_used", []))
                    _themes.add(current_theme)
                    stats["themes_used"] = list(_themes)
                    stats["total_food_eaten"] = stats.get("total_food_eaten", 0) + snake_game.food_eaten
                    check_achievements({
                        "games_played": stats["games_played"],
                        "game_score": current_score,
                        "snake_length": len(snake_game.snake),
                        "total_food": stats.get("total_food_eaten", 0),
                        "total_time": stats["total_time"],
                        "vs_wins": stats.get("vs_wins", 0),
                        "speeds_played": _speeds,
                        "themes_used": _themes,
                        "game_duration": session_time,
                        "wall_slides": getattr(snake_game, 'wall_slide_count', 0),
                        "corners_visited": getattr(snake_game, 'corners_visited', set()),
                        "skin_id": current_skin_id,
                        "game_completed": False,
                    })
                    # XP奖励
                    _earned_xp = 50 + snake_game.food_eaten * 5
                    _new_lvl, _, _ = award_xp(_earned_xp, "game_complete")
                    stats["xp_streak"] = stats.get("xp_streak", 0) + 1
                    flash_alpha = 200
                    game_state = ST_GAME_OVER
                    paused = False

            elif game_state == ST_GAME_OVER:
                if go_restart.clicked(event):
                    snake_game.reset()
                    snake_game.mode = game_mode
                    game_state = ST_PLAYING
                    paused = False
                    session_time = 0
                elif go_menu.clicked(event):
                    game_state = ST_MENU

        # ---- 更新按钮悬停状态 (修复: 移出KEYDOWN检查) ----
        if game_state == ST_MENU:
            for b in menu_buttons:
                b.update(mp)
        elif game_state in (ST_PLAYING, ST_PAUSED):
            pause_btn.update(mp)
            end_btn.update(mp)
        elif game_state == ST_GAME_OVER:
            go_restart.update(mp)
            go_menu.update(mp)
        elif game_state == ST_VS_OVER:
            vs_restart.update(mp)
            vs_menu.update(mp)
        elif game_state == ST_POPUP:
            if popup_type == "shop" and eb:
                eb.update(mp)
                e10.update(mp)
                e50.update(mp)
                eall.update(mp)
            elif popup_type == "music":
                mp_prev.update(mp)
                mp_play.update(mp)
                mp_next.update(mp)
            elif popup_type == "skin" and skin_confirm_popup:
                skin_confirm_yes.update(mp)
                skin_confirm_no.update(mp)

        # ---- 单人游戏逻辑 ----
        if game_state == ST_PLAYING and not paused:
            speed_mult = 1.0
            if (effects_enabled and
                SKINS[current_skin_id]["special"]["type"] == "speed_boost"):
                speed_mult = SKINS[current_skin_id]["special"]["params"]
            move_timer += dt * speed_mult
            interval = 1000 // SPEED_PRESETS[current_speed_index]["fps"]
            if move_timer >= interval:
                move_timer -= interval
                over = snake_game.update(dt_sec * (interval / 16.67))
                session_time += interval / 1000.0
                if over:
                    current_score = snake_game.score
                    stats["total_score"] += current_score
                    stats["games_played"] += 1
                    stats["total_time"] += int(session_time)
                    if snake_game.mode == "endless":
                        if current_score > stats["endless_high"]:
                            stats["endless_high"] = current_score
                    else:
                        if current_score > stats["timed_high"]:
                            stats["timed_high"] = current_score
                    save_stats()
                    flash_alpha = 200
                    game_state = ST_GAME_OVER

        # ---- 对战游戏逻辑 ----
        if game_state == ST_VS_PLAYING and not vs_paused:
            vs_move_timer += dt
            vs_speed_mult = 1.0
            if (effects_enabled and
                SKINS[current_skin_id]["special"]["type"] == "speed_boost"):
                vs_speed_mult = SKINS[current_skin_id]["special"]["params"]
            vs_interval = 1000 // max(1, int(8 * vs_speed_mult))
            if vs_move_timer >= vs_interval:
                vs_move_timer -= vs_interval
                # 修复: 对战模式也累计游戏时长
                session_time += vs_interval / 1000.0
                if vs_game.player is None:
                    vs_game.player = vs_game._create_player_snake()
                vs_game.update()
                if vs_game.vs_game_over:
                    current_score = vs_game.player_score * SCORE_SCALE
                    stats["total_score"] += current_score
                    stats["games_played"] += 1
                    stats["total_time"] += int(session_time)
                    stats["vs_wins"] = (stats.get("vs_wins", 0) +
                                        (1 if vs_game.result == "win" else 0))
                    stats["vs_losses"] = (stats.get("vs_losses", 0) +
                                          (1 if vs_game.result == "lose" else 0))
                    save_stats()
                    # 成就追踪 (VS模式)
                    _themes = set(stats.get("themes_used", []))
                    _themes.add(current_theme)
                    stats["themes_used"] = list(_themes)
                    check_achievements({
                        "games_played": stats["games_played"],
                        "game_score": vs_game.player_score * SCORE_SCALE,
                        "snake_length": len(vs_game.player) if vs_game.player else 0,
                        "total_food": stats.get("total_food_eaten", 0),
                        "total_time": stats["total_time"],
                        "vs_wins": stats.get("vs_wins", 0),
                        "vs_hell_win": vs_game.result == "win" and vs_game.ai_difficulty == 2,
                        "themes_used": _themes,
                    })
                    # VS模式XP奖励
                    if vs_game.result == "win":
                        _vs_xp = 80 if vs_game.ai_difficulty == 2 else 40
                        award_xp(_vs_xp, "vs_win")
                    stats["xp_streak"] = stats.get("xp_streak", 0) + 1
                    game_state = ST_VS_OVER

        # ---- 渲染 ----
        screen.fill(Colors.BG_DARK)

        if game_state == ST_MENU:
            draw_menu(screen)
        elif game_state == ST_DIFFICULTY_SELECT:
            draw_menu(screen)
            draw_difficulty_popup(screen)
        elif game_state == ST_LANG_SELECT:
            draw_menu(screen)
            draw_lang_popup(screen)
        elif game_state == ST_THEME_SELECT:
            draw_menu(screen)
            draw_theme_popup(screen)
        elif game_state in (ST_VS_PLAYING, ST_VS_PAUSED):
            draw_vs_playing(screen, vs_paused)
        elif game_state == ST_VS_OVER:
            draw_vs_over(screen)
        elif game_state in (ST_PLAYING, ST_PAUSED):
            draw_playing(screen, paused)
        elif game_state == ST_GAME_OVER:
            draw_game_over(screen)
        elif game_state == ST_POPUP:
            if popup_type == "shop":
                draw_menu(screen)
                draw_shop_popup(screen)
            elif popup_type == "skin":
                draw_menu(screen)
                draw_skin_popup(screen)
            elif popup_type == "music":
                draw_menu(screen)
                draw_music_popup(screen)
            elif popup_type == "help":
                draw_menu(screen)
                help_popup.draw(screen, T("help_title"),
                                LANG[current_lang]["help_content"])
            elif popup_type == "dev":
                draw_menu(screen)
                dev_popup.draw(screen, T("dev_title"),
                               LANG[current_lang]["dev_content"])
            elif popup_type == "update":
                draw_menu(screen)
                update_popup.draw(screen, T("update_title"),
                                  LANG[current_lang]["update_content"])
            elif popup_type == "stats":
                draw_menu(screen)
                stats_popup.draw(screen, T("stats_title"), get_stat_lines())
            elif popup_type == "achievements":
                draw_menu(screen)
                draw_achievement_popup(screen)
            elif popup_type == "daily_info":
                draw_menu(screen)
                draw_daily_challenge_info(screen)

        if game_state == ST_RANK_PANEL:
            draw_menu(screen)
            draw_rank_panel(screen)

        # 成就解锁通知弹窗
        if achievement_popup_timer > 0 and achievement_popup:
            achievement_popup_timer -= 1
            ach = achievement_popup
            pw, ph = 380, 70
            px = (WINDOW_WIDTH - pw) // 2
            py_ = 20
            alpha = min(255, achievement_popup_timer * 8)
            # 背景
            ps = pygame.Surface((pw, ph), pygame.SRCALPHA)
            ps.fill((*Colors.BG_MID[:3], alpha))
            screen.blit(ps, (px, py_))
            pygame.draw.rect(screen, (*Colors.GOLD[:3], alpha), (px, py_, pw, ph), 2, border_radius=8)
            # 图标
            icon_s = FONT_MEDIUM.render(ach["icon"], True, (*Colors.TEXT_MAIN[:3], alpha))
            screen.blit(icon_s, (px + 12, py_ + (ph - 24) // 2))
            # 文字
            name_text = ach["name"].get(current_lang, ach["name"]["en"])
            name_s = FONT_SMALL.render(f"[ACHIEVEMENT] {name_text}", True, (*Colors.TEXT_MAIN[:3], alpha))
            screen.blit(name_s, (px + 45, py_ + 8))
            desc_s = FONT_TINY.render(ach["desc"].get(current_lang, ach["desc"]["en"]), True, (*Colors.TEXT_DIM[:3], alpha))
            screen.blit(desc_s, (px + 45, py_ + 28))
            # 积分奖励
            pts = ach.get("_earned_points", ach.get("points", 0))
            if pts > 0:
                pts_s = FONT_TINY.render(f"+{pts} pts", True, (*Colors.GOLD[:3], alpha))
                screen.blit(pts_s, (px + 45, py_ + 46))

        # 升级通知弹窗（右侧显示）
        if rank_levelup_timer > 0 and rank_levelup_popup:
            rank_levelup_timer -= 1
            lvl = rank_levelup_popup
            pw, ph = 200, 50
            px = WINDOW_WIDTH - pw - 15
            py_ = 120
            alpha = min(255, rank_levelup_timer * 8)
            ps = pygame.Surface((pw, ph), pygame.SRCALPHA)
            ps.fill((*Colors.BG_MID[:3], alpha))
            screen.blit(ps, (px, py_))
            pygame.draw.rect(screen, (*Colors.GOLD[:3], alpha), (px, py_, pw, ph), 2, border_radius=8)
            tier = get_rank_tier(lvl)
            tier_color = tier["color"]
            icon_s = FONT_SMALL.render("LVL", True, (*tier_color[:3], alpha))
            screen.blit(icon_s, (px + 8, py_ + (ph - 19) // 2))
            name_text = T("rank_level_up", lvl)
            name_s = FONT_TINY.render(name_text, True, (*Colors.TEXT_MAIN[:3], alpha))
            screen.blit(name_s, (px + 45, py_ + 8))
            tier_name = T(tier["name_key"])
            desc_s = FONT_MICRO.render(tier_name, True, (*tier_color[:3], alpha))
            screen.blit(desc_s, (px + 45, py_ + 28))

        pygame.display.flip()

    stop_music()
    pygame.quit()


if __name__ == "__main__":
    main()
