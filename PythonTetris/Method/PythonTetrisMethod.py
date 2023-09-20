import pygame
import random
from Module.PythonTetrisWindowDefine import  BOARD_WIDTH, BOARD_HEIGHT, BLOCK_SIZE, SHAPES, SHAPE_COLORS, SCORE, BONUS
from Module.ColorDefine import BLACK, GREY11

# 判斷是否碰撞 True:表示碰撞 False:表示合法
def IsCollision(board, shape, offset_x, offset_y):
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


# 產生方塊
def GenerateShape():
    shape_idx = random.randint(0, len(SHAPES) - 1)
    shape = SHAPES[shape_idx]
    color = SHAPE_COLORS[shape_idx]
    return shape, color

# 繪製方塊單元格
def DrawBlock(screen, x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(screen, GREY11, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# 繪製方塊形狀
def DrawShape(screen, shape, x, y, color):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                DrawBlock(screen, x + col, y + row, color)

# 繪製整個畫面
def ShapeFall(bgm, can_move, x, y, board, current_shape, current_color, drop_Applus):

    # 沒有碰撞，則當前方塊往下移動一步
    if not IsCollision(board, current_shape, x, y + 1):
        y += 1
    else:
        # 重製
        drop_Applus = 0
        # 方塊到底部了，將它固定在棋盤上
        for row in range(len(current_shape)):
            for col in range(len(current_shape[row])):
                if current_shape[row][col] == 1:
                    board[y + row][x + col] = current_color
        # 消除滿行
        RemoveFullRows(board, bgm)
        # 產生新的方塊
        x, y = 3, 0
        current_shape, current_color = GenerateShape()
        if IsCollision(board, current_shape, x, y):
            can_move = False

    return can_move, x, y, board, current_shape, current_color, drop_Applus

# 消除方塊的邏輯
def RemoveFullRows(board, bgm):
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