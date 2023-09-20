from Module.ColorDefine import WHITE, BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE

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
SCORE = 0
BONUS = 10

# 背景音樂
BACKGROUND_MUSIC_PATH = "Assest/TetrisThemeSong.mp3";

# 消除音效
BACKGROUND_SOUND_EFFECTS_CLEAR_PATH = "Assest/ClearLaser.mp3";
