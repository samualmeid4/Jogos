import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.load("humorous-loop-275485.mp3")
pygame.mixer.music.play(-1)

barulho_colisao = pygame.mixer.Sound("smw_coin.wav")

altura = 650
largura = 530

x_cobra = int(largura / 2)
y_cobra = int(altura / 2)

velocidade = 4
x_controle = velocidade
y_controle = 0

morreu = False
tempo_inicial = pygame.time.get_ticks()
tempo_para_aumentar = 15000

fonte = pygame.font.SysFont("mvboli", 25, True, True)
pontos = 0

# Configurações da tela
tela = pygame.display.set_mode((altura, largura))

imagem_fundo = pygame.image.load("Space.png")
pedra1 = pygame.image.load("pedra.jpg")
pedra2 = pygame.image.load("pedra.jpg")

cobra_img = pygame.image.load("cobra.jpg")
cobra_img = pygame.transform.scale(cobra_img, (20, 20))  # Ajustando o tamanho correto

pedra1 = pygame.transform.scale(pedra1, (30, 30))
pedra2 = pygame.transform.scale(pedra2, (30, 30))

pygame.display.set_caption("Meu jogo")
relogio = pygame.time.Clock()

lista_cobra = []
comprimento_cobra = 5

def desenha_fundo():
    tela.blit(imagem_fundo, (0, 0))

def desenha_pedra(x, y, imagem):
    tela.blit(imagem, (x, y))

def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        tela.blit(cobra_img, (XeY[0], XeY[1]))  # Desenhando a imagem corretamente

def reiniciar_jogo():
    global pontos, comprimento_cobra, x_cobra, y_cobra, lista_cobra, morreu, tempo_inicial, velocidade, x_controle, y_controle

    pontos = 0
    comprimento_cobra = 5
    x_cobra = int(largura // 2)
    y_cobra = int(altura // 2)
    lista_cobra = []
    velocidade = 4
    x_controle = velocidade
    y_controle = 0
    tempo_inicial = pygame.time.get_ticks()
    morreu = False

    # Garante que a maçã não aparece sobre uma pedra
    while True:
        x_maca = randint(40, 580)
        y_maca = randint(50, 430)
        maca_rect = pygame.Rect(x_maca, y_maca, 20, 20)
        if not (maca_rect.colliderect(pedra1_rect) or maca_rect.colliderect(pedra2_rect)):
            break

# Posicionamento inicial da maçã
while True:
    x_maca = randint(40, 580)
    y_maca = randint(50, 430)
    maca_rect = pygame.Rect(x_maca, y_maca, 20, 20)
    if not (maca_rect.colliderect(pygame.Rect(100, 120, 30, 30)) or maca_rect.colliderect(pygame.Rect(480, 400, 30, 30))):
        break

while True:
    relogio.tick(60)
    tela.fill((0, 0, 0))
    desenha_fundo()
    desenha_pedra(100, 120, pedra1)
    desenha_pedra(480, 400, pedra2)

    pedra1_rect = pedra1.get_rect(topleft=(100, 120))
    pedra2_rect = pedra2.get_rect(topleft=(480, 400))
    linha1 = pygame.draw.line(tela, (211, 211, 211), (630,20), (630,500), 8)
    linha2 = pygame.draw.line(tela, (211, 211, 211), (15,12), (15,500), 8)
    linha3 = pygame.draw.line(tela, (211, 211, 211), (15,15), (634,15), 8)
    linha4 = pygame.draw.line(tela, (211, 211, 211), (12,500), (634,500), 8)

    cobra_rect = pygame.Rect(x_cobra, y_cobra, 20, 20)

    mensagem = f"Pontos: {pontos}"
    texto_formatado = fonte.render(mensagem, True, (255, 255, 255))

    tempo_passado = pygame.time.get_ticks() - tempo_inicial
    if tempo_passado >= tempo_para_aumentar:
        velocidade += 2
        tempo_inicial = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if (event.key == K_a or event.key == K_LEFT) and x_controle != velocidade:
                x_controle = -velocidade
                y_controle = 0
            if (event.key == K_d or event.key == K_RIGHT) and x_controle != -velocidade:
                x_controle = velocidade
                y_controle = 0
            if (event.key == K_w or event.key == K_UP) and y_controle != velocidade:
                x_controle = 0
                y_controle = -velocidade
            if (event.key == K_s or event.key == K_DOWN) and y_controle != -velocidade:
                x_controle = 0
                y_controle = velocidade

    x_cobra += x_controle
    y_cobra += y_controle

    # Corrigindo a renderização da cobra
    lista_cabeca = [x_cobra, y_cobra]
    lista_cobra.append(lista_cabeca)

    # Desenhando a cobra corretamente
    aumenta_cobra(lista_cobra)

    # Removendo a parte antiga da cobra para manter o tamanho correto
    if len(lista_cobra) > comprimento_cobra:
        del lista_cobra[0]

    # Desenhando a maçã
    maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 20, 20))

    # Colisão com a maçã
    if cobra_rect.colliderect(maca):
        while True:
            x_maca = randint(40, 580)
            y_maca = randint(50, 430)
            maca_rect = pygame.Rect(x_maca, y_maca, 20, 20)
            if not (maca_rect.colliderect(pedra1_rect) or maca_rect.colliderect(pedra2_rect)):
                break
        pontos += 1
        barulho_colisao.play()
        comprimento_cobra += 1

    # Verifica se a cobra bateu nela mesma ou em uma pedra
    if lista_cobra.count(lista_cabeca) > 1 or cobra_rect.colliderect(pedra1_rect) or cobra_rect.colliderect(pedra2_rect) or cobra_rect.colliderect(linha1) or cobra_rect.colliderect(linha2) or cobra_rect.colliderect(linha3) or cobra_rect.colliderect(linha4):
        morreu = True
        while morreu:
            tela.fill((0, 0, 255))
            mensagem = "Game over! Pressione a tecla R para jogar novamente"
            texto_formatado = pygame.font.SysFont("arial", 20, True, True).render(mensagem, True, (255, 255, 255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN and event.key == K_r:
                    reiniciar_jogo()
            tela.blit(texto_formatado, (105, 260))
            pygame.display.update()

    # Ajustando limites da tela
    # if x_cobra >= largura:
    #     x_cobra = 0
    # if x_cobra < 0:
    #     x_cobra = largura - 20
    # if y_cobra < 0:
    #     y_cobra = altura - 20
    # if y_cobra >= altura:
    #     y_cobra = 0

    tela.blit(texto_formatado, (440, 40))
    pygame.display.update()
