import pygame
import random
import sys
import math

pygame.init()

LARGURA = 900
ALTURA = 550
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pescaria do Azar")

clock = pygame.time.Clock()

# CORES
CEU = (120, 200, 255)
MAR = (20, 110, 210)
MAR_ESCURO = (10, 80, 170)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (220, 40, 40)
AMARELO = (255, 220, 50)
LARANJA = (255, 150, 50)
CINZA = (120, 120, 120)
ROSA = (255, 120, 180)
MARROM = (120, 70, 30)
MADEIRA = (160, 95, 45)
PELE = (235, 180, 130)
AZUL_ROUPA = (40, 80, 200)
VERDE_DINHEIRO = (40, 180, 90)
VERDE_ESCURO = (20, 110, 50)
DOURADO = (255, 210, 40)

fonte = pygame.font.SysFont("arial", 32)
fonte_grande = pygame.font.SysFont("arial", 58)
fonte_pequena = pygame.font.SysFont("arial", 24)

# JOGO
pontos = 0
objetivo = 20
nivel = 1
mensagem = "Aperte ESPAÇO para lançar a vara!"
resultado = ""
fim_de_jogo = False
venceu = False
vitoria_final = False

# ANIMAÇÃO DE PESCA
pescando = False
tempo_pescando = 0
peixe_pendente = None
valor_pendente = 0

# ANIMAÇÃO DO TUBARÃO
ataque_tubarao = False
tempo_ataque = 0
barco_quebrado = False

# CENA MAGIKARP
cena_magikarp = False
aguardando_magikarp = False

# POSIÇÕES
barco_x = 330
barco_y = 285
pescador_x = barco_x + 230
pescador_y = barco_y - 85


def sortear_pescaria():
    numero = random.randint(1, 100)

    if nivel == 1:
        if numero <= 40:
            return "Tilápia", 1
        elif numero <= 70:
            return "Camarão", 2
        elif numero <= 90:
            return "Salmão", 3
        elif numero <= 94:
            return "Magikarp", 20
        else:
            return "Tubarão", 0

    elif nivel == 2:
        if numero <= 38:
            return "Tilápia", 1
        elif numero <= 58:
            return "Camarão", 2
        elif numero <= 70:
            return "Salmão", 3
        elif numero <= 75:
            return "Magikarp", 20
        else:
            return "Tubarão", 0

    else:
        if numero <= 35:
            return "Tilápia", 1
        elif numero <= 47:
            return "Camarão", 2
        elif numero <= 57:
            return "Salmão", 3
        elif numero <= 65:
            return "Magikarp", 20
        else:
            return "Tubarão", 0


def desenhar_texto(texto, fonte_usada, cor, x, y):
    imagem = fonte_usada.render(texto, True, cor)
    tela.blit(imagem, (x, y))


def desenhar_mar():
    tela.fill(CEU)
    pygame.draw.circle(tela, AMARELO, (760, 90), 45)
    pygame.draw.rect(tela, MAR, (0, 250, LARGURA, 300))

    tempo = pygame.time.get_ticks() / 300

    for y in range(270, ALTURA, 35):
        for x in range(-40, LARGURA, 90):
            offset = math.sin(tempo + x * 0.03 + y * 0.01) * 8
            pygame.draw.arc(tela, BRANCO, (x + offset, y, 60, 20), 0, math.pi, 3)

    pygame.draw.line(tela, MAR_ESCURO, (0, 250), (LARGURA, 250), 3)


def desenhar_barco():
    tremor_x = 0
    tremor_y = 0

    if ataque_tubarao and tempo_ataque > 80:
        tremor_x = random.randint(-4, 4)
        tremor_y = random.randint(-3, 3)

    x = barco_x + tremor_x
    y = barco_y + tremor_y

    pygame.draw.ellipse(tela, MAR_ESCURO, (x + 20, y + 90, 310, 35))

    if not barco_quebrado:
        pygame.draw.polygon(
            tela,
            MADEIRA,
            [
                (x, y + 45),
                (x + 340, y + 45),
                (x + 290, y + 115),
                (x + 55, y + 115),
            ]
        )

        pygame.draw.rect(tela, MARROM, (x + 25, y + 25, 290, 35))

        for i in range(4):
            pygame.draw.line(
                tela,
                MARROM,
                (x + 70 + i * 55, y + 60),
                (x + 50 + i * 55, y + 105),
                3
            )

    else:
        pygame.draw.polygon(
            tela,
            MADEIRA,
            [
                (x, y + 50),
                (x + 150, y + 40),
                (x + 125, y + 115),
                (x + 55, y + 120),
            ]
        )

        pygame.draw.polygon(
            tela,
            MADEIRA,
            [
                (x + 190, y + 40),
                (x + 340, y + 55),
                (x + 290, y + 120),
                (x + 210, y + 115),
            ]
        )

        pygame.draw.line(tela, PRETO, (x + 160, y + 40), (x + 175, y + 70), 5)
        pygame.draw.line(tela, PRETO, (x + 175, y + 70), (x + 160, y + 95), 5)
        pygame.draw.line(tela, PRETO, (x + 160, y + 95), (x + 180, y + 120), 5)

        pygame.draw.rect(tela, MARROM, (x + 120, y + 10, 35, 12))
        pygame.draw.rect(tela, MARROM, (x + 205, y + 15, 45, 12))
        pygame.draw.rect(tela, MADEIRA, (x + 170, y + 130, 50, 10))


def desenhar_pescador():
    offset_y = 20 if barco_quebrado else 0

    pygame.draw.line(tela, PRETO, (pescador_x - 10, pescador_y + 80 + offset_y), (pescador_x - 35, pescador_y + 120 + offset_y), 8)
    pygame.draw.line(tela, PRETO, (pescador_x + 10, pescador_y + 80 + offset_y), (pescador_x + 35, pescador_y + 120 + offset_y), 8)

    pygame.draw.rect(tela, AZUL_ROUPA, (pescador_x - 22, pescador_y + 30 + offset_y, 44, 55))
    pygame.draw.circle(tela, PELE, (pescador_x, pescador_y + 10 + offset_y), 22)

    pygame.draw.rect(tela, MARROM, (pescador_x - 30, pescador_y - 15 + offset_y, 60, 10))
    pygame.draw.rect(tela, MARROM, (pescador_x - 18, pescador_y - 35 + offset_y, 36, 25))

    pygame.draw.circle(tela, PRETO, (pescador_x - 7, pescador_y + 7 + offset_y), 3)
    pygame.draw.circle(tela, PRETO, (pescador_x + 7, pescador_y + 7 + offset_y), 3)

    if barco_quebrado:
        pygame.draw.circle(tela, PRETO, (pescador_x, pescador_y + 22 + offset_y), 5)

    pygame.draw.line(tela, PELE, (pescador_x + 20, pescador_y + 45 + offset_y), (pescador_x + 65, pescador_y + 25 + offset_y), 8)


def desenhar_vara():
    if barco_quebrado:
        return

    inicio_x = pescador_x + 60
    inicio_y = pescador_y + 25

    if pescando:
        progresso = min(tempo_pescando / 60, 1)

        ponta_x = inicio_x + 120 + progresso * 130
        ponta_y = inicio_y - 80 + progresso * 130

        boia_x = ponta_x
        boia_y = ponta_y + 85

        pygame.draw.line(tela, PRETO, (inicio_x, inicio_y), (ponta_x, ponta_y), 5)
        pygame.draw.line(tela, PRETO, (ponta_x, ponta_y), (boia_x, boia_y), 2)
        pygame.draw.circle(tela, VERMELHO, (int(boia_x), int(boia_y)), 8)

        if progresso > 0.8:
            pygame.draw.circle(tela, BRANCO, (int(boia_x), int(boia_y)), 18, 3)
            pygame.draw.circle(tela, BRANCO, (int(boia_x - 20), int(boia_y + 5)), 8, 2)
            pygame.draw.circle(tela, BRANCO, (int(boia_x + 20), int(boia_y + 5)), 8, 2)

    else:
        ponta_x = inicio_x + 170
        ponta_y = inicio_y - 55
        boia_x = ponta_x
        boia_y = ponta_y + 110

        pygame.draw.line(tela, PRETO, (inicio_x, inicio_y), (ponta_x, ponta_y), 5)
        pygame.draw.line(tela, PRETO, (ponta_x, ponta_y), (boia_x, boia_y), 2)
        pygame.draw.circle(tela, VERMELHO, (boia_x, boia_y), 8)


def desenhar_tubarao_ataque():
    if not ataque_tubarao:
        return

    if tempo_ataque < 80:
        progresso = tempo_ataque / 80
        x = -220 + progresso * 480
        y = 405
    else:
        x = 260
        y = 405

    pygame.draw.ellipse(tela, CINZA, (x, y - 40, 230, 90))
    pygame.draw.polygon(tela, CINZA, [(x + 80, y - 40), (x + 115, y - 115), (x + 150, y - 40)])
    pygame.draw.polygon(tela, CINZA, [(x, y + 5), (x - 70, y - 35), (x - 70, y + 55)])
    pygame.draw.circle(tela, PRETO, (x + 165, y - 5), 7)

    pygame.draw.polygon(tela, PRETO, [(x + 185, y + 20), (x + 225, y + 5), (x + 220, y + 38)])

    for i in range(4):
        pygame.draw.polygon(
            tela,
            BRANCO,
            [
                (x + 195 + i * 8, y + 16),
                (x + 199 + i * 8, y + 30),
                (x + 203 + i * 8, y + 16)
            ]
        )

    if tempo_ataque > 80:
        pygame.draw.circle(tela, BRANCO, (370, 360), 35, 4)
        pygame.draw.circle(tela, BRANCO, (330, 375), 20, 3)
        pygame.draw.circle(tela, BRANCO, (410, 380), 25, 3)
        pygame.draw.line(tela, BRANCO, (350, 330), (310, 280), 4)
        pygame.draw.line(tela, BRANCO, (385, 330), (430, 280), 4)


def desenhar_peixe(nome):
    x, y = 380, 400

    if nome == "Tilápia":
        pygame.draw.ellipse(tela, CINZA, (x, y, 90, 40))
        pygame.draw.polygon(tela, CINZA, [(x, y + 20), (x - 30, y), (x - 30, y + 40)])
        pygame.draw.circle(tela, PRETO, (x + 65, y + 14), 4)

    elif nome == "Camarão":
        pygame.draw.arc(tela, ROSA, (x, y, 90, 60), 0, math.pi, 8)
        pygame.draw.circle(tela, ROSA, (x + 75, y + 30), 14)
        pygame.draw.circle(tela, PRETO, (x + 80, y + 25), 3)

    elif nome == "Salmão":
        pygame.draw.ellipse(tela, LARANJA, (x, y, 115, 45))
        pygame.draw.polygon(tela, LARANJA, [(x, y + 22), (x - 35, y), (x - 35, y + 45)])
        pygame.draw.circle(tela, PRETO, (x + 85, y + 16), 4)


def desenhar_cena_magikarp():
    tela.fill((25, 25, 45))

    pygame.draw.rect(tela, DOURADO, (0, 370, LARGURA, 180))

    tempo = pygame.time.get_ticks() / 180

    for i in range(20):
        x = 40 + i * 45
        y = 80 + math.sin(tempo + i) * 20
        pygame.draw.circle(tela, AMARELO, (int(x), int(y)), 6)

    # pilha de dinheiro
    pygame.draw.ellipse(tela, VERDE_ESCURO, (250, 310, 400, 120))
    pygame.draw.ellipse(tela, VERDE_DINHEIRO, (280, 260, 340, 120))
    pygame.draw.ellipse(tela, VERDE_DINHEIRO, (320, 220, 260, 110))
    pygame.draw.ellipse(tela, VERDE_DINHEIRO, (360, 190, 180, 90))

    # notas
    for i in range(12):
        x = 260 + (i * 47) % 360
        y = 220 + (i * 29) % 150
        pygame.draw.rect(tela, VERDE_DINHEIRO, (x, y, 55, 25))
        pygame.draw.rect(tela, VERDE_ESCURO, (x, y, 55, 25), 3)
        pygame.draw.circle(tela, DOURADO, (x + 27, y + 12), 7)

    # moedas
    for i in range(16):
        x = 230 + (i * 41) % 430
        y = 375 + (i * 17) % 70
        pygame.draw.circle(tela, DOURADO, (x, y), 12)
        pygame.draw.circle(tela, AMARELO, (x, y), 7)

    # pescador pulando de felicidade no topo
    pulo = math.sin(tempo * 2) * 12
    px = 450
    py = 145 + pulo

    # pernas pulando
    pygame.draw.line(tela, PRETO, (px - 15, py + 95), (px - 55, py + 135), 9)
    pygame.draw.line(tela, PRETO, (px + 15, py + 95), (px + 55, py + 135), 9)

    # corpo
    pygame.draw.rect(tela, AZUL_ROUPA, (px - 28, py + 35, 56, 65))

    # cabeça
    pygame.draw.circle(tela, PELE, (px, py + 10), 26)

    # chapéu
    pygame.draw.rect(tela, MARROM, (px - 38, py - 18, 76, 12))
    pygame.draw.rect(tela, MARROM, (px - 22, py - 42, 44, 28))

    # olhos felizes
    pygame.draw.arc(tela, PRETO, (px - 17, py, 14, 10), 0, math.pi, 3)
    pygame.draw.arc(tela, PRETO, (px + 3, py, 14, 10), 0, math.pi, 3)

    # sorrisão feliz
    pygame.draw.arc(tela, PRETO, (px - 15, py + 5, 30, 25), math.pi, 2 * math.pi, 4)

    # braços comemorando
    pygame.draw.line(tela, PELE, (px - 25, py + 45), (px - 90, py - 10), 8)
    pygame.draw.line(tela, PELE, (px + 25, py + 45), (px + 90, py - 10), 8)

    # mini Magikarp troféu
    mx = 645
    my = 135
    pygame.draw.ellipse(tela, VERMELHO, (mx, my, 90, 45))
    pygame.draw.polygon(tela, AMARELO, [(mx, my + 22), (mx - 30, my), (mx - 30, my + 45)])
    pygame.draw.circle(tela, BRANCO, (mx + 62, my + 15), 9)
    pygame.draw.circle(tela, PRETO, (mx + 65, my + 15), 4)

    desenhar_texto("MAGIKARP MILIONÁRIO!", fonte_grande, DOURADO, 150, 35)
    desenhar_texto("+20 PONTOS!", fonte, BRANCO, 355, 105)
    desenhar_texto("Aperte ESPAÇO para continuar", fonte_pequena, BRANCO, 285, 500)


def processar_pontos_do_peixe():
    global pontos, mensagem, resultado, fim_de_jogo, venceu, nivel, vitoria_final

    pontos += valor_pendente
    mensagem = f"Você pescou {peixe_pendente}! +{valor_pendente} pontos"

    if pontos >= objetivo:
        pontos = objetivo

        if nivel < 3:
            nivel += 1
            pontos = 0
            resultado = ""
            mensagem = f"Você passou para o NÍVEL {nivel}!"
        else:
            fim_de_jogo = True
            venceu = True
            vitoria_final = True
            mensagem = "Você venceu todos os níveis!"


def aplicar_resultado():
    global mensagem, resultado
    global ataque_tubarao, tempo_ataque
    global cena_magikarp, aguardando_magikarp

    resultado = peixe_pendente

    if peixe_pendente == "Tubarão":
        mensagem = "Algo enorme puxou a linha..."
        resultado = ""
        ataque_tubarao = True
        tempo_ataque = 0

    elif peixe_pendente == "Magikarp":
        resultado = ""
        mensagem = "VOCÊ PESCOU UM MAGIKARP!"
        cena_magikarp = True
        aguardando_magikarp = True

    else:
        processar_pontos_do_peixe()


def reiniciar():
    global pontos, mensagem, resultado, fim_de_jogo, venceu, nivel, vitoria_final
    global pescando, tempo_pescando, peixe_pendente, valor_pendente
    global ataque_tubarao, tempo_ataque, barco_quebrado
    global cena_magikarp, aguardando_magikarp

    pontos = 0
    nivel = 1
    mensagem = "Aperte ESPAÇO para lançar a vara!"
    resultado = ""
    fim_de_jogo = False
    venceu = False
    vitoria_final = False

    pescando = False
    tempo_pescando = 0
    peixe_pendente = None
    valor_pendente = 0

    ataque_tubarao = False
    tempo_ataque = 0
    barco_quebrado = False

    cena_magikarp = False
    aguardando_magikarp = False


while True:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_SPACE and cena_magikarp and aguardando_magikarp:
                cena_magikarp = False
                aguardando_magikarp = False
                processar_pontos_do_peixe()

            elif (
                evento.key == pygame.K_SPACE
                and not fim_de_jogo
                and not pescando
                and not ataque_tubarao
                and not cena_magikarp
            ):
                peixe_pendente, valor_pendente = sortear_pescaria()
                pescando = True
                tempo_pescando = 0
                resultado = ""
                mensagem = "Lançando a vara..."

            if evento.key == pygame.K_r:
                reiniciar()

    if pescando:
        tempo_pescando += 1

        if tempo_pescando >= 90:
            pescando = False
            aplicar_resultado()

    if ataque_tubarao:
        tempo_ataque += 1

        if tempo_ataque == 90:
            barco_quebrado = True
            mensagem = "O TUBARÃO DESTRUIU O BARCO!"

        if tempo_ataque >= 150:
            fim_de_jogo = True
            venceu = False
            mensagem = "Você morreu no ataque do tubarão!"

    if cena_magikarp:
        desenhar_cena_magikarp()
        desenhar_texto("R = Reiniciar", fonte_pequena, BRANCO, 30, 500)

    else:
        desenhar_mar()
        desenhar_tubarao_ataque()
        desenhar_barco()
        desenhar_pescador()
        desenhar_vara()

        desenhar_texto(f"Pontos: {pontos} / {objetivo}", fonte, PRETO, 30, 25)
        desenhar_texto(f"Nível: {nivel}", fonte, PRETO, 30, 60)
        desenhar_texto("ESPAÇO = Pescar", fonte_pequena, PRETO, 30, 105)
        desenhar_texto("R = Reiniciar", fonte_pequena, PRETO, 30, 135)

        if vitoria_final:
            desenhar_texto("VITÓRIA FINAL!", fonte_grande, AMARELO, 250, 130)
        elif venceu:
            desenhar_texto("VITÓRIA!", fonte_grande, BRANCO, 330, 130)
        elif fim_de_jogo:
            desenhar_texto("GAME OVER", fonte_grande, VERMELHO, 290, 130)

        desenhar_texto(mensagem, fonte_pequena, PRETO, 250, 210)

        if resultado != "":
            desenhar_peixe(resultado)

    pygame.display.update()