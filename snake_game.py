# CONFIGURAÇÕES INICIAIS
import pygame
import pygame.mixer
import random
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Snake_Game')
largura, altura = 800, 800
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()
som_comer = pygame.mixer.Sound("./sons/comer.wav")
som_game_over = pygame.mixer.Sound("./sons/game_over.wav")

# CORES
preto = (0, 0, 0)
branca = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
# PARAMETROS DO JOGO
tam_quadrado = 20
velocidade_jogo = 10


def gerar_comida():
    comida_x = round(random.randrange(0, largura-tam_quadrado) /
                     float(tam_quadrado))*float(tam_quadrado)
    comida_y = round(random.randrange(0, altura-tam_quadrado) /
                     float(tam_quadrado))*float(tam_quadrado)
    return comida_x, comida_y


def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho, tamanho])


def desenhar_cobra(tamanho_quadrado, pixels):
    for pixel in pixels:
        pygame.draw.rect(
            tela, verde, [pixel[0], pixel[1], tamanho_quadrado, tamanho_quadrado])


def desenhar_pontos(pontos, velocidade):
    fonte = pygame.font.SysFont('Helvetica', 25)
    texto = fonte.render(f'Pontos: {pontos}', True, branca)
    tela.blit(texto, [10, 10])


def selecionar_velocidade(tecla):
    velocidades = {
        pygame.K_DOWN: (0, tam_quadrado),
        pygame.K_UP: (0, -tam_quadrado),
        pygame.K_LEFT: (-tam_quadrado, 0),
        pygame.K_RIGHT: (tam_quadrado, 0)
    }
    if tecla in velocidades:
        return velocidades[tecla]
    else:
        return (0, 0)


def velocidade(velocidade_cobra):
    return velocidade_cobra + velocidade_jogo


def inicio_do_jogo():
    inicio_jogo = False
    while not inicio_jogo:
        tela.fill(preto)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                inicio_jogo = True
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if botao_iniciar_rect.collidepoint(mouse_x, mouse_y):
                    inicio_jogo = True
                    rodar_jogo()
        botao_iniciar_rect = pygame.draw.rect(tela, branca, [(
            largura / 2) - (3 * tam_quadrado), (altura / 2) - (1 * tam_quadrado), (6 * tam_quadrado), (2 * tam_quadrado)])
        fonte_2 = pygame.font.SysFont('Helvetica', 50)
        texto_2 = fonte_2.render('SNAKE GAME', True, branca)
        fonte = pygame.font.SysFont('Helvetica', 25)
        texto = fonte.render('INICIAR', True, preto)
        texto_rect = texto.get_rect()
        texto_rect_2 = texto_2.get_rect()
        texto_rect_2.center = (largura // 2, 40)
        texto_rect.center = botao_iniciar_rect.center
        tela.blit(texto_2, texto_rect_2)
        tela.blit(texto, texto_rect)

        pygame.display.update()


def rodar_jogo():
    fim_do_jogo = False
    x = largura/2
    y = altura/2
    velocidade_x = 0
    velocidade_y = 0
    tamanho_cobra = 1
    velocidade_cobra = 0
    pixels = []
    comida_x, comida_y = gerar_comida()

    while not fim_do_jogo:
        tela.fill(preto)
        # CRIAR LOOP INFINITO
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_do_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)
        # DESENHAR OBJETOS DO JOGO NA TELA
        # DESENHAR COMIDA
        desenhar_comida(tam_quadrado, comida_x, comida_y)
        # ATUALIZAR POSIÇÃO COBRA
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_do_jogo = True
            som_game_over.play()
            inicio_do_jogo()
        x += velocidade_x
        y += velocidade_y
        # DESENHAR COBRA
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_do_jogo = True
                som_game_over.play()
                inicio_do_jogo()
        desenhar_cobra(tam_quadrado, pixels)
        # DESENHAR PONTOS
        desenhar_pontos(tamanho_cobra - 1, velocidade_cobra)
        # ATUALIZAÇÃO DA TELA
        pygame.display.update()
        # GERAR NOVA COMIDA
        if x == comida_x and y == comida_y:
            som_comer.play()
            tamanho_cobra += 1
            velocidade_cobra += 1
            comida_x, comida_y = gerar_comida()

        relogio.tick(velocidade(velocidade_cobra))


inicio_do_jogo()
