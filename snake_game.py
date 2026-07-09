"""
====================================================================
  🐍 贪吃蛇 - Snake Game  (v6.0 稳定版)
  新增: 英文语言支持 | 死亡闪白 | 结算界面优化
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
from collections import OrderedDict

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

    # ====================================================================
    #  语言系统 (中文 / English)
    # ====================================================================
    current_lang = "zh"

    LANG = {
        "zh": {
            "title": "贪  吃  蛇",
            "subtitle": "经 典 重 现  ·  挑 战 高 分",
            "speed": "移动速度",
            "mode": "模式: 无限",
            "mode_timed": "模式: 限时",
            "edge_slide": "边缘: 滑动",
            "edge_death": "边缘: 死亡",
            "start": "开始游戏",
            "shop": "积分商店",
            "help": "游戏说明",
            "stats": "统计信息",
            "update": "更新说明",
            "dev": "开发者",
            "music": "音乐控制",
            "lang_zh": "中文",
            "lang_en": "English",
            "score": "得分",
            "multiplier": "倍率",
            "mode_label": "模式",
            "time_label": "时间",
            "food_label": "食物",
            "pause": "暂停",
            "resume": "继续",
            "end": "结束",
            "game_over": "游 戏 结 束",
            "score_label": "本局得分",
            "high_label": "最高",
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
                "[ 积分商店 ]",
                "  主界面左侧「积分商店」按钮",
                "  累计总分按 2:1 比例兑换为积分",
            ],
            "dev_content": [
                "[ 开发者信息 ]",
                "",
                "  作者    :  WEZHCE",
                "  邮箱    :  1827267356@qq.com",
                "  B站 UID :  1309420497",
                "  GitHub  :  https://github.com/WEZHCE",
                "",
                "  版本    :  6.0 (稳定版)",
                "  引擎    :  Python 3 + Pygame",
                "",
                "[ 特别感谢 ]",
                "  感谢游玩本游戏，欢迎在B站/GitHub反馈交流",
            ],
            "update_content": [
                "═══════  v6.0 版本更新 ═══════",
                "",
                "  [新增] 英文语言支持",
                "    界面右下角一键切换中/英文",
                "",
                "  [新增] 死亡闪白特效",
                "    蛇死亡时屏幕白光一闪",
                "",
                "  [优化] 结算界面重设计",
                "    更清晰的信息层级",
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
            "mode": "Mode: Endless",
            "mode_timed": "Mode: Timed",
            "edge_slide": "Edge: Slide",
            "edge_death": "Edge: Death",
            "start": "Start Game",
            "shop": "Shop",
            "help": "Help",
            "stats": "Stats",
            "update": "Updates",
            "dev": "Dev",
            "music": "Music",
            "lang_zh": "中文",
            "lang_en": "English",
            "score": "Score",
            "multiplier": "Multiplier",
            "mode_label": "Mode",
            "time_label": "Time",
            "food_label": "Food",
            "pause": "Pause",
            "resume": "Resume",
            "end": "End",
            "game_over": "G A M E   O V E R",
            "score_label": "Score",
            "high_label": "High Score",
            "max_endless": "Endless High",
            "max_timed": "Timed High",
            "total_score": "Total Score",
            "new_record": "NEW RECORD !",
            "restart": "Play Again",
            "back_menu": "Main Menu",
            "score_earned": "Total Points Earned",
            "real_time": "Live Score",
            "current": "Current",
            "track_label": "Track",
            "volume": "Volume",
            "no_music": "No Music",
            "playing_status": "Playing",
            "paused_status": "Paused",
            "current_playing": "Now Playing",
            "status": "Status",
            "track_list": "Track List",
            "prev": "<<",
            "play": "Play",
            "pause_btn": "Pause",
            "next": ">>",
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
            "click_close": "Click outside to close",
            "scroll_close": "Scroll | Drag volume | Click outside",
            "stats_title": "D E T A I L E D   S T A T S",
            "games_played": "Games Played",
            "play_time": "Play Time",
            "avg_score": "Avg Score",
            "mode_title": "Mode High Scores",
            "help_title": "H E L P",
            "dev_title": "D E V E L O P E R",
            "update_title": "U P D A T E   L O G",
            "help_content": [
                "[ Controls ]",
                "  Arrow Keys / WASD    Move the snake",
                "  ESC                  Back to menu",
                "  Space                Pause/Resume",
                "",
                "[ Rules ]",
                "  Eat food to grow and gain score",
                "  Edge mode can be toggled in menu",
                "  Hitting yourself ends the game",
                "",
                "[ Modes ]",
                "  Endless - Classic unlimited play",
                "  Timed - 3 minute challenge",
                "",
                "[ Point Shop ]",
                "  Click Shop button on the left",
                "  Total score exchanged at 2:1 ratio",
            ],
            "dev_content": [
                "[ Developer Info ]",
                "",
                "  Author  :  WEZHCE",
                "  Email   :  1827267356@qq.com",
                "  B站 UID :  1309420497",
                "  GitHub  :  https://github.com/WEZHCE",
                "",
                "  Version :  6.0 (Stable)",
                "  Engine  :  Python 3 + Pygame",
                "",
                "[ Special Thanks ]",
                "  Thanks for playing! Feedback welcome on B站/GitHub",
            ],
            "update_content": [
                "═══════  v6.0 Update ═══════",
                "",
                "  [New] English Language Support",
                "    Toggle ZH/EN at bottom right",
                "",
                "  [New] Flash White on Death",
                "    Screen flashes white when snake dies",
                "",
                "  [Improve] Redesigned Game Over Screen",
                "",
                "═══════  v5.9 Update ═══════",
                "",
                "  [New] Point Shop System",
                "",
                "═══════  v5.8 Update ═══════",
                "",
                "  [New] Music Control Window",
                "",
                "═══════  v5.7 Update ═══════",
                "",
                "  [Fix] PyInstaller music path",
                "",
                "═══════  v5.6 Update ═══════",
                "",
                "  [Fix] Music button layout",
                "",
                "═══════  v5.5 Update ═══════",
                "",
                "  [Fix] Music button to bottom right",
                "",
                "═══════  v5.4 Update ═══════",
                "",
                "  [Fix] Skip corrupted music files",
                "",
                "═══════  v5.3 Update ═══════",
                "",
                "  [Update] Developer info",
                "",
                "═══════  v5.2 Update ═══════",
                "",
                "  [New] Background music system",
                "",
                "═══════  v5.1 Update ═══════",
                "",
                "  [New] Stats button",
                "",
                "═══════  v5.0 Update ═══════",
                "",
                "  [Change] Removed account system",
                "",
                "═══════  v4.0 Update ═══════",
                "",
                "  [New] Dual mode system",
                "  [New] In-game controls",
                "  [New] Live score panel",
                "",
                "═══════  v3.0 Update ═══════",
                "",
                "  [New] Edge collision toggle",
                "  [New] Score multiplier mechanic",
            ],
        }
    }

    def T(key, *args):
        text = LANG[current_lang].get(key, key)
        if args:
            return text.format(*args)
        return text

    # ====================================================================
    #  音乐系统
    # ====================================================================
    def get_music_dir():
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            internal = os.path.join(sys._MEIPASS, "music")
            if os.path.isdir(internal):
                return internal
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        external = os.path.join(base, "music")
        if os.path.isdir(external):
            return external
        cwd = os.path.join(os.getcwd(), "music")
        if os.path.isdir(cwd):
            return cwd
        return external

    MUSIC_DIR = get_music_dir()
    music_list = []
    music_names = []
    music_index = 0
    music_playing = False
    music_volume = 0.5
    music_total = 0

    if os.path.isdir(MUSIC_DIR):
        for f in sorted(os.listdir(MUSIC_DIR)):
            if f.lower().endswith(('.mp3', '.wav', '.ogg')):
                fp = os.path.join(MUSIC_DIR, f)
                if os.path.getsize(fp) > 1024:
                    music_list.append(fp)
                    music_names.append(f)

    music_total = len(music_list)
    if music_total > 0:
        print(f"[音乐] 加载了 {music_total} 首音乐")

    def play_music(index=None):
        nonlocal music_index, music_playing
        if music_total == 0:
            return
        if index is not None:
            music_index = max(0, min(index, music_total - 1))
        try:
            pygame.mixer.music.load(music_list[music_index])
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1)
            music_playing = True
        except pygame.error:
            music_playing = False
            if music_total > 1:
                next_idx = (music_index + 1) % music_total
                if next_idx != music_index:
                    music_index = next_idx
                    play_music()
        except Exception:
            music_playing = False

    def stop_music():
        nonlocal music_playing
        pygame.mixer.music.stop()
        music_playing = False

    def pause_music():
        nonlocal music_playing
        if music_playing and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            music_playing = False

    def resume_music():
        nonlocal music_playing
        if not music_playing and music_total > 0:
            pygame.mixer.music.unpause()
            music_playing = True

    def next_music():
        nonlocal music_index
        if music_total > 0:
            music_index = (music_index + 1) % music_total
            play_music()

    def prev_music():
        nonlocal music_index
        if music_total > 0:
            music_index = (music_index - 1) % music_total
            play_music()

    def set_volume(vol):
        nonlocal music_volume
        music_volume = max(0.0, min(1.0, vol))
        pygame.mixer.music.set_volume(music_volume)

    if music_total > 0:
        play_music(0)

    dragging_volume = False
    music_list_scroll = 0

    # ====================================================================
    #  配色
    # ====================================================================
    class Colors:
        BG_DARK       = (13, 13, 28)
        BG_MID        = (20, 20, 45)
        BG_LIGHT      = (30, 30, 60)
        GRID_EVEN     = (23, 23, 50)
        GRID_ODD      = (28, 28, 58)
        ACCENT        = (255, 82, 112)
        ACCENT_HOVER  = (255, 110, 140)
        SNAKE_HEAD    = (0, 220, 160)
        SNAKE_BODY    = (0, 170, 120)
        FOOD_MAIN     = (255, 82, 112)
        FOOD_GLOW     = (255, 130, 150)
        TEXT_MAIN     = (240, 240, 248)
        TEXT_DIM      = (140, 140, 170)
        TEXT_DARK     = (80, 80, 110)
        PANEL_BG      = (17, 17, 38)
        PANEL_BORDER  = (35, 35, 65)
        BTN_BG        = (40, 40, 75)
        BTN_HOVER     = (55, 55, 95)
        GOLD          = (255, 215, 0)
        GREEN_BTN     = (0, 180, 120)
        GREEN_BTN_H   = (0, 210, 150)
        RED_BTN       = (200, 60, 60)
        RED_BTN_H     = (230, 80, 80)
        BLUE_BTN      = (40, 100, 200)
        BLUE_BTN_H    = (60, 130, 230)
        SPEED_ACTIVE  = (60, 150, 255)
        VOLUME_TRACK  = (50, 50, 80)
        VOLUME_FILL   = (100, 200, 255)
        SHOP_GOLD     = (255, 180, 50)
        WHITE_FLASH   = (255, 255, 255)
        OVERLAY       = (13, 13, 28, 200)
        SCORE_PANEL   = (17, 17, 38, 200)
        SCROLL_BAR    = (60, 60, 100)
        SCROLL_BAR_BG = (30, 30, 50)

    def _find_font():
        font_paths = []
        win_dir = "C:/Windows/Fonts"
        if os.path.isdir(win_dir):
            for fn in ["msyh.ttc","msyhbd.ttc","simhei.ttf","simsun.ttc"]:
                fp = os.path.join(win_dir, fn)
                if os.path.isfile(fp): font_paths.append(fp)
        for d in ["/System/Library/Fonts","/Library/Fonts",os.path.expanduser("~/Library/Fonts")]:
            if os.path.isdir(d):
                for fn in ["PingFang.ttc","STHeiti Light.ttc","STHeiti Medium.ttc"]:
                    fp = os.path.join(d, fn)
                    if os.path.isfile(fp): font_paths.append(fp)
        linux_paths = [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        ]
        font_paths += linux_paths
        for fp in font_paths:
            if os.path.isfile(fp):
                try:
                    tf = pygame.font.Font(fp, 12)
                    if tf.render("中",True,(255,255,255)).get_width() > 5:
                        print(f"[字体] {os.path.basename(fp)}")
                        return fp
                except: pass
        return None

    FONT_PATH = _find_font()
    def _f(size):
        if FONT_PATH:
            try: return pygame.font.Font(FONT_PATH, size)
            except: pass
        return pygame.font.Font(None, size)

    FONT_TITLE  = _f(54)
    FONT_LARGE  = _f(32)
    FONT_MEDIUM = _f(24)
    FONT_SMALL  = _f(19)
    FONT_TINY   = _f(14)
    FONT_MICRO  = _f(12)

    SPEED_PRESETS = [
        {"name": {"zh":"简单","en":"Easy"}, "fps":5},
        {"name": {"zh":"普通","en":"Normal"}, "fps":9},
        {"name": {"zh":"困难","en":"Hard"}, "fps":14},
        {"name": {"zh":"地狱","en":"Hell"}, "fps":19},
    ]
    current_speed_index = 1
    edge_kills = False
    game_mode = "endless"
    TIMED_LIMIT = 180

    ST_MENU, ST_PLAYING, ST_PAUSED, ST_GAME_OVER, ST_POPUP = range(5)
    game_state = ST_MENU
    popup_type = None

    flash_alpha = 0

    stats = {
        "total_score": 0,
        "redeemed_points": 0,
        "games_played": 0,
        "endless_high": 0,
        "timed_high": 0,
        "total_time": 0
    }
    current_score = 0
    session_time = 0

    def get_redeemable():
        return max(0, stats['total_score'] - stats['redeemed_points'] * 2)

    class Button:
        def __init__(self, x, y, w, h, text, font=FONT_MEDIUM,
                     bg=Colors.BTN_BG, hover=Colors.BTN_HOVER,
                     tc=Colors.TEXT_MAIN, accent=False, radius=10,
                     toggle=False, active_color=None):
            self.rect = pygame.Rect(x, y, w, h)
            self.text = text
            self.font = font
            self.bg = bg
            self.hover_bg = hover
            self.tc = tc
            self.accent = accent
            self.radius = radius
            self.toggle = toggle
            self.active_color = active_color if active_color else Colors.SPEED_ACTIVE
            self.is_hovered = False
            self.active = False

        def draw(self, surface):
            if self.toggle and self.active:
                color = self.active_color
            elif self.accent:
                color = Colors.ACCENT_HOVER if self.is_hovered else Colors.ACCENT
            elif self.active and not self.toggle:
                color = Colors.SPEED_ACTIVE
            else:
                color = self.hover_bg if self.is_hovered else self.bg
            shadow = self.rect.copy()
            shadow.y += 2
            pygame.draw.rect(surface, (0,0,0,30), shadow, border_radius=self.radius)
            pygame.draw.rect(surface, color, self.rect, border_radius=self.radius)
            if self.active:
                pygame.draw.rect(surface, Colors.ACCENT, self.rect, 2, border_radius=self.radius)
            txt = self.font.render(self.text, True, self.tc)
            tr = txt.get_rect(center=self.rect.center)
            surface.blit(txt, tr)

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

        def scroll(self, direction):
            self.scroll_offset += direction * 30
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

        def handle_wheel(self, event):
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 4: self.scroll(-1); return True
                elif event.button == 5: self.scroll(1); return True
            return False

        def draw(self, surface, title_text, lines):
            self.content_height = len(lines) * self.line_h + 20
            visible_height = self.H - 90
            self.max_scroll = max(0, self.content_height - visible_height)
            overlay = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill(Colors.OVERLAY)
            surface.blit(overlay, (0,0))
            pygame.draw.rect(surface, Colors.BG_MID, self.rect, border_radius=16)
            pygame.draw.rect(surface, Colors.PANEL_BORDER, self.rect, 2, border_radius=16)
            title_surf = FONT_LARGE.render(title_text, True, Colors.ACCENT)
            tr = title_surf.get_rect(center=(self.rect.centerx, self.rect.y+30))
            surface.blit(title_surf, tr)
            pygame.draw.line(surface, Colors.PANEL_BORDER,
                             (self.rect.x+30, self.rect.y+60),
                             (self.rect.right-30, self.rect.y+60), 1)
            clip_rect = pygame.Rect(self.rect.x+4, self.rect.y+66, self.W-8, visible_height)
            surface.set_clip(clip_rect)
            y0 = self.rect.y + 76 - self.scroll_offset
            for i, line in enumerate(lines):
                yy = y0 + i * self.line_h
                if yy + self.line_h < self.rect.y+66 or yy > self.rect.y+66+visible_height:
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
                bar_x = self.rect.right - 14
                bar_y = self.rect.y + 66
                bar_h = visible_height
                pygame.draw.rect(surface, Colors.SCROLL_BAR_BG, (bar_x, bar_y, 8, bar_h), border_radius=4)
                thumb_h = max(20, int(bar_h*(visible_height/self.content_height)))
                thumb_y = bar_y + int((self.scroll_offset/self.max_scroll)*(bar_h-thumb_h))
                pygame.draw.rect(surface, Colors.SCROLL_BAR, (bar_x, thumb_y, 8, thumb_h), border_radius=4)
            hint = FONT_MICRO.render(T("scroll_close"), True, Colors.TEXT_DARK)
            hr = hint.get_rect(center=(self.rect.centerx, self.rect.bottom-16))
            surface.blit(hint, hr)

    class SnakeGame:
        def __init__(self):
            self.reset()

        def reset(self):
            cx, cy = GRID_SIZE//2, GRID_SIZE//2
            self.snake = [(cx,cy),(cx-1,cy),(cx-2,cy)]
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

        def _spawn_food(self):
            occ = set(self.snake)
            while True:
                p = (random.randint(0,GRID_SIZE-1), random.randint(0,GRID_SIZE-1))
                if p not in occ:
                    return p

        def change_direction(self, nd):
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
            self.direction = nd; self.next_direction = nd; self.input_queue.clear()
            return True

        def update(self, dt_sec):
            nonlocal edge_kills, session_time
            if self.game_over: return True
            if self.mode == "timed":
                self.time_left -= dt_sec
                if self.time_left <= 0:
                    self.time_left = 0; self.game_over = True; return True
            if self.input_queue:
                self.next_direction = self.input_queue.pop(0)
            self.direction = self.next_direction
            hx, hy = self.snake[0]; dx, dy = self.direction; nh = (hx+dx, hy+dy)
            wall = False
            if nh[0] < 0 or nh[0] >= GRID_SIZE or nh[1] < 0 or nh[1] >= GRID_SIZE:
                if edge_kills: self.game_over = True; return True
                wall = True
                if nh[0] < 0:
                    nh = (0, hy)
                    if not self._try_dir((0,1)): self._try_dir((0,-1))
                elif nh[0] >= GRID_SIZE:
                    nh = (GRID_SIZE-1, hy)
                    if not self._try_dir((0,1)): self._try_dir((0,-1))
                elif nh[1] < 0:
                    nh = (hx, 0)
                    if not self._try_dir((1,0)): self._try_dir((-1,0))
                elif nh[1] >= GRID_SIZE:
                    nh = (hx, GRID_SIZE-1)
                    if not self._try_dir((1,0)): self._try_dir((-1,0))
            if not wall and nh in self.snake: self.game_over = True; return True
            self.snake.insert(0, nh)
            if nh == self.food:
                self.food_eaten += 1; self.multiplier = 2**(self.food_eaten//10)
                self.score += self.multiplier; self.food = self._spawn_food()
            else:
                if wall: self.snake.pop(0)
                else: self.snake.pop()
            return False

        def draw(self, surface):
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    r = (GRID_X+x*CELL_SIZE, GRID_Y+y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    c = Colors.GRID_EVEN if (x+y)%2==0 else Colors.GRID_ODD
                    pygame.draw.rect(surface, c, r)
            fx, fy = self.food
            fc = (GRID_X+fx*CELL_SIZE+CELL_SIZE//2, GRID_Y+fy*CELL_SIZE+CELL_SIZE//2)
            for rad in range(14,6,-2):
                g = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
                pygame.draw.circle(g, (*Colors.FOOD_MAIN, max(0,40-rad*2)), fc, rad)
                surface.blit(g, (0,0))
            pygame.draw.circle(surface, Colors.FOOD_MAIN, fc, 9)
            pygame.draw.circle(surface, Colors.FOOD_GLOW, fc, 5)
            seg_n = len(self.snake)
            for i,(sx,sy) in enumerate(self.snake):
                r = (GRID_X+sx*CELL_SIZE+2, GRID_Y+sy*CELL_SIZE+2, CELL_SIZE-4, CELL_SIZE-4)
                if i == 0:
                    pygame.draw.rect(surface, Colors.SNAKE_HEAD, r, border_radius=7)
                    dx, dy = self.direction
                    e1 = (GRID_X+sx*CELL_SIZE+7, GRID_Y+sy*CELL_SIZE+7)
                    e2 = (GRID_X+sx*CELL_SIZE+CELL_SIZE-9, GRID_Y+sy*CELL_SIZE+7)
                    pygame.draw.circle(surface, (255,255,255), e1, 4)
                    pygame.draw.circle(surface, (255,255,255), e2, 4)
                    pygame.draw.circle(surface, (20,20,20), (e1[0]+dx, e1[1]+dy), 2)
                    pygame.draw.circle(surface, (20,20,20), (e2[0]+dx, e2[1]+dy), 2)
                else:
                    t = i/max(seg_n,1); g = max(60, int(200*(1-t*0.6)))
                    pygame.draw.rect(surface, (0,g,max(80,int(g*0.75))), r, border_radius=5)
            pygame.draw.rect(surface, Colors.PANEL_BORDER, (GRID_X,GRID_Y,GRID_PX,GRID_PX), 2, border_radius=6)

    def load_stats():
        nonlocal stats
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE,'r',encoding='utf-8') as f:
                    loaded = json.load(f)
                    for k in stats:
                        if k not in loaded: loaded[k] = stats[k]
                    stats = loaded
            except: pass

    def save_stats():
        with open(SAVE_FILE,'w',encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

    load_stats()
    snake_game = SnakeGame()

    help_popup = ScrollablePopup(560, 420)
    dev_popup = ScrollablePopup(580, 400)
    update_popup = ScrollablePopup(600, 520)
    stats_popup = ScrollablePopup(560, 400)

    # ====================================================================
    #  按钮
    # ====================================================================
    SPEED_BTN_W, SPEED_BTN_H, SPEED_GAP = 95, 38, 8
    SPEED_TOTAL = 4*SPEED_BTN_W + 3*SPEED_GAP
    sx0 = WINDOW_WIDTH//2 - SPEED_TOTAL//2
    speed_btns = []
    for i,sp in enumerate(SPEED_PRESETS):
        btn = Button(sx0+i*(SPEED_BTN_W+SPEED_GAP), 205, SPEED_BTN_W, SPEED_BTN_H,
                     sp["name"][current_lang], FONT_SMALL, radius=6)
        btn.speed_index = i
        btn.active = (i == current_speed_index)
        speed_btns.append(btn)

    speed_card_rect = pygame.Rect((WINDOW_WIDTH-440)//2, 150, 440, 106)

    mode_btn = Button(WINDOW_WIDTH//2-200, 285, 180, 38,
                      T("mode"), FONT_SMALL, radius=8,
                      toggle=True, active_color=Colors.BLUE_BTN)
    mode_btn.active = True

    edge_btn = Button(WINDOW_WIDTH//2+20, 285, 180, 38,
                      T("edge_slide"), FONT_SMALL, radius=8,
                      toggle=True, active_color=Colors.GREEN_BTN)
    edge_btn.active = True

    start_btn = Button((WINDOW_WIDTH-170)//2, 350, 170, 50,
                       T("start"), FONT_MEDIUM, accent=True, radius=12)

    btn_y = 530
    help_btn = Button(WINDOW_WIDTH//2-230, btn_y, 100, 36,
                      T("help"), FONT_SMALL, radius=8)
    stats_btn = Button(WINDOW_WIDTH//2-115, btn_y, 100, 36,
                       T("stats"), FONT_SMALL, radius=8)
    update_btn = Button(WINDOW_WIDTH//2, btn_y, 100, 36,
                        T("update"), FONT_SMALL, radius=8)
    dev_btn = Button(WINDOW_WIDTH//2+115, btn_y, 100, 36,
                     T("dev"), FONT_SMALL, radius=8)

    shop_btn = Button(15, 200, 100, 42,
                      T("shop"), FONT_SMALL,
                      bg=(60,40,20), hover=(80,60,30),
                      tc=Colors.SHOP_GOLD, radius=8)

    music_btn_x = WINDOW_WIDTH - 160
    music_btn_y = WINDOW_HEIGHT - 50
    music_btn = Button(music_btn_x, music_btn_y, 90, 36,
                       T("music"), FONT_SMALL, radius=8)

    lang_btn_x = music_btn_x - 5
    lang_btn_y = music_btn_y - 42
    lang_btn = Button(lang_btn_x, lang_btn_y, 100, 36,
                      T("lang_en") if current_lang=="zh" else T("lang_zh"),
                      FONT_SMALL, radius=8,
                      toggle=True, active_color=Colors.SPEED_ACTIVE)
    lang_btn.active = True

    pause_btn = Button(GRID_X+GRID_PX+15, GRID_Y, 70, 34,
                       T("pause"), FONT_SMALL, radius=8)
    end_btn = Button(GRID_X+GRID_PX+15, GRID_Y+48, 70, 34,
                     T("end"), FONT_SMALL, bg=Colors.RED_BTN, hover=Colors.RED_BTN_H, radius=8)

    go_restart = Button((WINDOW_WIDTH-170)//2, 330, 170, 46,
                        T("restart"), FONT_MEDIUM, accent=True, radius=12)
    go_menu = Button((WINDOW_WIDTH-170)//2, 400, 170, 46,
                     T("back_menu"), FONT_MEDIUM, radius=12)

    MUSIC_POPUP_W = 480
    MUSIC_POPUP_H = 430
    music_popup_rect = pygame.Rect(
        (WINDOW_WIDTH-MUSIC_POPUP_W)//2, (WINDOW_HEIGHT-MUSIC_POPUP_H)//2,
        MUSIC_POPUP_W, MUSIC_POPUP_H
    )
    mp_btn_y = music_popup_rect.y + 130
    mp_prev_btn = Button(music_popup_rect.x+80, mp_btn_y, 70, 36,
                         T("prev"), FONT_SMALL, radius=8)
    mp_play_btn = Button(music_popup_rect.x+175, mp_btn_y, 90, 36,
                         T("pause_btn") if music_playing else T("play"), FONT_SMALL,
                         accent=True, radius=8)
    mp_next_btn = Button(music_popup_rect.x+290, mp_btn_y, 70, 36,
                         T("next"), FONT_SMALL, radius=8)

    SHOP_POPUP_W = 500
    SHOP_POPUP_H = 420
    shop_popup_rect = pygame.Rect(
        (WINDOW_WIDTH-SHOP_POPUP_W)//2, (WINDOW_HEIGHT-SHOP_POPUP_H)//2,
        SHOP_POPUP_W, SHOP_POPUP_H
    )

    # ====================================================================
    #  弹窗内容获取
    # ====================================================================
    def get_help_lines():
        return LANG[current_lang]["help_content"]

    def get_dev_lines():
        return LANG[current_lang]["dev_content"]

    def get_update_lines():
        return LANG[current_lang]["update_content"]

    def get_stats_lines():
        hours = stats['total_time'] // 3600
        minutes = (stats['total_time'] % 3600) // 60
        seconds = stats['total_time'] % 60
        time_str = f"{hours}h{minutes}m{seconds}s" if current_lang=="en" else f"{hours}时{minutes}分{seconds}秒"
        if hours == 0:
            time_str = f"{minutes}m{seconds}s" if current_lang=="en" else f"{minutes}分{seconds}秒"
        avg_score = stats['total_score'] // max(stats['games_played'], 1)
        return [
            f"[ {T('stats_title')} ]",
            "",
            f"  {T('total_score')}: {stats['total_score']}",
            f"  {T('games_played')}: {stats['games_played']}",
            f"  {T('play_time')}: {time_str}",
            f"  {T('avg_score')}: {avg_score}",
            "",
            f"═══   {T('mode_title')}   ═══",
            "",
            f"  {T('max_endless')}: {stats['endless_high']}",
            f"  {T('max_timed')}: {stats['timed_high']}",
        ]

    # ====================================================================
    #  音乐控制弹窗绘制
    # ====================================================================
    def draw_music_popup(surface):
        overlay = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(Colors.OVERLAY)
        surface.blit(overlay, (0,0))
        pygame.draw.rect(surface, Colors.BG_MID, music_popup_rect, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, music_popup_rect, 2, border_radius=16)
        title = FONT_LARGE.render(T("music").upper() if current_lang=="en" else "音 乐 控 制", True, Colors.ACCENT)
        tr = title.get_rect(center=(music_popup_rect.centerx, music_popup_rect.y+28))
        surface.blit(title, tr)
        pygame.draw.line(surface, Colors.PANEL_BORDER,
                         (music_popup_rect.x+30, music_popup_rect.y+58),
                         (music_popup_rect.right-30, music_popup_rect.y+58), 1)
        current_name = music_names[music_index] if music_total > 0 else T("no_music")
        if len(current_name) > 35: current_name = current_name[:32]+"..."
        np_text = f"{T('current_playing')}: {current_name}"
        np = FONT_SMALL.render(np_text, True, Colors.TEXT_MAIN)
        surface.blit(np, (music_popup_rect.x+30, music_popup_rect.y+72))
        st_text = T("playing_status") if music_playing else T("paused_status")
        st_color = Colors.GREEN_BTN if music_playing else Colors.TEXT_DIM
        st = FONT_SMALL.render(f"{T('status')}: {st_text}", True, st_color)
        surface.blit(st, (music_popup_rect.x+30, music_popup_rect.y+98))
        mp_prev_btn.draw(surface)
        mp_play_btn.draw(surface)
        mp_next_btn.draw(surface)
        vol_label = FONT_SMALL.render(T("volume"), True, Colors.TEXT_DIM)
        surface.blit(vol_label, (music_popup_rect.x+30, music_popup_rect.y+180))
        slider_x = music_popup_rect.x + 80
        slider_y = music_popup_rect.y + 188
        slider_w = 320; slider_h = 10
        pygame.draw.rect(surface, Colors.VOLUME_TRACK, (slider_x,slider_y,slider_w,slider_h), border_radius=5)
        fill_w = int(slider_w * music_volume)
        if fill_w > 0:
            pygame.draw.rect(surface, Colors.VOLUME_FILL, (slider_x,slider_y,fill_w,slider_h), border_radius=5)
        thumb_x = slider_x + fill_w - 6
        pygame.draw.rect(surface, Colors.ACCENT, (thumb_x, slider_y-4, 12, 18), border_radius=4)
        vol_pct = FONT_TINY.render(f"{int(music_volume*100)}%", True, Colors.TEXT_MAIN)
        surface.blit(vol_pct, (music_popup_rect.x+30, music_popup_rect.y+210))
        tl = FONT_SMALL.render(T("track_list"), True, Colors.TEXT_DIM)
        surface.blit(tl, (music_popup_rect.x+30, music_popup_rect.y+240))
        list_x = music_popup_rect.x + 30
        list_y = music_popup_rect.y + 265
        list_w = MUSIC_POPUP_W - 80; list_h = 120; item_h = 22
        clip_rect = pygame.Rect(list_x, list_y, list_w, list_h)
        surface.set_clip(clip_rect)
        max_scroll = max(0, music_total * item_h - list_h)
        for i, name in enumerate(music_names):
            yy = list_y + i*item_h - music_list_scroll
            if yy+item_h < list_y or yy > list_y+list_h: continue
            dn = name if len(name)<=28 else name[:25]+"..."
            marker = ">> " if i==music_index else "   "
            c = Colors.GOLD if i==music_index else Colors.TEXT_DIM
            txt = FONT_TINY.render(f"{marker}{i+1}. {dn}", True, c)
            surface.blit(txt, (list_x+5, yy+2))
        surface.set_clip(None)
        if max_scroll > 0:
            bar_x = list_x+list_w+5; bar_y = list_y; bar_h = list_h
            pygame.draw.rect(surface, Colors.SCROLL_BAR_BG, (bar_x,bar_y,6,bar_h), border_radius=3)
            thumb_h = max(12, int(bar_h*(list_h/(music_total*item_h))))
            thumb_y = bar_y + int((music_list_scroll/max_scroll)*(bar_h-thumb_h))
            pygame.draw.rect(surface, Colors.SCROLL_BAR, (bar_x,thumb_y,6,thumb_h), border_radius=3)
        hint = FONT_MICRO.render(T("scroll_close"), True, Colors.TEXT_DARK)
        hr = hint.get_rect(center=(music_popup_rect.centerx, music_popup_rect.bottom-16))
        surface.blit(hint, hr)

    # ====================================================================
    #  积分商店弹窗
    # ====================================================================
    shop_buttons_created = False
    exchange_btn = None
    exchange_10_btn = None
    exchange_50_btn = None
    exchange_all_btn = None
    shop_exchange_message = ""
    shop_message_timer = 0

    def draw_shop_popup(surface):
        nonlocal shop_buttons_created, exchange_btn, exchange_10_btn, exchange_50_btn, exchange_all_btn
        overlay = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(Colors.OVERLAY)
        surface.blit(overlay, (0,0))
        pygame.draw.rect(surface, Colors.BG_MID, shop_popup_rect, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, shop_popup_rect, 2, border_radius=16)
        title_text = T("shop_title")
        title = FONT_LARGE.render(title_text, True, Colors.SHOP_GOLD)
        tr = title.get_rect(center=(shop_popup_rect.centerx, shop_popup_rect.y+28))
        surface.blit(title, tr)
        pygame.draw.line(surface, Colors.PANEL_BORDER,
                         (shop_popup_rect.x+30, shop_popup_rect.y+58),
                         (shop_popup_rect.right-30, shop_popup_rect.y+58), 1)
        rate_txt = FONT_TINY.render(T("exchange_rate"), True, Colors.TEXT_DIM)
        surface.blit(rate_txt, (shop_popup_rect.x+40, shop_popup_rect.y+72))
        card_y = shop_popup_rect.y + 105
        card_w = 110; card_h = 80; card_gap = 10
        total_card_w = 3*card_w + 2*card_gap
        start_x = shop_popup_rect.x + (SHOP_POPUP_W-total_card_w)//2
        redeemable = get_redeemable(); redeemed = stats['redeemed_points']; total_score = stats['total_score']
        cards_data = [
            (T("redeemable"), str(redeemable), Colors.GREEN_BTN),
            (T("redeemed"), str(redeemed), Colors.RED_BTN),
            (T("total"), str(total_score), Colors.SHOP_GOLD),
        ]
        for i, (label, value, color) in enumerate(cards_data):
            cx = start_x + i*(card_w+card_gap)
            pygame.draw.rect(surface, Colors.PANEL_BG, (cx,card_y,card_w,card_h), border_radius=10)
            pygame.draw.rect(surface, Colors.PANEL_BORDER, (cx,card_y,card_w,card_h), 1, border_radius=10)
            lbl = FONT_MICRO.render(label, True, Colors.TEXT_DIM)
            lr = lbl.get_rect(center=(cx+card_w//2, card_y+18))
            surface.blit(lbl, lr)
            val = FONT_LARGE.render(value, True, color)
            vr = val.get_rect(center=(cx+card_w//2, card_y+50))
            surface.blit(val, vr)
        info_y = shop_popup_rect.y + 200
        cur_txt = FONT_SMALL.render(T("current_redeemable", redeemable), True, Colors.GOLD)
        surface.blit(cur_txt, (shop_popup_rect.x+35, info_y))
        high_txt = FONT_SMALL.render(T("history_total", total_score), True, Colors.TEXT_DIM)
        high_x = shop_popup_rect.right - 35 - high_txt.get_width()
        surface.blit(high_txt, (high_x, info_y))
        if not shop_buttons_created:
            exchange_btn = Button(shop_popup_rect.x+150, shop_popup_rect.y+245, 200, 46,
                                  T("exchange_1"), FONT_MEDIUM, accent=True, radius=12)
            btn_y = shop_popup_rect.y + 305
            btn_w = 100; btn_gap = 15
            total_btn_w = 3*btn_w + 2*btn_gap
            btn_start_x = shop_popup_rect.x + (SHOP_POPUP_W-total_btn_w)//2
            exchange_10_btn = Button(btn_start_x, btn_y, btn_w, 32, T("exchange_10"), FONT_SMALL, radius=8)
            exchange_50_btn = Button(btn_start_x+btn_w+btn_gap, btn_y, btn_w, 32, T("exchange_50"), FONT_SMALL, radius=8)
            exchange_all_btn = Button(btn_start_x+2*(btn_w+btn_gap), btn_y, btn_w, 32, T("exchange_all"), FONT_SMALL, radius=8)
            shop_buttons_created = True
        exchange_btn.draw(surface)
        exchange_10_btn.draw(surface)
        exchange_50_btn.draw(surface)
        exchange_all_btn.draw(surface)
        if shop_message_timer > 0:
            msg = FONT_TINY.render(shop_exchange_message, True, Colors.GOLD)
            mr = msg.get_rect(center=(shop_popup_rect.centerx, shop_popup_rect.y+365))
            surface.blit(msg, mr)
        hint = FONT_MICRO.render(T("click_close"), True, Colors.TEXT_DARK)
        hr = hint.get_rect(center=(shop_popup_rect.centerx, shop_popup_rect.bottom-14))
        surface.blit(hint, hr)
        return exchange_btn, exchange_10_btn, exchange_50_btn, exchange_all_btn

    # ====================================================================
    #  语言切换
    # ====================================================================
    def update_language():
        nonlocal mode_btn, edge_btn, start_btn, shop_btn, help_btn, stats_btn, update_btn, dev_btn
        nonlocal music_btn, lang_btn, pause_btn, end_btn, go_restart, go_menu
        nonlocal mp_prev_btn, mp_play_btn, mp_next_btn

        for i, btn in enumerate(speed_btns):
            btn.text = SPEED_PRESETS[i]["name"][current_lang]
        mode_btn.text = T("mode_timed") if game_mode=="timed" else T("mode")
        edge_btn.text = T("edge_death") if edge_kills else T("edge_slide")
        start_btn.text = T("start")
        shop_btn.text = T("shop")
        help_btn.text = T("help")
        stats_btn.text = T("stats")
        update_btn.text = T("update")
        dev_btn.text = T("dev")
        music_btn.text = T("music")
        lang_btn.text = T("lang_en") if current_lang=="zh" else T("lang_zh")
        pause_btn.text = T("resume") if paused else T("pause")
        end_btn.text = T("end")
        go_restart.text = T("restart")
        go_menu.text = T("back_menu")
        mp_prev_btn.text = T("prev")
        mp_play_btn.text = T("pause_btn") if music_playing else T("play")
        mp_next_btn.text = T("next")

    # ====================================================================
    #  绘制主菜单
    # ====================================================================
    def draw_menu(surface):
        for i in range(0, WINDOW_WIDTH, 60):
            ls = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(ls, (*Colors.BG_LIGHT,4), (i,0), (i,WINDOW_HEIGHT),1)
            surface.blit(ls, (0,0))
        title = FONT_TITLE.render(T("title"), True, Colors.ACCENT)
        tr = title.get_rect(center=(WINDOW_WIDTH//2, 55))
        ts = FONT_TITLE.render(T("title"), True, (0,0,0,30))
        tsr = ts.get_rect(center=(WINDOW_WIDTH//2+2, 57))
        surface.blit(ts, tsr)
        surface.blit(title, tr)
        sub = FONT_SMALL.render(T("subtitle"), True, Colors.TEXT_DIM)
        sr = sub.get_rect(center=(WINDOW_WIDTH//2, 100))
        surface.blit(sub, sr)
        pygame.draw.rect(surface, Colors.PANEL_BG, speed_card_rect, border_radius=10)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, speed_card_rect, 1, border_radius=10)
        lbl = FONT_SMALL.render(T("speed"), True, Colors.TEXT_DIM)
        lr = lbl.get_rect(center=(WINDOW_WIDTH//2, speed_card_rect.y+18))
        surface.blit(lbl, lr)
        for btn in speed_btns:
            btn.draw(surface)
        mode_btn.draw(surface)
        edge_btn.draw(surface)
        start_btn.draw(surface)
        stat_y = 460
        sc = pygame.Rect(WINDOW_WIDTH//2-200, stat_y-12, 400, 42)
        pygame.draw.rect(surface, Colors.PANEL_BG, sc, border_radius=8)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, sc, 1, border_radius=8)
        stat_text = f"{T('total_score')}:{stats['total_score']}  {T('max_endless')}:{stats['endless_high']}  {T('max_timed')}:{stats['timed_high']}  {T('games_played')}:{stats['games_played']}"
        st = FONT_MICRO.render(stat_text, True, Colors.TEXT_MAIN)
        str_ = st.get_rect(center=(WINDOW_WIDTH//2, stat_y+9))
        surface.blit(st, str_)
        shop_btn.draw(surface)
        help_btn.draw(surface)
        stats_btn.draw(surface)
        update_btn.draw(surface)
        dev_btn.draw(surface)
        lang_btn.draw(surface)
        music_btn.draw(surface)
        if music_total > 0:
            tip = FONT_MICRO.render(f"{T('track_label')}{music_index+1}/{music_total}", True, Colors.TEXT_DARK)
            surface.blit(tip, (music_btn_x-75, music_btn_y+10))
        ver = FONT_MICRO.render("v6.0", True, Colors.TEXT_DARK)
        surface.blit(ver, (WINDOW_WIDTH-60, WINDOW_HEIGHT-18))

    def draw_playing(surface, paused=False):
        snake_game.draw(surface)
        pygame.draw.rect(surface, Colors.PANEL_BG, (0,0,WINDOW_WIDTH,TOP_BAR_HEIGHT))
        pygame.draw.line(surface, Colors.BG_LIGHT, (0,TOP_BAR_HEIGHT), (WINDOW_WIDTH,TOP_BAR_HEIGHT), 2)
        sc_t = FONT_MEDIUM.render(f"{T('score')}: {snake_game.score}", True, Colors.TEXT_MAIN)
        surface.blit(sc_t, (18, 18))
        mc = Colors.GOLD if snake_game.multiplier>1 else Colors.TEXT_DIM
        mu_t = FONT_TINY.render(f"{T('multiplier')}: {snake_game.multiplier}x", True, mc)
        surface.blit(mu_t, (18, 48))
        mode_name = T("mode_label") + ": " + ("Endless" if current_lang=="en" else "无限")
        if snake_game.mode == "timed":
            mode_name = T("mode_label") + ": " + ("Timed" if current_lang=="en" else "限时")
        mode_t = FONT_TINY.render(mode_name, True, Colors.TEXT_DIM)
        surface.blit(mode_t, (GRID_X+5, 16))
        if snake_game.mode == "timed":
            mins = int(snake_game.time_left // 60)
            secs = int(snake_game.time_left % 60)
            time_str = f"{T('time_label')}: {mins:02d}:{secs:02d}"
            time_color = Colors.RED_BTN if snake_game.time_left<30 else Colors.GOLD
            time_t = FONT_MEDIUM.render(time_str, True, time_color)
            surface.blit(time_t, (GRID_X+5, 40))
        panel_x = GRID_X+GRID_PX+15
        panel_w = WINDOW_WIDTH-panel_x-15
        panel_y = GRID_Y+95; panel_h = 160
        panel_surf = pygame.Surface((panel_w,panel_h), pygame.SRCALPHA)
        panel_surf.fill(Colors.SCORE_PANEL)
        surface.blit(panel_surf, (panel_x,panel_y))
        pt = FONT_SMALL.render(T("real_time"), True, Colors.ACCENT)
        surface.blit(pt, (panel_x+6,panel_y+6))
        ps1 = FONT_TINY.render(f"{T('current')}: {snake_game.score}", True, Colors.TEXT_MAIN)
        surface.blit(ps1, (panel_x+6,panel_y+32))
        high_score = stats["endless_high"] if snake_game.mode=="endless" else stats["timed_high"]
        ps2 = FONT_TINY.render(f"{T('high_label')}: {high_score}", True, Colors.GOLD)
        surface.blit(ps2, (panel_x+6,panel_y+52))
        ps3 = FONT_TINY.render(f"{T('food_label')}: {snake_game.food_eaten}", True, Colors.TEXT_DIM)
        surface.blit(ps3, (panel_x+6,panel_y+72))
        pause_btn.draw(surface)
        end_btn.draw(surface)
        if paused:
            pause_overlay = pygame.Surface((GRID_PX,GRID_PX), pygame.SRCALPHA)
            pause_overlay.fill((0,0,0,180))
            surface.blit(pause_overlay, (GRID_X,GRID_Y))
            pause_text = FONT_TITLE.render(T("resume").upper() if current_lang=="en" else "已 暂 停", True, Colors.TEXT_MAIN)
            ptr = pause_text.get_rect(center=(GRID_X+GRID_PX//2,GRID_Y+GRID_PX//2))
            surface.blit(pause_text, ptr)
            pause_hint = FONT_SMALL.render(T("resume"), True, Colors.TEXT_DIM)
            phr = pause_hint.get_rect(center=(GRID_X+GRID_PX//2,GRID_Y+GRID_PX//2+50))
            surface.blit(pause_hint, phr)

    def draw_game_over(surface):
        snake_game.draw(surface)
        nonlocal flash_alpha
        if flash_alpha > 0:
            flash_surf = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255,255,255,flash_alpha))
            surface.blit(flash_surf, (0,0))

        overlay = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(Colors.OVERLAY)
        surface.blit(overlay, (0,0))

        go = FONT_TITLE.render(T("game_over"), True, Colors.ACCENT)
        gor = go.get_rect(center=(WINDOW_WIDTH//2, 70))
        gs = FONT_TITLE.render(T("game_over"), True, (0,0,0,30))
        gsr = gs.get_rect(center=(WINDOW_WIDTH//2+2, 72))
        surface.blit(gs, gsr)
        surface.blit(go, gor)

        # 得分卡片
        card_w = 380; card_h = 120
        card_x = WINDOW_WIDTH//2 - card_w//2; card_y = 95
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)
        pygame.draw.rect(surface, Colors.PANEL_BG, card_rect, border_radius=12)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, card_rect, 2, border_radius=12)

        # 左侧得分
        score_label = FONT_TINY.render(T("score_label"), True, Colors.TEXT_DIM)
        surface.blit(score_label, (card_x+18, card_y+10))
        score_value = FONT_TITLE.render(str(current_score), True, Colors.GOLD)
        svr = score_value.get_rect(midleft=(card_x+18, card_y+70))
        surface.blit(score_value, svr)

        # 右侧信息
        info_x = card_x + card_w - 180
        info_y_start = card_y + 15
        mode_name = "Endless" if snake_game.mode=="endless" else "Timed"
        info_texts = [
            f"{T('mode_label')}: {mode_name}",
            f"{T('multiplier')}: {snake_game.multiplier}x",
            f"{T('food_label')}: {snake_game.food_eaten}",
        ]
        for i, txt in enumerate(info_texts):
            it = FONT_TINY.render(txt, True, Colors.TEXT_DIM)
            surface.blit(it, (info_x, info_y_start + i*22))

        # 统计卡片
        stats_card_y = card_y + card_h + 12
        stats_card_rect = pygame.Rect(card_x, stats_card_y, card_w, 72)
        pygame.draw.rect(surface, Colors.PANEL_BG, stats_card_rect, border_radius=10)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, stats_card_rect, 1, border_radius=10)

        col_w = card_w // 3
        stat_items = [
            (T("max_endless"), str(stats['endless_high'])),
            (T("max_timed"), str(stats['timed_high'])),
            (T("total_score"), str(stats['total_score'])),
        ]
        for i, (label, value) in enumerate(stat_items):
            cx = card_x + i * col_w + col_w//2
            lbl = FONT_MICRO.render(label, True, Colors.TEXT_DIM)
            lr = lbl.get_rect(center=(cx, stats_card_y+18))
            surface.blit(lbl, lr)
            val = FONT_SMALL.render(value, True, Colors.TEXT_MAIN)
            vr = val.get_rect(center=(cx, stats_card_y+48))
            surface.blit(val, vr)

        # 动态布局
        next_y = stats_card_y + 85
        high_ref = stats['endless_high'] if snake_game.mode=='endless' else stats['timed_high']
        if current_score >= high_ref and current_score > 0:
            pulse = abs(math.sin(pygame.time.get_ticks()/300))
            gold_c = (255, int(215*pulse), 0)
            rec = FONT_LARGE.render(T("new_record"), True, gold_c)
            recr = rec.get_rect(center=(WINDOW_WIDTH//2, next_y))
            glow_surf = pygame.Surface((rec.get_width()+20, rec.get_height()+10), pygame.SRCALPHA)
            glow_surf.fill((*gold_c, 30))
            surface.blit(glow_surf, (recr.x-10, recr.y-5))
            surface.blit(rec, recr)
            next_y += 55

        pts_txt = FONT_TINY.render(f"{T('score_earned')}: +{current_score}", True, Colors.GREEN_BTN)
        ptr = pts_txt.get_rect(center=(WINDOW_WIDTH//2, next_y))
        surface.blit(pts_txt, ptr)
        next_y += 35

        go_restart.rect.y = next_y
        go_menu.rect.y = next_y + 55
        go_restart.draw(surface)
        go_menu.draw(surface)

    # ====================================================================
    #  主循环
    # ====================================================================
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("贪吃蛇 v6.0")
    clock = pygame.time.Clock()

    running = True
    move_timer = 0
    paused = False

    while running:
        dt = clock.tick(FPS)
        dt_sec = dt / 1000.0
        mp = pygame.mouse.get_pos()

        if flash_alpha > 0:
            flash_alpha -= 15
            if flash_alpha < 0: flash_alpha = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break

            if game_state == ST_POPUP:
                if popup_type == "shop":
                    if event.type == MOUSEBUTTONDOWN:
                        if not shop_popup_rect.collidepoint(event.pos):
                            game_state = ST_MENU; popup_type = None; continue
                        eb, e10, e50, eall = draw_shop_popup(screen)
                        if eall and eall.clicked(event):
                            r = get_redeemable()
                            if r >= 2:
                                gained = r//2; cost = gained*2
                                stats['redeemed_points'] += gained; save_stats()
                                shop_exchange_message = T("exchange_success", cost, gained)
                                shop_message_timer = 180
                            else:
                                shop_exchange_message = T("exchange_fail", 2); shop_message_timer = 120
                        elif e50 and e50.clicked(event):
                            r = get_redeemable()
                            if r >= 100:
                                stats['redeemed_points'] += 50; save_stats()
                                shop_exchange_message = T("exchange_success", 100, 50); shop_message_timer = 180
                            else:
                                shop_exchange_message = T("exchange_fail", 100); shop_message_timer = 120
                        elif e10 and e10.clicked(event):
                            r = get_redeemable()
                            if r >= 20:
                                stats['redeemed_points'] += 10; save_stats()
                                shop_exchange_message = T("exchange_success", 20, 10); shop_message_timer = 180
                            else:
                                shop_exchange_message = T("exchange_fail", 20); shop_message_timer = 120
                        elif eb and eb.clicked(event):
                            r = get_redeemable()
                            if r >= 2:
                                stats['redeemed_points'] += 1; save_stats()
                                shop_exchange_message = T("exchange_success", 2, 1); shop_message_timer = 180
                            else:
                                shop_exchange_message = T("exchange_fail", 2); shop_message_timer = 120
                    if shop_message_timer > 0: shop_message_timer -= 1

                elif popup_type == "music":
                    if event.type == MOUSEBUTTONDOWN:
                        if not music_popup_rect.collidepoint(event.pos):
                            game_state = ST_MENU; popup_type = None; continue
                        if mp_prev_btn.clicked(event): prev_music(); mp_play_btn.text = T("pause_btn")
                        if mp_play_btn.clicked(event):
                            if music_playing: pause_music(); mp_play_btn.text = T("play")
                            else: resume_music(); mp_play_btn.text = T("pause_btn")
                        if mp_next_btn.clicked(event): next_music(); mp_play_btn.text = T("pause_btn")
                        slider_x = music_popup_rect.x+80; slider_y = music_popup_rect.y+188; slider_w=320
                        tr = pygame.Rect(slider_x+int(slider_w*music_volume)-6, slider_y-4, 12, 18)
                        if tr.collidepoint(event.pos) or pygame.Rect(slider_x,slider_y,slider_w,10).collidepoint(event.pos):
                            dragging_volume = True
                            rel_x = max(0, min(event.pos[0]-slider_x, slider_w))
                            set_volume(rel_x/slider_w)
                        list_x = music_popup_rect.x+30; list_y = music_popup_rect.y+265
                        if list_y <= event.pos[1] < list_y+120:
                            idx = (event.pos[1]-list_y+music_list_scroll)//22
                            if 0 <= idx < music_total: play_music(idx); mp_play_btn.text = T("pause_btn")
                    elif event.type == MOUSEMOTION and dragging_volume:
                        slider_x = music_popup_rect.x+80; slider_w=320
                        rel_x = max(0, min(event.pos[0]-slider_x, slider_w))
                        set_volume(rel_x/slider_w)
                    elif event.type == MOUSEBUTTONUP: dragging_volume = False
                    if event.type == MOUSEBUTTONDOWN and event.button in (4,5):
                        ms = max(0, music_total*22-120)
                        if event.button == 4: music_list_scroll = max(0, music_list_scroll-30)
                        else: music_list_scroll = min(ms, music_list_scroll+30)

                else:
                    cp = None
                    if popup_type=="help": cp=help_popup
                    elif popup_type=="dev": cp=dev_popup
                    elif popup_type=="update": cp=update_popup
                    elif popup_type=="stats": cp=stats_popup
                    handled = False
                    if cp: handled = cp.handle_wheel(event)
                    if not handled and event.type==MOUSEBUTTONDOWN and event.button==1:
                        if cp and not cp.rect.collidepoint(event.pos):
                            game_state=ST_MENU; popup_type=None; cp.reset_scroll()

            elif game_state == ST_MENU:
                for btn in speed_btns:
                    if btn.clicked(event):
                        current_speed_index = btn.speed_index
                        for b in speed_btns: b.active=False
                        btn.active=True
                if start_btn.clicked(event):
                    snake_game.reset(); snake_game.mode=game_mode
                    game_state=ST_PLAYING; paused=False; session_time=0
                if mode_btn.clicked(event):
                    if game_mode=="endless":
                        game_mode="timed"; mode_btn.text=T("mode_timed"); mode_btn.active_color=Colors.RED_BTN
                    else:
                        game_mode="endless"; mode_btn.text=T("mode"); mode_btn.active_color=Colors.BLUE_BTN
                    mode_btn.active=True
                if edge_btn.clicked(event):
                    edge_kills=not edge_kills; edge_btn.active=not edge_btn.active
                    edge_btn.text=T("edge_death") if edge_kills else T("edge_slide")
                    edge_btn.active_color=Colors.RED_BTN if edge_kills else Colors.GREEN_BTN
                if shop_btn.clicked(event):
                    game_state=ST_POPUP; popup_type="shop"
                    shop_exchange_message=""; shop_message_timer=0
                if lang_btn.clicked(event):
                    current_lang = "en" if current_lang=="zh" else "zh"
                    update_language()
                    lang_btn.text = T("lang_en") if current_lang=="zh" else T("lang_zh")
                if music_btn.clicked(event):
                    game_state=ST_POPUP; popup_type="music"
                    music_list_scroll=0; mp_play_btn.text=T("pause_btn") if music_playing else T("play")
                if help_btn.clicked(event):
                    game_state=ST_POPUP; popup_type="help"; help_popup.reset_scroll()
                elif stats_btn.clicked(event):
                    game_state=ST_POPUP; popup_type="stats"; stats_popup.reset_scroll()
                elif update_btn.clicked(event):
                    game_state=ST_POPUP; popup_type="update"; update_popup.reset_scroll()
                elif dev_btn.clicked(event):
                    game_state=ST_POPUP; popup_type="dev"; dev_popup.reset_scroll()
                if event.type==KEYDOWN:
                    if event.key in (K_PLUS,K_EQUALS): set_volume(music_volume+0.1)
                    elif event.key==K_MINUS: set_volume(music_volume-0.1)

                start_btn.update(mp)
                for btn in speed_btns: btn.update(mp)
                mode_btn.update(mp); edge_btn.update(mp); shop_btn.update(mp)
                lang_btn.update(mp); music_btn.update(mp)
                help_btn.update(mp); stats_btn.update(mp); update_btn.update(mp); dev_btn.update(mp)

            elif game_state in (ST_PLAYING, ST_PAUSED):
                if pause_btn.clicked(event):
                    paused=not paused; game_state=ST_PAUSED if paused else ST_PLAYING
                    pause_btn.text=T("resume") if paused else T("pause")
                if end_btn.clicked(event):
                    current_score=snake_game.score
                    stats["total_score"]+=current_score; stats["games_played"]+=1
                    stats["total_time"]+=int(session_time)
                    if snake_game.mode=="endless":
                        if current_score>stats["endless_high"]: stats["endless_high"]=current_score
                    else:
                        if current_score>stats["timed_high"]: stats["timed_high"]=current_score
                    save_stats()
                    flash_alpha = 200
                    game_state=ST_GAME_OVER
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE: paused=False; game_state=ST_MENU
                    elif event.key==K_SPACE:
                        paused=not paused; game_state=ST_PAUSED if paused else ST_PLAYING
                        pause_btn.text=T("resume") if paused else T("pause")
                    elif not paused:
                        if event.key in (K_UP,K_w): snake_game.change_direction((0,-1))
                        elif event.key in (K_DOWN,K_s): snake_game.change_direction((0,1))
                        elif event.key in (K_LEFT,K_a): snake_game.change_direction((-1,0))
                        elif event.key in (K_RIGHT,K_d): snake_game.change_direction((1,0))
                pause_btn.update(mp); end_btn.update(mp)

            elif game_state == ST_GAME_OVER:
                if go_restart.clicked(event):
                    snake_game.reset(); snake_game.mode=game_mode
                    game_state=ST_PLAYING; paused=False; session_time=0
                elif go_menu.clicked(event): game_state=ST_MENU
                go_restart.update(mp); go_menu.update(mp)

        if game_state == ST_PLAYING and not paused:
            move_timer += dt
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
                        if current_score > stats["endless_high"]: stats["endless_high"] = current_score
                    else:
                        if current_score > stats["timed_high"]: stats["timed_high"] = current_score
                    save_stats()
                    flash_alpha = 200
                    game_state = ST_GAME_OVER

        screen.fill(Colors.BG_DARK)

        if game_state == ST_MENU:
            draw_menu(screen)
        elif game_state in (ST_PLAYING, ST_PAUSED):
            draw_playing(screen, paused)
        elif game_state == ST_GAME_OVER:
            draw_game_over(screen)
        elif game_state == ST_POPUP:
            if popup_type == "shop":
                draw_menu(screen)
                btns = draw_shop_popup(screen)
                for b in btns:
                    if b: b.update(mp)
            elif popup_type == "music":
                draw_menu(screen)
                draw_music_popup(screen)
                mp_prev_btn.update(mp); mp_play_btn.update(mp); mp_next_btn.update(mp)
            elif popup_type == "help":
                draw_menu(screen); help_popup.draw(screen, T("help_title"), get_help_lines())
            elif popup_type == "dev":
                draw_menu(screen); dev_popup.draw(screen, T("dev_title"), get_dev_lines())
            elif popup_type == "update":
                draw_menu(screen); update_popup.draw(screen, T("update_title"), get_update_lines())
            elif popup_type == "stats":
                draw_menu(screen); stats_popup.draw(screen, T("stats_title"), get_stats_lines())

        pygame.display.flip()

    stop_music()
    pygame.quit()

if __name__ == "__main__":
    main()
