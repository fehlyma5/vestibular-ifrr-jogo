import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()
LARGURA, ALTURA = 800, 500
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Missão IFRR: Desafio Avançado do Vestibular")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE_IF = (0, 128, 64)
LARANJA = (255, 140, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 102, 204)
VERDE_CLARO = (50, 205, 50)

FONTE = pygame.font.SysFont("arial", 20)
FONTE_GRANDE = pygame.font.SysFont("arial", 32, bold=True)

# Estados do jogo: LOGIN, JOGANDO, VITORIA, DERROTA
estado_jogo = "LOGIN"
telefone_usuario = ""
tempo_restante = 60
pontos = 0

# Jogador
jogador_x = 100
jogador_y = 350
jogador_largura = 35
jogador_altura = 45
jogador_vel_y = 0
no_chao = True

# Obstáculo (Barra que cresce)
obs_x = 800
obs_largura = 30
obs_altura_inicial = 40
obs_altura_atual = 40

# Lista de Cursos do IFRR Campus Boa Vista para as bolas verdes
cursos_ifrr = ["TADS", "BIOLOGIA", "GEST. HOSP.", "SANEAMENTO", "TURISMO", "ED. FÍSICA", "MATEMÁTICA"]

# Bolas caindo (Vermelhas e Verdes)
bolas = []
# Estrutura de cada bola: [x, y, tipo ('vermelha' ou 'verde'), texto_curso, raio]

relogio = pygame.time.Clock()
contador_frames = 0
contador_crescimento_barra = 0

def salvar_ranking(telefone, pontos_finais):
    with open("ranking.txt", "a") as f:
        f.write(f"Tel: {telefone} - Pontuação: {pontos_finais} pts\n")

# Loop Principal
while True:
    TELA.fill(BRANCO)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if estado_jogo == "LOGIN":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and len(telefone_usuario) >= 8:
                    estado_jogo = "JOGANDO"
                    tempo_restante = 60
                    pontos = 0
                elif evento.key == pygame.K_BACKSPACE:
                    telefone_usuario = telefone_usuario[:-1]
                else:
                    if evento.unicode.isdigit():
                        telefone_usuario += evento.unicode
                        
        elif estado_jogo == "JOGANDO":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and no_chao:
                    jogador_vel_y = -15
                    no_chao = False

    if estado_jogo == "LOGIN":
        txt_titulo = FONTE_GRANDE.render("Missão IFRR: Cadastre seu Telefone (WhatsApp)", True, VERDE_IF)
        txt_tel = FONTE_GRANDE.render(telefone_usuario + "_", True, PRETO)
        TELA.blit(txt_titulo, (80, 150))
        TELA.blit(txt_tel, (330, 220))
        sub = FONTE.render("Pressione ENTER para iniciar o desafio.", True, PRETO)
        TELA.blit(sub, (260, 280))

    elif estado_jogo == "JOGANDO":
        # Contagem regressiva do tempo (60 frames = 1 segundo)
        contador_frames += 1
        if contador_frames >= 60:
            tempo_restante -= 1
            contador_frames = 0
            if tempo_restante <= 0:
                estado_jogo = "VITORIA" # Sobreviveu aos 60s
                salvar_ranking(telefone_usuario, pontos)

        # 1. Aumentar o tamanho da barra de obstáculo a cada 3 segundos
        contador_crescimento_barra += 1
        if contador_crescimento_barra >= 180: # 180 frames = 3 segundos
            obs_altura_atual += 10
            if obs_altura_atual > 120: # Limite máximo de altura para não ficar impossível
                obs_altura_atual = 120
            contador_crescimento_barra = 0

        # Física do Jogador (Gravidade)
        jogador_vel_y += 0.8
        jogador_y += jogador_vel_y
        if jogador_y >= 350:
            jogador_y = 350
            no_chao = True

        # Movimento do Obstáculo principal
        obs_x -= 6
        if obs_x < -30:
            obs_x = 800

        # Gerar novas bolas caindo aleatoriamente
        if random.randint(1, 40) == 1:
            tipo_bola = random.choice(["vermelha", "verde", "verde"]) # Mais chances de verde para pontuar
            curso_texto = random.choice(cursos_ifrr) if tipo_bola == "verde" else ""
            bolas.append([random.randint(100, 750), -20, tipo_bola, curso_texto, 18])

        # Atualizar posições e colisões das bolas
        for b in bolas[:]:
            b[1] += 4 # Velocidade de queda da bola
            
            # Desenhar bola na tela
            cor_bola = VERMELHO if b[2] == "vermelha" else VERDE_CLARO
            pygame.draw.circle(TELA, cor_bola, (b[0], b[1]), b[4])
            
            if b[2] == "verde" and b[3]:
                txt_c = FONTE.render(b[3], True, PRETO)
                TELA.blit(txt_c, (b[0] - 25, b[1] - 30))

            # Colisão da bola com o Jogador
            # Caixa de colisão simples do jogador
            if (jogador_x < b[0] + b[4] and jogador_x + jogador_largura > b[0] - b[4] and
                jogador_y < b[1] + b[4] and jogador_y + jogador_altura > b[1] - b[4]):
                
                if b[2] == "vermelha":
                    pontos -= 5 # Perde pontos se pegar a vermelha
                else:
                    pontos += 10 # Ganha pontos se tocar na bola verde do curso
                bolas.remove(b)
            elif b[1] > 400: # Remove se cair no chão
                bolas.remove(b)

        # Colisão com o obstáculo principal (barra que cresce)
        obs_y_pos = 395 - obs_altura_atual
        if (jogador_x < obs_x + obs_largura and
            jogador_x + jogador_largura > obs_x and
            jogador_y + jogador_altura > obs_y_pos):
            pontos -= 2 # Penalidade leve ao tocar na barra

        # Desenhar Elementos na Tela
        # Chão
        pygame.draw.line(TELA, PRETO, (0, 395), (800, 395), 4)
        
        # Jogador
        pygame.draw.rect(TELA, VERDE_IF, (jogador_x, jogador_y, jogador_largura, jogador_altura))
        
        # Obstáculo barra vertical
        pygame.draw.rect(TELA, VERMELHO, (obs_x, obs_y_pos, obs_largura, obs_altura_atual))

        # Placar e Infos na tela
        txt_info = FONTE.render(f"Tempo: {tempo_restante}s  |  Pontos: {pontos}  |  Altura do Obstáculo: {obs_altura_atual}px", True, PRETO)
        TELA.blit(txt_info, (30, 20))

    elif estado_jogo == "VITORIA":
        msg = FONTE_GRANDE.render("PARABÉNS! Você sobreviveu ao Vestibular!", True, VERDE_IF)
        TELA.blit(msg, (150, 180))
        pts_final = FONTE.render(f"Sua pontuação final foi: {pontos} pontos", True, PRETO)
        TELA.blit(pts_final, (260, 240))
        aviso = FONTE.render("Dados salvos no ranking da escola! Pressione Fechar.", True, PRETO)
        TELA.blit(aviso, (200, 300))

    pygame.display.flip()
    relogio.tick(60)