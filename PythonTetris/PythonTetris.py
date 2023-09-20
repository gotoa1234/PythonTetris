import pygame
import sys
from Method.scoreboard import draw_score, CaculateScore   # 引入scoreboard.py中的函式
from Method.PythonTetrisMethod import IsCollision, GenerateShape, DrawBlock, DrawShape, ShapeFall
from Module.PythonTetrisWindowDefine import TITLE_NAME, SPEED_SCREEN_UPDATE, SPEED_SQUARE, SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_WIDTH, BOARD_HEIGHT, BLOCK_SIZE, SHAPES, SHAPE_COLORS, SCORE, BONUS, BACKGROUND_MUSIC_PATH, BACKGROUND_SOUND_EFFECTS_CLEAR_PATH
from Module.ColorDefine import BLACK, RED

# 創建遊戲視窗
PythonTetris = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption(TITLE_NAME)
PythonTetris.fill(RED)

# 主程式
def main():
    # 初始化配置
    global move_direction, isRotate, x, y, current_shape, current_color, can_move, board, drop_Applus # 全域變數
    move_direction = None
    isRotate = False
    x, y = 3, 0
    current_shape, current_color = GenerateShape()
    can_move = True
    board = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    drop_Applus = 0

    # 初始化
    pygame.init() # 初始化Pygame程序 
    pygame.mixer.init() # 初始化Pygame的音頻

    # 創建背景音樂、音效
    background_music = pygame.mixer.Sound(BACKGROUND_MUSIC_PATH) #音樂
    clear_bgm = pygame.mixer.Sound(BACKGROUND_SOUND_EFFECTS_CLEAR_PATH) # 消除時音效
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
                    drop_Applus += 3 if drop_Applus == 0 else 50
                elif event.key == pygame.K_UP:
                    isRotate = True

        if move_direction is not None:
            new_x = x + move_direction
            if not IsCollision(board, current_shape, new_x, y):
                x = new_x

        if isRotate:
            rotated_shape = [list(reversed(row)) for row in zip(*current_shape)]
            if not IsCollision(board, rotated_shape, x, y):
                current_shape = rotated_shape

        move_direction = None
        isRotate = False

        # 使用計數器控制方塊下落速度
        drop_counter = drop_counter + 1 + drop_Applus
        if drop_counter >= SPEED_SQUARE:  # 方塊達到秒數，立刻下落一次
            can_move, x, y, board, current_shape, current_color, drop_Applus = ShapeFall(clear_bgm, can_move, x, y, board, current_shape, current_color, drop_Applus)
            drop_counter = 0  # 重置計數器

        # 繪製遊戲畫面
        screen.fill(BLACK)
        for row in range(len(board)):
            for col in range(len(board[row])):
                DrawBlock(screen, col, row, board[row][col])

        DrawShape(screen, current_shape, x, y, current_color)

        # 新增繪製記分板的呼叫                
        draw_score(screen, SCORE)

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