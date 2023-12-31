import pygame

import time
import variaviesGlobais
from mapa import getTesouro, getKey, mapa
from config import *
from inimigos import getBomba_V1, getBomba_V2, getInimsPos, getExplosao
import variaviesGlobais as p

# animacao 
direita = []  # vetor de imagens - sentido direita
esquerda = []  # vetor de imagens - sentido esquerda
cima = []  # vetor de imagens - sentido cima
baixo = []  # vetor de imagens - baixo
colisao = False
sentido = "r"
colide = []
p.novo_jogo()
def sheets_player():
    global frames, spt_wdt, spt_hgt, direita, esquerda, cima

    frames = pygame.image.load("images/joagador.png")
    spt_wdt = frames.get_width() / 4  # Largura de um sprite
    spt_hgt = frames.get_height() / 4  # Altura de um sprite

    # carrega as imagens da animação
    i = 3  # sentido para direita
    for j in range(4):
        tupla = (j * spt_wdt, i * spt_hgt)
        cima.append(tupla)


    i = 2  # sentido para esquerda
    for j in range(4):
        tupla = (j * spt_wdt, i * spt_hgt)
        direita.append(tupla)

    i = 1  # sentido para cima
    for j in range(4):
        tupla = (j * spt_wdt, i * spt_hgt)
        esquerda.append(tupla)

    i = 0  # sentido para baixo
    for j in range(4):
        tupla = (j * spt_wdt, i * spt_hgt)
        baixo.append(tupla)

arquivo_ranking = "ranking.txt"
# Função para salvar as pontuações em um arquivo.txt
def salvar_ranking(ranking, tempo):
    with open(arquivo_ranking, "a") as file:
        file.write(f"\n{tempo}\n")

# logica da movimentacao + colisoes
def animacao_player(dt):
    global direita, esquerda, cima, baixo, sentido, frames, spt_wdt, spt_hgt, old_x, old_y, posBombas, colisao, colide

    old_x = p.anim_pos_x
    old_y = p.anim_pos_y

    # movimentos do personagem
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        sentido = "r"
        if (p.anim_pos_x> 910):  # não deixa passar da borda
            p.anim_pos_x = 905
        p.anim_pos_x = p.anim_pos_x + (0.1 * dt)  # movimenta o personagem
        p.anim_time = p.anim_time + dt  # incrementa o tempo usando dt
        if p.anim_time > 100:  # quando acumular mais de 100 ms
            p.anim_frame += 1  # avança para proximo frame
            if p.anim_frame > 3:  # loop da animação
                p.anim_frame = 0
            p.anim_time = 0  # reinicializa a contagem do tempo
    if keys[pygame.K_LEFT]:
        sentido = "l"
        if (p.anim_pos_x < 1):  # não deixa passar da borda
            p.anim_pos_x = 2
        p.anim_pos_x = p.anim_pos_x - (0.1 * dt)
        p.anim_time = p.anim_time + dt
        if p.anim_time > 100:
            p.anim_frame += 1
            if p.anim_frame > 3:
                p.anim_frame = 0
            p.anim_time = 0
    if keys[pygame.K_UP]:
        sentido = "u"
        if (p.anim_pos_y < 1):
            p.anim_pos_y = 2
        p.anim_pos_y = p.anim_pos_y - (0.1 * dt)
        p.anim_time = p.anim_time + dt
        if p.anim_time > 100:
            p.anim_frame += 1
            if p.anim_frame > 3:
                p.anim_frame = 0
            p.anim_time = 0
    if keys[pygame.K_DOWN]:
        sentido = "d"
        if (p.anim_pos_y > 580):
            p.anim_pos_y = 575
        p.anim_pos_y = p.anim_pos_y + (0.1 * dt)
        p.anim_time = p.anim_pos_y + dt
        if p.anim_time > 100:
            p.anim_frame += 1
            if p.anim_frame > 3:
                p.anim_frame = 0
            p.anim_time = 0

    jogador_rect = pygame.Rect(p.anim_pos_x, p.anim_pos_y, spt_wdt, spt_hgt)
    jogador_rect = jogador_rect.inflate(-25, -20)
    textura3 = pygame.transform.scale(pygame.image.load("images/tijolo.png"), (22,22)) # c
    key = getKey()

    # verifica se o jogador está em contato com qualquer bloquinho "C"
    for i in range(20):
        for j in range(30):
            if (mapa[i][j] == 'C'):
                if jogador_rect.colliderect(textura3.get_rect(topleft=(j * 32, i * 32))):
                    p.anim_pos_x = old_x
                    p.anim_pos_y = old_y

    bomba1 = getBomba_V1()
    bomba2 = getBomba_V2()
    posBombas = getInimsPos()

    # verifica qual bomba atingiu o personagem
    tipo = 0
    if(jogador_rect.colliderect(bomba1.get_rect(topleft=(posBombas[0], posBombas[1])))):
        tipo = 1
    if(jogador_rect.colliderect(bomba2.get_rect(topleft=(posBombas[2], posBombas[3])))):
        tipo = 2
    if(tipo > 0):
        colisao = True
        # guarda em uma lista a posição x e a posição y do cavaleiro
        if(tipo == 1):
            colide.append(posBombas[0])
            colide.append(posBombas[1])
        elif(tipo == 2):
            colide.append(posBombas[2])
            colide.append(posBombas[3])

    # verifica se o jogador está em contato com a chave
    for i in range(20):
        for j in range(30):
            if ('K' in mapa[i][j]):
                key_collide = key.get_rect(topleft=(j*32, i*32))
                if jogador_rect.colliderect(key_collide.inflate(-25, -20)):
                    str = mapa[i][j]
                    str = str.replace("K", "")
                    mapa[i][j] = str
                    pygame.display.update()
                    p.qtdChaves +=1
                    
    # verifica se o jogador está em contato com o baú
    tresure = getTesouro()
    if(p.qtdChaves == 5):
        if jogador_rect.colliderect(tresure.get_rect(topleft=(835, 350))):
            p.vitoria = True
            salvar_ranking(arquivo_ranking, (p.tempo_atual/100))

def getColisao():
    return colisao

# desenha o personagem animado na tela
def draw_player(screen):
    global colisao
    if(colisao == True):
        colisao = False
        p.vida_atual -= 25
        time.sleep(0.1)
        exp = getExplosao()
        screen.blit(exp, (p.anim_pos_x, p.anim_pos_y))
        # colocar o cavaleiro para longe da bomba com o impacto
        p.anim_pos_x = colide[0] + 100
        p.anim_pos_y = colide[1] + 50

    if (sentido == "r"):  # direita
        aux = direita[p.anim_frame]
        screen.blit(frames, (p.anim_pos_x, p.anim_pos_y),
                    (aux[0], aux[1], spt_wdt, spt_hgt))
    elif (sentido == "l"):  # esquerda
        aux = esquerda[p.anim_frame]
        screen.blit(frames, (p.anim_pos_x, p.anim_pos_y),
                    (aux[0], aux[1], spt_wdt, spt_hgt))
    elif (sentido == "u"):  # cima
        aux = cima[p.anim_frame]
        screen.blit(frames, (p.anim_pos_x, p.anim_pos_y),
                    (aux[0], aux[1], spt_wdt, spt_hgt))
    elif (sentido == "d"):  # baixo
        aux = baixo[p.anim_frame]
        screen.blit(frames, (p.anim_pos_x, p.anim_pos_y),
                    (aux[0], aux[1], spt_wdt, spt_hgt))