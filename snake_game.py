"""
====================================================================
  🐍 贪吃蛇 - Snake Game  (v5.8 音乐控制窗口版)
  新增: 独立音乐控制窗口 | 音量滑块 | 曲目列表
  开发者: Chuanzhi Wang | B站: 1309420497
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

    # 音量滑块状态
    dragging_volume = False
    music_popup_scroll = 0

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
        {"name":"简单","fps":5},
        {"name":"普通","fps":9},
        {"name":"困难","fps":14},
        {"name":"地狱","fps":19},
    ]
    current_speed_index = 1
    edge_kills = False
    game_mode = "endless"
    TIMED_LIMIT = 180

    ST_MENU, ST_PLAYING, ST_PAUSED, ST_GAME_OVER, ST_POPUP = range(5)
    game_state = ST_MENU
    popup_type = None  # "help", "dev", "update", "stats", "music"

    stats = {
        "total_score": 0, "games_played": 0,
        "endless_high": 0, "timed_high": 0,
        "total_time": 0
    }
    current_score = 0
    session_time = 0

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
            overlay = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill(Colors.OVERLAY)
            surface.blit(overlay, (0,0))
            pygame.draw.rect(surface, Colors.BG_MID, self.rect, border_radius=16)
            pygame.draw.rect(surface, Colors.PANEL_BORDER, self.rect, 2, border_radius=16)
            title = FONT_LARGE.render(title_text, True, Colors.ACCENT)
            tr = title.get_rect(center=(self.rect.centerx, self.rect.y+30))
            surface.blit(title, tr)
            pygame.draw.line(surface, Colors.PANEL_BORDER,
                             (self.rect.x+30, self.rect.y+60),
                             (self.rect.right-30, self.rect.y+60), 1)
            clip_rect = pygame.Rect(self.rect.x+4, self.rect.y+66, self.W-8, visible_height)
            surface.set_clip(clip_rect)
            y0 = self.rect.y + 76 - self.scroll_offset
            for i, line in enumerate(lines):
                yy = y0 + i * self.line_h
                if yy + self.line_h < self.rect.y + 66 or yy > self.rect.y + 66 + visible_height:
                    continue
                if line.startswith("═══"):
                    c = Colors.ACCENT
                elif line.startswith("  v"):
                    c = Colors.GOLD
                elif line.startswith("  ["):
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
                thumb_h = max(20, int(bar_h * (visible_height / self.content_height)))
                thumb_y = bar_y + int((self.scroll_offset / self.max_scroll) * (bar_h - thumb_h))
                pygame.draw.rect(surface, Colors.SCROLL_BAR, (bar_x, thumb_y, 8, thumb_h), border_radius=4)
            hint = FONT_MICRO.render("滚轮滚动  |  点击外部关闭", True, Colors.TEXT_DARK)
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
            self.direction = nd
            self.next_direction = nd
            self.input_queue.clear()
            return True

        def update(self, dt_sec):
            nonlocal edge_kills, session_time
            if self.game_over:
                return True
            if self.mode == "timed":
                self.time_left -= dt_sec
                if self.time_left <= 0:
                    self.time_left = 0
                    self.game_over = True
                    return True
            if self.input_queue:
                self.next_direction = self.input_queue.pop(0)
            self.direction = self.next_direction
            hx, hy = self.snake[0]
            dx, dy = self.direction
            nh = (hx+dx, hy+dy)
            wall = False
            if nh[0] < 0 or nh[0] >= GRID_SIZE or nh[1] < 0 or nh[1] >= GRID_SIZE:
                if edge_kills:
                    self.game_over = True
                    return True
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
            if not wall and nh in self.snake:
                self.game_over = True
                return True
            self.snake.insert(0, nh)
            if nh == self.food:
                self.food_eaten += 1
                self.multiplier = 2 ** (self.food_eaten // 10)
                self.score += self.multiplier
                self.food = self._spawn_food()
            else:
                if wall:
                    self.snake.pop(0)
                else:
                    self.snake.pop()
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
                    t = i/max(seg_n,1)
                    g = max(60, int(200*(1-t*0.6)))
                    pygame.draw.rect(surface, (0,g,max(80,int(g*0.75))), r, border_radius=5)
            pygame.draw.rect(surface, Colors.PANEL_BORDER, (GRID_X,GRID_Y,GRID_PX,GRID_PX), 2, border_radius=6)

    def load_stats():
        nonlocal stats
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE,'r',encoding='utf-8') as f:
                    loaded = json.load(f)
                    for k in stats:
                        if k not in loaded:
                            loaded[k] = stats[k]
                    stats = loaded
            except:
                pass

    def save_stats():
        with open(SAVE_FILE,'w',encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

    load_stats()
    snake_game = SnakeGame()

    help_popup = ScrollablePopup(560, 420)
    dev_popup = ScrollablePopup(560, 380)
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
                     sp["name"], FONT_SMALL, radius=6)
        btn.speed_index = i
        btn.active = (i == current_speed_index)
        speed_btns.append(btn)

    speed_card_rect = pygame.Rect((WINDOW_WIDTH-440)//2, 150, 440, 106)

    mode_btn = Button(WINDOW_WIDTH//2-200, 285, 180, 38,
                      "模式: 无限", FONT_SMALL, radius=8,
                      toggle=True, active_color=Colors.BLUE_BTN)
    mode_btn.active = True

    edge_btn = Button(WINDOW_WIDTH//2+20, 285, 180, 38,
                      "边缘: 滑动", FONT_SMALL, radius=8,
                      toggle=True, active_color=Colors.GREEN_BTN)
    edge_btn.active = True

    start_btn = Button((WINDOW_WIDTH-170)//2, 350, 170, 50,
                       "开始游戏", FONT_MEDIUM, accent=True, radius=12)

    btn_y = 530
    help_btn = Button(WINDOW_WIDTH//2-230, btn_y, 100, 36,
                      "游戏说明", FONT_SMALL, radius=8)
    stats_btn = Button(WINDOW_WIDTH//2-115, btn_y, 100, 36,
                       "统计信息", FONT_SMALL, radius=8)
    update_btn = Button(WINDOW_WIDTH//2, btn_y, 100, 36,
                        "更新说明", FONT_SMALL, radius=8)
    dev_btn = Button(WINDOW_WIDTH//2+115, btn_y, 100, 36,
                     "开发者", FONT_SMALL, radius=8)

    # 右下角音乐按钮（点击打开音乐控制窗口）
    music_btn_x = WINDOW_WIDTH - 120
    music_btn_y = WINDOW_HEIGHT - 50
    music_btn = Button(music_btn_x, music_btn_y, 100, 36,
                       "音乐控制", FONT_SMALL, radius=8)

    # 游戏内按钮
    pause_btn = Button(GRID_X+GRID_PX+15, GRID_Y, 70, 34,
                       "暂停", FONT_SMALL, radius=8)
    end_btn = Button(GRID_X+GRID_PX+15, GRID_Y+48, 70, 34,
                     "结束", FONT_SMALL, bg=Colors.RED_BTN, hover=Colors.RED_BTN_H, radius=8)

    go_restart = Button((WINDOW_WIDTH-170)//2, 330, 170, 46,
                        "再来一局", FONT_MEDIUM, accent=True, radius=12)
    go_menu = Button((WINDOW_WIDTH-170)//2, 390, 170, 46,
                     "返回菜单", FONT_MEDIUM, radius=12)

    # ===== 音乐控制弹窗内的按钮 =====
    MUSIC_POPUP_W = 480
    MUSIC_POPUP_H = 430
    music_popup_rect = pygame.Rect(
        (WINDOW_WIDTH-MUSIC_POPUP_W)//2, (WINDOW_HEIGHT-MUSIC_POPUP_H)//2,
        MUSIC_POPUP_W, MUSIC_POPUP_H
    )

    # 弹窗内控制按钮
    mp_btn_y = music_popup_rect.y + 130
    mp_prev_btn = Button(music_popup_rect.x+80, mp_btn_y, 70, 36,
                         "<<", FONT_SMALL, radius=8)
    mp_play_btn = Button(music_popup_rect.x+175, mp_btn_y, 90, 36,
                         "暂停" if music_playing else "播放", FONT_SMALL,
                         accent=True, radius=8)
    mp_next_btn = Button(music_popup_rect.x+290, mp_btn_y, 70, 36,
                         ">>", FONT_SMALL, radius=8)

    # 弹窗内曲目列表滚动偏移
    music_list_scroll = 0

    # ====================================================================
    #  弹窗内容
    # ====================================================================
    HELP_LINES = [
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
        "[ 音乐控制 ]",
        "  点击右下角「音乐控制」按钮",
        "  在弹出窗口中操作音乐播放",
    ]

    DEV_LINES = [
        "[ 开发者信息 ]",
        "",
        "  作者    :  Chuanzhi Wang",
        "  邮箱    :  1827267356@qq.com",
        "  B站 UID :  1309420497",
        "",
        "  版本    :  5.8 (音乐控制窗口版)",
        "  引擎    :  Python 3 + Pygame",
        "",
        "[ 特别感谢 ]",
        "  感谢游玩本游戏，欢迎在B站反馈交流",
    ]

    UPDATE_LINES = [
        "═══════  v5.8 版本更新 ═══════",
        "",
        "  [新增] 独立音乐控制窗口",
        "    音量滑块可拖拽调节",
        "    显示完整曲目列表",
        "    点击曲目快速切换",
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
    ]

    def get_stats_lines():
        hours = stats['total_time'] // 3600
        minutes = (stats['total_time'] % 3600) // 60
        seconds = stats['total_time'] % 60
        time_str = f"{hours}时{minutes}分{seconds}秒" if hours > 0 else f"{minutes}分{seconds}秒"
        avg_score = stats['total_score'] // max(stats['games_played'], 1)
        return [
            "[ 详细统计数据 ]",
            "",
            f"  累计总分: {stats['total_score']}",
            f"  总游戏局数: {stats['games_played']}",
            f"  总游戏时长: {time_str}",
            f"  平均每局得分: {avg_score}",
            "",
            "═══  各模式最高分  ═══",
            "",
            f"  无限模式最高分: {stats['endless_high']}",
            f"  限时模式最高分: {stats['timed_high']}",
        ]

    # ====================================================================
    #  音乐控制弹窗绘制
    # ====================================================================
    def draw_music_popup(surface):
        overlay = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(Colors.OVERLAY)
        surface.blit(overlay, (0,0))

        # 弹窗背景
        pygame.draw.rect(surface, Colors.BG_MID, music_popup_rect, border_radius=16)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, music_popup_rect, 2, border_radius=16)

        # 标题
        title = FONT_LARGE.render("音 乐 控 制", True, Colors.ACCENT)
        tr = title.get_rect(center=(music_popup_rect.centerx, music_popup_rect.y+28))
        surface.blit(title, tr)
        pygame.draw.line(surface, Colors.PANEL_BORDER,
                         (music_popup_rect.x+30, music_popup_rect.y+58),
                         (music_popup_rect.right-30, music_popup_rect.y+58), 1)

        # 当前曲目
        current_name = music_names[music_index] if music_total > 0 else "无音乐"
        # 截断过长的文件名
        if len(current_name) > 35:
            current_name = current_name[:32] + "..."
        now_playing = FONT_SMALL.render(f"当前播放: {current_name}", True, Colors.TEXT_MAIN)
        surface.blit(now_playing, (music_popup_rect.x+30, music_popup_rect.y+72))

        # 播放状态
        status_text = "播放中" if music_playing else "已暂停"
        status_color = Colors.GREEN_BTN if music_playing else Colors.TEXT_DIM
        status = FONT_SMALL.render(f"状态: {status_text}", True, status_color)
        surface.blit(status, (music_popup_rect.x+30, music_popup_rect.y+98))

        # 控制按钮
        mp_prev_btn.draw(surface)
        mp_play_btn.draw(surface)
        mp_next_btn.draw(surface)

        # 音量区域
        vol_label = FONT_SMALL.render("音量", True, Colors.TEXT_DIM)
        surface.blit(vol_label, (music_popup_rect.x+30, music_popup_rect.y+180))

        # 音量滑块轨道
        slider_x = music_popup_rect.x + 80
        slider_y = music_popup_rect.y + 188
        slider_w = 320
        slider_h = 10
        track_rect = pygame.Rect(slider_x, slider_y, slider_w, slider_h)

        # 轨道背景
        pygame.draw.rect(surface, Colors.VOLUME_TRACK, track_rect, border_radius=5)
        # 填充部分
        fill_w = int(slider_w * music_volume)
        if fill_w > 0:
            fill_rect = pygame.Rect(slider_x, slider_y, fill_w, slider_h)
            pygame.draw.rect(surface, Colors.VOLUME_FILL, fill_rect, border_radius=5)

        # 滑块按钮
        thumb_x = slider_x + fill_w - 6
        thumb_rect = pygame.Rect(thumb_x, slider_y-4, 12, 18)
        pygame.draw.rect(surface, Colors.ACCENT, thumb_rect, border_radius=4)

        # 音量百分比
        vol_pct = FONT_TINY.render(f"{int(music_volume*100)}%", True, Colors.TEXT_MAIN)
        surface.blit(vol_pct, (music_popup_rect.x+30, music_popup_rect.y+210))

        # 曲目列表标题
        list_label = FONT_SMALL.render("曲目列表", True, Colors.TEXT_DIM)
        surface.blit(list_label, (music_popup_rect.x+30, music_popup_rect.y+240))

        # 曲目列表（可滚动区域）
        list_x = music_popup_rect.x + 30
        list_y = music_popup_rect.y + 265
        list_w = MUSIC_POPUP_W - 80
        list_h = 120
        item_h = 22

        # 裁剪区域
        clip_rect = pygame.Rect(list_x, list_y, list_w, list_h)
        surface.set_clip(clip_rect)

        # 计算最大滚动
        max_scroll = max(0, music_total * item_h - list_h)

        for i, name in enumerate(music_names):
            yy = list_y + i * item_h - music_list_scroll
            if yy + item_h < list_y or yy > list_y + list_h:
                continue
            # 截断显示
            display_name = name
            if len(display_name) > 28:
                display_name = display_name[:25] + "..."

            if i == music_index:
                # 当前曲目高亮
                marker = ">> "
                c = Colors.GOLD
            else:
                marker = "    "
                c = Colors.TEXT_DIM if not music_playing or i != music_index else Colors.TEXT_MAIN

            item_text = f"{marker}{i+1}. {display_name}"
            txt = FONT_TINY.render(item_text, True, c)
            surface.blit(txt, (list_x+5, yy+2))

        surface.set_clip(None)

        # 滚动条（曲目列表右侧）
        if max_scroll > 0:
            bar_x = list_x + list_w + 5
            bar_y = list_y
            bar_h = list_h
            pygame.draw.rect(surface, Colors.SCROLL_BAR_BG,
                             (bar_x, bar_y, 6, bar_h), border_radius=3)
            thumb_h = max(12, int(bar_h * (list_h / (music_total * item_h))))
            thumb_y = bar_y + int((music_list_scroll / max_scroll) * (bar_h - thumb_h))
            pygame.draw.rect(surface, Colors.SCROLL_BAR,
                             (bar_x, thumb_y, 6, thumb_h), border_radius=3)

        # 底部提示
        hint = FONT_MICRO.render("滚轮滚动列表  |  拖拽滑块调音量  |  点击外部关闭", True, Colors.TEXT_DARK)
        hr = hint.get_rect(center=(music_popup_rect.centerx, music_popup_rect.bottom-16))
        surface.blit(hint, hr)

        # 保存滑块区域供事件使用
        return slider_x, slider_y, slider_w, slider_h

    # ====================================================================
    #  绘制主菜单
    # ====================================================================
    def draw_menu(surface):
        for i in range(0, WINDOW_WIDTH, 60):
            ls = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(ls, (*Colors.BG_LIGHT,4), (i,0), (i,WINDOW_HEIGHT),1)
            surface.blit(ls, (0,0))
        title = FONT_TITLE.render("贪  吃  蛇", True, Colors.ACCENT)
        tr = title.get_rect(center=(WINDOW_WIDTH//2, 55))
        ts = FONT_TITLE.render("贪  吃  蛇", True, (0,0,0,30))
        tsr = ts.get_rect(center=(WINDOW_WIDTH//2+2, 57))
        surface.blit(ts, tsr)
        surface.blit(title, tr)
        sub = FONT_SMALL.render("经 典 重 现  ·  挑 战 高 分", True, Colors.TEXT_DIM)
        sr = sub.get_rect(center=(WINDOW_WIDTH//2, 100))
        surface.blit(sub, sr)
        pygame.draw.rect(surface, Colors.PANEL_BG, speed_card_rect, border_radius=10)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, speed_card_rect, 1, border_radius=10)
        lbl = FONT_SMALL.render("移动速度", True, Colors.TEXT_DIM)
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
        stat_text = f"总分:{stats['total_score']}  无限最高:{stats['endless_high']}  限时最高:{stats['timed_high']}  局数:{stats['games_played']}"
        st = FONT_MICRO.render(stat_text, True, Colors.TEXT_MAIN)
        str_ = st.get_rect(center=(WINDOW_WIDTH//2, stat_y+9))
        surface.blit(st, str_)
        help_btn.draw(surface)
        stats_btn.draw(surface)
        update_btn.draw(surface)
        dev_btn.draw(surface)

        # 音乐控制按钮（右下角）
        music_btn.draw(surface)
        # 当前播放状态小提示
        if music_total > 0:
            status_icon = "音符" if music_playing else "静音"
            status_c = Colors.GREEN_BTN if music_playing else Colors.TEXT_DARK
            tip = FONT_MICRO.render(f"曲目{music_index+1}/{music_total}", True, status_c)
            surface.blit(tip, (music_btn_x-85, music_btn_y+10))

        ver = FONT_MICRO.render("v5.8", True, Colors.TEXT_DARK)
        surface.blit(ver, (WINDOW_WIDTH-60, WINDOW_HEIGHT-18))

    def draw_playing(surface, paused=False):
        snake_game.draw(surface)
        pygame.draw.rect(surface, Colors.PANEL_BG, (0,0,WINDOW_WIDTH,TOP_BAR_HEIGHT))
        pygame.draw.line(surface, Colors.BG_LIGHT, (0,TOP_BAR_HEIGHT), (WINDOW_WIDTH,TOP_BAR_HEIGHT), 2)
        sc_t = FONT_MEDIUM.render(f"得分: {snake_game.score}", True, Colors.TEXT_MAIN)
        surface.blit(sc_t, (18, 18))
        mc = Colors.GOLD if snake_game.multiplier>1 else Colors.TEXT_DIM
        mu_t = FONT_TINY.render(f"倍率: {snake_game.multiplier}x", True, mc)
        surface.blit(mu_t, (18, 48))
        mode_name = "无限" if snake_game.mode == "endless" else "限时"
        mode_t = FONT_TINY.render(f"模式: {mode_name}", True, Colors.TEXT_DIM)
        surface.blit(mode_t, (GRID_X+5, 16))
        if snake_game.mode == "timed":
            mins = int(snake_game.time_left // 60)
            secs = int(snake_game.time_left % 60)
            time_str = f"时间: {mins:02d}:{secs:02d}"
            time_color = Colors.RED_BTN if snake_game.time_left < 30 else Colors.GOLD
            time_t = FONT_MEDIUM.render(time_str, True, time_color)
            surface.blit(time_t, (GRID_X+5, 40))
        panel_x = GRID_X+GRID_PX+15
        panel_w = WINDOW_WIDTH-panel_x-15
        panel_y = GRID_Y+95
        panel_h = 160
        panel_surf = pygame.Surface((panel_w,panel_h), pygame.SRCALPHA)
        panel_surf.fill(Colors.SCORE_PANEL)
        surface.blit(panel_surf, (panel_x,panel_y))
        pt = FONT_SMALL.render("实时分数", True, Colors.ACCENT)
        surface.blit(pt, (panel_x+6,panel_y+6))
        ps1 = FONT_TINY.render(f"本局: {snake_game.score}", True, Colors.TEXT_MAIN)
        surface.blit(ps1, (panel_x+6,panel_y+32))
        high_score = stats["endless_high"] if snake_game.mode=="endless" else stats["timed_high"]
        ps2 = FONT_TINY.render(f"最高: {high_score}", True, Colors.GOLD)
        surface.blit(ps2, (panel_x+6,panel_y+52))
        ps3 = FONT_TINY.render(f"食物: {snake_game.food_eaten}", True, Colors.TEXT_DIM)
        surface.blit(ps3, (panel_x+6,panel_y+72))
        pause_btn.draw(surface)
        end_btn.draw(surface)
        if paused:
            pause_overlay = pygame.Surface((GRID_PX,GRID_PX), pygame.SRCALPHA)
            pause_overlay.fill((0,0,0,180))
            surface.blit(pause_overlay, (GRID_X,GRID_Y))
            pause_text = FONT_TITLE.render("已 暂 停", True, Colors.TEXT_MAIN)
            ptr = pause_text.get_rect(center=(GRID_X+GRID_PX//2,GRID_Y+GRID_PX//2))
            surface.blit(pause_text, ptr)
            pause_hint = FONT_SMALL.render("点击「继续」恢复游戏", True, Colors.TEXT_DIM)
            phr = pause_hint.get_rect(center=(GRID_X+GRID_PX//2,GRID_Y+GRID_PX//2+50))
            surface.blit(pause_hint, phr)

    def draw_game_over(surface):
        snake_game.draw(surface)
        overlay = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(Colors.OVERLAY)
        surface.blit(overlay, (0,0))
        go = FONT_TITLE.render("游 戏 结 束", True, Colors.ACCENT)
        gor = go.get_rect(center=(WINDOW_WIDTH//2, 85))
        gs = FONT_TITLE.render("游 戏 结 束", True, (0,0,0,30))
        gsr = gs.get_rect(center=(WINDOW_WIDTH//2+2, 87))
        surface.blit(gs, gsr)
        surface.blit(go, gor)
        sc = pygame.Rect(WINDOW_WIDTH//2-170, 120, 340, 150)
        pygame.draw.rect(surface, Colors.PANEL_BG, sc, border_radius=12)
        pygame.draw.rect(surface, Colors.PANEL_BORDER, sc, 1, border_radius=12)
        sc1 = FONT_MEDIUM.render(f"本局得分: {current_score}", True, Colors.TEXT_MAIN)
        sc1r = sc1.get_rect(center=(WINDOW_WIDTH//2, 155))
        surface.blit(sc1, sc1r)
        mode_name = "无限" if snake_game.mode=="endless" else "限时"
        sc1b = FONT_TINY.render(f"模式: {mode_name}  倍率: {snake_game.multiplier}x  已吃: {snake_game.food_eaten}个", True, Colors.TEXT_DIM)
        sc1br = sc1b.get_rect(center=(WINDOW_WIDTH//2, 180))
        surface.blit(sc1b, sc1br)
        sc2a = FONT_TINY.render(f"无限最高: {stats['endless_high']}", True, Colors.TEXT_DIM)
        sc2ar = sc2a.get_rect(midleft=(WINDOW_WIDTH//2-135, 205))
        surface.blit(sc2a, sc2ar)
        sc2b = FONT_TINY.render(f"限时最高: {stats['timed_high']}", True, Colors.TEXT_DIM)
        sc2br = sc2b.get_rect(midleft=(WINDOW_WIDTH//2+15, 205))
        surface.blit(sc2b, sc2br)
        sc2c = FONT_TINY.render(f"累计总分: {stats['total_score']}", True, Colors.TEXT_DIM)
        sc2cr = sc2c.get_rect(center=(WINDOW_WIDTH//2, 225))
        surface.blit(sc2c, sc2cr)
        high_ref = stats['endless_high'] if snake_game.mode=='endless' else stats['timed_high']
        if current_score >= high_ref and current_score > 0:
            rec = FONT_MEDIUM.render("新 纪 录 !", True, Colors.GOLD)
            recr = rec.get_rect(center=(WINDOW_WIDTH//2, 255))
            surface.blit(rec, recr)
        go_restart.draw(surface)
        go_menu.draw(surface)

    # ====================================================================
    #  主循环
    # ====================================================================
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("贪吃蛇 v5.8")
    clock = pygame.time.Clock()

    running = True
    move_timer = 0
    paused = False

    while running:
        dt = clock.tick(FPS)
        dt_sec = dt / 1000.0
        mp = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break

            # ===== 弹窗状态 =====
            if game_state == ST_POPUP:
                if popup_type == "music":
                    # ---- 音乐控制弹窗 ----
                    if event.type == MOUSEBUTTONDOWN:
                        # 检查是否点击了外部关闭
                        if not music_popup_rect.collidepoint(event.pos):
                            game_state = ST_MENU
                            popup_type = None
                            continue

                        # 控制按钮
                        if mp_prev_btn.clicked(event):
                            prev_music()
                            mp_play_btn.text = "暂停"
                        if mp_play_btn.clicked(event):
                            if music_playing:
                                pause_music()
                                mp_play_btn.text = "播放"
                            else:
                                resume_music()
                                mp_play_btn.text = "暂停"
                        if mp_next_btn.clicked(event):
                            next_music()
                            mp_play_btn.text = "暂停"

                        # 音量滑块点击
                        slider_x = music_popup_rect.x + 80
                        slider_y = music_popup_rect.y + 188
                        slider_w = 320
                        slider_h = 10
                        thumb_rect = pygame.Rect(
                            slider_x + int(slider_w * music_volume) - 6,
                            slider_y - 4, 12, 18
                        )
                        if thumb_rect.collidepoint(event.pos) or \
                           pygame.Rect(slider_x, slider_y, slider_w, slider_h).collidepoint(event.pos):
                            dragging_volume = True
                            # 计算点击位置的音量值
                            rel_x = event.pos[0] - slider_x
                            vol = max(0.0, min(1.0, rel_x / slider_w))
                            set_volume(vol)

                        # 曲目列表点击
                        list_x = music_popup_rect.x + 30
                        list_y = music_popup_rect.y + 265
                        item_h = 22
                        if list_y <= event.pos[1] < list_y + 120:
                            idx = (event.pos[1] - list_y + music_list_scroll) // item_h
                            if 0 <= idx < music_total:
                                play_music(idx)
                                mp_play_btn.text = "暂停"

                    elif event.type == MOUSEMOTION and dragging_volume:
                        slider_x = music_popup_rect.x + 80
                        slider_y = music_popup_rect.y + 188
                        slider_w = 320
                        # 限制鼠标在窗口内
                        mx = max(slider_x, min(event.pos[0], slider_x + slider_w))
                        rel_x = mx - slider_x
                        vol = max(0.0, min(1.0, rel_x / slider_w))
                        set_volume(vol)

                    elif event.type == MOUSEBUTTONUP:
                        dragging_volume = False

                    # 滚轮滚动曲目列表
                    if event.type == MOUSEBUTTONDOWN and event.button in (4, 5):
                        max_scroll = max(0, music_total * 22 - 120)
                        if event.button == 4:  # 上滚
                            music_list_scroll = max(0, music_list_scroll - 30)
                        elif event.button == 5:  # 下滚
                            music_list_scroll = min(max_scroll, music_list_scroll + 30)

                else:
                    # ---- 其他弹窗（帮助/开发者/更新/统计） ----
                    current_popup = None
                    if popup_type == "help": current_popup = help_popup
                    elif popup_type == "dev": current_popup = dev_popup
                    elif popup_type == "update": current_popup = update_popup
                    elif popup_type == "stats": current_popup = stats_popup
                    handled = False
                    if current_popup:
                        handled = current_popup.handle_wheel(event)
                    if not handled and event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if current_popup and not current_popup.rect.collidepoint(event.pos):
                            game_state = ST_MENU
                            popup_type = None
                            if current_popup:
                                current_popup.reset_scroll()

            # ===== 菜单状态 =====
            elif game_state == ST_MENU:
                for btn in speed_btns:
                    if btn.clicked(event):
                        current_speed_index = btn.speed_index
                        for b in speed_btns:
                            b.active = False
                        btn.active = True
                if start_btn.clicked(event):
                    snake_game.reset()
                    snake_game.mode = game_mode
                    game_state = ST_PLAYING
                    paused = False
                    session_time = 0
                if mode_btn.clicked(event):
                    if game_mode == "endless":
                        game_mode = "timed"
                        mode_btn.text = "模式: 限时"
                        mode_btn.active_color = Colors.RED_BTN
                    else:
                        game_mode = "endless"
                        mode_btn.text = "模式: 无限"
                        mode_btn.active_color = Colors.BLUE_BTN
                    mode_btn.active = True
                if edge_btn.clicked(event):
                    edge_kills = not edge_kills
                    edge_btn.active = not edge_btn.active
                    edge_btn.text = "边缘: 死亡" if edge_kills else "边缘: 滑动"
                    edge_btn.active_color = Colors.RED_BTN if edge_kills else Colors.GREEN_BTN
                if music_btn.clicked(event):
                    game_state = ST_POPUP
                    popup_type = "music"
                    music_list_scroll = 0
                    mp_play_btn.text = "暂停" if music_playing else "播放"
                if help_btn.clicked(event):
                    game_state = ST_POPUP; popup_type = "help"; help_popup.reset_scroll()
                elif stats_btn.clicked(event):
                    game_state = ST_POPUP; popup_type = "stats"; stats_popup.reset_scroll()
                elif update_btn.clicked(event):
                    game_state = ST_POPUP; popup_type = "update"; update_popup.reset_scroll()
                elif dev_btn.clicked(event):
                    game_state = ST_POPUP; popup_type = "dev"; dev_popup.reset_scroll()

                # 菜单中的音量快捷键
                if event.type == KEYDOWN:
                    if event.key in (K_PLUS, K_EQUALS):
                        set_volume(music_volume + 0.1)
                    elif event.key == K_MINUS:
                        set_volume(music_volume - 0.1)

                start_btn.update(mp)
                for btn in speed_btns:
                    btn.update(mp)
                mode_btn.update(mp)
                edge_btn.update(mp)
                music_btn.update(mp)
                help_btn.update(mp)
                stats_btn.update(mp)
                update_btn.update(mp)
                dev_btn.update(mp)

            # ===== 游戏/暂停状态 =====
            elif game_state in (ST_PLAYING, ST_PAUSED):
                if pause_btn.clicked(event):
                    paused = not paused
                    game_state = ST_PAUSED if paused else ST_PLAYING
                    pause_btn.text = "继续" if paused else "暂停"
                if end_btn.clicked(event):
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
                    game_state = ST_GAME_OVER
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        paused = False
                        game_state = ST_MENU
                    elif event.key == K_SPACE:
                        paused = not paused
                        game_state = ST_PAUSED if paused else ST_PLAYING
                    elif not paused:
                        if event.key in (K_UP, K_w):
                            snake_game.change_direction((0,-1))
                        elif event.key in (K_DOWN, K_s):
                            snake_game.change_direction((0,1))
                        elif event.key in (K_LEFT, K_a):
                            snake_game.change_direction((-1,0))
                        elif event.key in (K_RIGHT, K_d):
                            snake_game.change_direction((1,0))
                pause_btn.update(mp)
                end_btn.update(mp)

            # ===== 结算状态 =====
            elif game_state == ST_GAME_OVER:
                if go_restart.clicked(event):
                    snake_game.reset()
                    snake_game.mode = game_mode
                    game_state = ST_PLAYING
                    paused = False
                    session_time = 0
                elif go_menu.clicked(event):
                    game_state = ST_MENU
                go_restart.update(mp)
                go_menu.update(mp)

        # ---- 游戏逻辑 ----
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
                        if current_score > stats["endless_high"]:
                            stats["endless_high"] = current_score
                    else:
                        if current_score > stats["timed_high"]:
                            stats["timed_high"] = current_score
                    save_stats()
                    game_state = ST_GAME_OVER

        # ---- 渲染 ----
        screen.fill(Colors.BG_DARK)

        if game_state == ST_MENU:
            draw_menu(screen)
        elif game_state in (ST_PLAYING, ST_PAUSED):
            draw_playing(screen, paused)
        elif game_state == ST_GAME_OVER:
            draw_game_over(screen)
        elif game_state == ST_POPUP:
            if popup_type == "music":
                # 音乐控制弹窗（先画菜单背景，再叠加密度弹窗）
                draw_menu(screen)
                draw_music_popup(screen)
                # 更新弹窗内按钮
                mp_prev_btn.update(mp)
                mp_play_btn.update(mp)
                mp_next_btn.update(mp)
            elif popup_type == "help":
                draw_menu(screen)
                help_popup.draw(screen, "游 戏 说 明", HELP_LINES)
            elif popup_type == "dev":
                draw_menu(screen)
                dev_popup.draw(screen, "开 发 者 信 息", DEV_LINES)
            elif popup_type == "update":
                draw_menu(screen)
                update_popup.draw(screen, "更 新 说 明", UPDATE_LINES)
            elif popup_type == "stats":
                draw_menu(screen)
                stats_lines = get_stats_lines()
                stats_popup.draw(screen, "统 计 信 息", stats_lines)

        pygame.display.flip()

    stop_music()
    pygame.quit()

if __name__ == "__main__":
    main()
