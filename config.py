import pygame
from Player import*
from inimigos import*


# constantes
width = 32 * 30 # largura da tela
height = 32 * 20 # altura da tela

cor_barra_cheia = (0, 255, 0)
cor_barra_vazia = (255, 0, 0)

largura_barra = 200
altura_barra = 20
posicao_barra = [50, 20]
vida_maxima = 100
vida_atual = 100
      
def barra_de_vida(screen):
    
    pygame.draw.rect(screen, cor_barra_cheia, (posicao_barra[0], posicao_barra[1], largura_barra, altura_barra))
    largura_atual = int((vida_atual / vida_maxima) * largura_barra)
    pygame.draw.rect(screen, cor_barra_vazia, (posicao_barra[0] + largura_atual, posicao_barra[1], largura_barra - largura_atual, altura_barra))

def chaves(screen):
    fonte = pygame.font.Font(None, 36)
    #pygame.draw.rect(screen, (255, 192, 0), (780, 20, 50, 100))
    texto = "Chaves: 0/5"
    text = fonte.render(texto, True, (255, 192, 0))
    screen.blit(text, (720, 20))