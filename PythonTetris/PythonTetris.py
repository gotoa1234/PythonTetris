import pygame
import random
import sys
from Method.scoreboard import draw_score    # 引入scoreboard.py中的函式
from Method.scoreboard import CaculateScore # 引入scoreboard.py中的函式


# 遊戲標題
TITLE_NAME = "俄羅斯方塊-Python範例遊戲"

# 定義畫面更新頻率
SPEED_SCREEN_UPDATE = 60

# 定義方塊自動降落的速度
SPEED_SQUARE = SPEED_SCREEN_UPDATE / 6

# 定義常數
SCREEN_WIDTH = 300  #螢幕寬度
SCREEN_HEIGHT = 600 #螢幕高度
BOARD_WIDTH = 10    #版塊寬的格子數
BOARD_HEIGHT = 20   #版塊高的格子數
BLOCK_SIZE = BOARD_WIDTH + BOARD_HEIGHT #版塊總數

# 定義顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREY11 = (28, 28, 28)

# 定義方塊
SHAPES = [
    [[1, 1, 1, 1]],           # I型
    [[1, 1, 1], [0, 0, 1]],   # J型
    [[1, 1, 1], [1, 0, 0]],   # L型
    [[1, 1], [1, 1]],         # O塊
    [[0, 1, 1], [1, 1, 0]],   # T型
    [[1, 1, 0], [0, 1, 1]],   # S型
    [[0, 1], [1, 1], [0, 1]], # Z型
]

# 定義方塊出現的顏色
SHAPE_COLORS = [
    RED,
    GREEN,
    BLUE,
    YELLOW,
    CYAN,
    MAGENTA,
    ORANGE
]

# 分數、紅利定義
score = 0
bonus = 10

# 產生方塊
def generate_shape():
    shape_idx = random.randint(0, len(SHAPES) - 1)
    shape = SHAPES[shape_idx]
    color = SHAPE_COLORS[shape_idx]
    return shape, color

# 判斷是否碰撞 True:表示碰撞 False:表示合法
def is_collision(board, shape, offset_x, offset_y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                y_pos = row + offset_y
                x_pos = col + offset_x
                if x_pos < 0 or x_pos >= BOARD_WIDTH or y_pos >= BOARD_HEIGHT:
                    return True
                if y_pos >= 0 and board[y_pos][x_pos] != BLACK:
                    return True
    return False

# 繪製整個畫面
def shape_fall(bgm):
    global can_move, x, y, board, current_shape, current_color

    # 沒有碰撞，則當前方塊往下移動一步
    if not is_collision(board, current_shape, x, y + 1):
        y += 1
    else:
        # 方塊到底部了，將它固定在棋盤上
        for row in range(len(current_shape)):
            for col in range(len(current_shape[row])):
                if current_shape[row][col] == 1:
                    board[y + row][x + col] = current_color
        # 消除滿行
        remove_full_rows(board, bgm)
        # 產生新的方塊
        x, y = 3, 0
        current_shape, current_color = generate_shape()
        if is_collision(board, current_shape, x, y):
            can_move = False

# 消除方塊的邏輯
def remove_full_rows(board, bgm):
    global score, bonus
    full_rows = []
    row = len(board) - 1
    isDelete = False        
    while row >= 0:  # 從底部開始檢查行
        current_row = board[row]  # 儲存當前行的參考
        if all(cell != BLACK for cell in current_row):  # 使用儲存的參考進行檢查
            full_rows.append(row)
            isDelete = True    
        row -= 1

    if isDelete :
       bgm.play(1)
       for delRow in full_rows:
           del board[delRow]
           score = CaculateScore(delRow, BOARD_HEIGHT, score, bonus)

    # 在頂部補上新的空行，數量與刪除行數相等
    for _ in range(len(full_rows)):
        board.insert(0, [BLACK for _ in range(BOARD_WIDTH)])

# 繪製方塊單元格
def draw_block(screen, x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(screen, GREY11, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# 繪製方塊形狀
def draw_shape(screen, shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                draw_block(screen, x + col, y + row, color)

# 主程式
def main():
    # 初始化配置
    global move_direction, isRotate, x, y, current_shape, current_color, can_move, board # 全域變數
    move_direction = None
    isRotate = False
    x, y = 3, 0
    current_shape, current_color = generate_shape()
    can_move = True
    board = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    # 初始化
    pygame.init() # 初始化Pygame程序 
    pygame.mixer.init() # 初始化Pygame的音頻

    # 創建背景音樂、音效
    background_music = pygame.mixer.Sound("Assest/TetrisThemeSong.mp3") #音樂
    clear_bgm = pygame.mixer.Sound("Assest/ClearLaser.mp3") # 消除時音效
    background_music.play(-1)# -1 表示無限循環播放音樂
    
    # 創建遊戲視窗
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
    # 設置視窗標題
    pygame.display.set_caption(TITLE_NAME)  

    clock = pygame.time.Clock()
    drop_counter = 0  # 初始化計數器
    playing = True  # 標記遊戲是否正在進行中
    while playing:  # 遊戲進行中才執行遊戲迴圈
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False  # 設置playing為False，結束遊戲迴圈

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_direction = -1
                elif event.key == pygame.K_RIGHT:
                    move_direction = 1
                elif event.key == pygame.K_DOWN:
                    drop_counter = (SPEED_SQUARE - 1)  # 立即將計數器設置為SPEED_SQUARE - 1，讓方塊下次立即下落一格
                elif event.key == pygame.K_UP:
                    isRotate = True

        if move_direction is not None:
            new_x = x + move_direction
            if not is_collision(board, current_shape, new_x, y):
                x = new_x

        if isRotate:
            rotated_shape = [list(reversed(row)) for row in zip(*current_shape)]
            if not is_collision(board, rotated_shape, x, y):
                current_shape = rotated_shape

        move_direction = None
        isRotate = False

        # 使用計數器控制方塊下落速度
        drop_counter = drop_counter + 1
        if drop_counter >= SPEED_SQUARE:  # 方塊達到秒數，立刻下落一次
            shape_fall(clear_bgm)
            drop_counter = 0  # 重置計數器

        # 繪製遊戲畫面
        screen.fill(BLACK)
        for row in range(len(board)):
            for col in range(len(board[row])):
                draw_block(screen, col, row, board[row][col])

        draw_shape(screen, current_shape, x, y, current_color)

        # 新增繪製記分板的呼叫                
        draw_score(screen, score)

        pygame.display.flip()
        clock.tick(SPEED_SCREEN_UPDATE)  # 設置遊戲迴圈的更新頻率為每秒60次

        if not can_move:
            playing = False  # 設置playing為False，結束遊戲迴圈

    # 當遊戲結束時停止音樂
    background_music.stop()
    pygame.quit()    
    sys.exit()  # 使用sys.exit()終止程式

if __name__ == "__main__":
    main()