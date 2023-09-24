import pygame
from Module.ColorDefine import WHITE

def draw_score(screen, score):
   font = pygame.font.Font(None, 24)
   score_text = font.render(f"Score:{score}", True, WHITE)
   screen.blit(score_text, (10, 10))

# 計算分數 當前高度 * 10
def CaculateScore(row, board_height, score, bonus):
    score += (board_height - row) * 10 + bonus;
    bonus += 5
    return score, bonus