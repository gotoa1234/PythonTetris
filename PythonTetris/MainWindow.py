import pygame
import sys

pygame.init()

# 視窗尺寸
window_size = (400, 300)

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 創建 A 視窗
MainWindow = pygame.display.set_mode(window_size)
pygame.display.set_caption('俄羅斯方塊')

# 開始遊戲按鈕
button_start_rect = pygame.Rect(150, 120, 100, 50)
# 離開遊戲按鈕
button_exit_rect = pygame.Rect(150, 200, 100, 50)

def draw_start_button():
    # 繪製按鈕
    pygame.draw.rect(MainWindow, BLACK, button_start_rect)

    # 創建字體物件
    font = pygame.font.Font(None, 30)
    font = pygame.font.SysFont("PMingLiU", 16)

    # 創建文字物件
    text = font.render("開始遊戲！", True, WHITE)

    # 繪製文字在按鈕上
    text_rect = text.get_rect(center=button_start_rect.center)
    MainWindow.blit(text, text_rect)

def draw_exit_button():    
    # 繪製按鈕
    pygame.draw.rect(MainWindow, BLACK, button_exit_rect)

    # 創建字體物件
    font = pygame.font.Font(None, 30)
    font = pygame.font.SysFont("PMingLiU", 16)

    # 創建文字物件
    text = font.render("離開遊戲！", True, WHITE)

    # 繪製文字在按鈕上
    text_rect = text.get_rect(center=button_exit_rect.center)
    MainWindow.blit(text, text_rect)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #底圖
            MainWindow.fill(WHITE)

            # 繪製按鈕
            draw_start_button()
            draw_exit_button()

            # 獲取滑鼠位置
            mouse_pos = pygame.mouse.get_pos()

            # 點擊 A 視窗的按鈕時切換到 B 視窗
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start_rect.collidepoint(mouse_pos):
                    import PythonTetris
                    PythonTetris.main()
                    pygame.quit()
                    sys.exit()
                elif button_exit_rect.collidepoint(mouse_pos):
                    pygame.display.set_mode((200, 100))
                    pygame.display.set_caption('提示訊息')
                    pygame.messagebox.showinfo('資訊', '歡迎使用 Pygame 提示訊息！')
                    pygame.quit()
                    sys.exit()

        # 更新顯示
        pygame.display.flip()

if __name__ == "__main__":
    main()
