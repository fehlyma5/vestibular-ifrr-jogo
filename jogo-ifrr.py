import pygame
import sys
import random

# Inicialização do Pygame e do Mixer de Som
pygame.init()
pygame.mixer.init()

LARGURA, ALTURA = 800, 500
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Missão IFRR: Edição Definitiva - IFRR na Comunidade")

# Cores e Paletas de Fases
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE_IF = (0, 128, 64)
LARANJA = (255, 140, 0)
VERMELHO = (200, 0, 0)
VERDE_CLARO = (50, 205, 50)

# Cores de fundo para cada fase (troca a cada 15s)
CORES_FUNDO = [
    (245, 247, 250), # Fase 1: Recepção / Entrada
    (230, 242, 230), # Fase 2: Área Verde / Biologia
    (230, 240, 250), # Fase 3: Laboratório de TADS / Tecnologia
    (255, 243, 230)  # Fase 4: Fase Final / Vestibular
]

NOMES_FASES = [
    "Fase 1: Conhecendo o Campus", 
    "Fase 2: Desafios Acadêmicos", 
    "Fase 3: Imersão Tecnológica", 
    "Fase 4: A Prova Final"
]

FONTE = pygame.font.SysFont("arial", 18)
FONTE_MEDIA = pygame.font.SysFont("arial", 20, bold=True)
FONTE_GRANDE = pygame.font.SysFont("arial", 32, bold=True)
FONTE_TOASTY = pygame.font.SysFont("arial", 40, bold=True)

# Estados do jogo
estado_jogo = "LOGIN"
telefone_usuario = ""
tempo_restante = 60
pontos = 0

# Jogador
jogador_x = 400
jogador_y = 350
jogador_largura = 35
jogador_altura = 45
jogador_vel_y = 0
no_chao = True

# Variáveis do Easter Egg "Oi Di" (Toasty!)
mostrar_toasty = 0 # Contador de frames para exibir o texto na tela

# Matérias e Cursos
materias_vestibular = ["MATEMÁTICA", "REDAÇÃO", "PORTUGUÊS", "FÍSICA", "QUÍMICA", "BIOLOGIA", "HISTÓRIA", "GEOGRAFIA"]
cursos_ifrr = ["TADS", "BIOLOGIA", "GEST. HOSP.", "SANEAMENTO", "TURISMO", "ED. FÍSICA", "MATEMÁTICA"]

obs_x = 800
obs_largura = 45
obs_altura_atual = 40
materia_atual_barra = random.choice(materias_vestibular)

bolas = []
relogio = pygame.time.Clock()
contador_frames = 0
contador_crescimento_barra = 0

# --- CONFIGURAÇÃO DE SONS (Seguro caso os arquivos não existam ainda) ---
def TocarSom(arquivo):
    try:
        som = pygame.mixer.Sound(arquivo)
        som.play()
    except:
        pass # Evita fechar o jogo se o arquivo de áudio ainda não estiver na pasta

def salvar_ranking(telefone, pontos_finais):
    with open("ranking.txt", "a") as f:
        f.write(f"Tel: {telefone} - Pontuação Final: {pontos_finais} pts\n")

# Loop Principal
while True:
    # Definir fase atual com base no tempo decorrido (muda a cada 15 segundos)
    tempo_decorrido = 60 - tempo_restante
    fase_atual = min(tempo_decorrido // 15, 3)
    
    TELA.fill(CORES_FUNDO[fase_atual])
    
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
                    TocarSom("pulo.wav")

    # Controles laterais
    if estado_jogo == "JOGANDO":
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jogador_x -= 5
        if teclas[pygame.K_RIGHT]:
            jogador_x += 5
            
        if jogador_x < 0:
            jogador_x = 0
        elif jogador_x > LARGURA - jogador_largura:
            jogador_x = LARGURA - jogador_largura

    if estado_jogo == "LOGIN":
        txt_titulo = FONTE_GRANDE.render("Missão IFRR: Digite seu WhatsApp", True, VERDE_IF)
        txt_tel = FONTE_GRANDE.render(telefone_usuario + "_", True, PRETO)
        TELA.blit(txt_titulo, (140, 150))
        TELA.blit(txt_tel, (330, 220))
        sub = FONTE.render("Pressione ENTER para comecar.", True, PRETO)
        TELA.blit(sub, (280, 280))

    elif estado_jogo == "JOGANDO":
        contador_frames += 1
        if contador_frames >= 60:
            tempo_restante -= 1
            contador_frames = 0
            if tempo_restante <= 0:
                estado_jogo = "VITORIA"
                salvar_ranking(telefone_usuario, pontos)

        # Crescimento da barra a cada 3s
        contador_crescimento_barra += 1
        if contador_crescimento_barra >= 180:
            obs_altura_atual += 10
            if obs_altura_atual > 130:
                obs_altura_atual = 130
            contador_crescimento_barra = 0

        # Gravidade
        jogador_vel_y += 0.8
        jogador_y += jogador_vel_y
        if jogador_y >= 350:
            jogador_y = 350
            no_chao = True

        # Movimento do Obstáculo
        obs_x -= 6
        if obs_x < -50:
            obs_x = 800
            obs_altura_atual = 40
            materia_atual_barra = random.choice(materias_vestibular)

        # Gerar bolas
        if random.randint(1, 35) == 1:
            tipo_bola = random.choice(["vermelha", "verde", "verde"])
            curso_texto = random.choice(cursos_ifrr) if tipo_bola == "verde" else ""
            bolas.append([random.randint(50, 750), -20, tipo_bola, curso_texto, 18])

        # Colisões das bolas
        for b in bolas[:]:
            b[1] += 4
            cor_bola = VERMELHO if b[2] == "vermelha" else VERDE_CLARO
            pygame.draw.circle(TELA, cor_bola, (b[0], b[1]), b[4])
            
            if b[2] == "verde" and b[3]:
                txt_c = FONTE.render(b[3], True, PRETO)
                TELA.blit(txt_c, (b[0] - 25, b[1] - 30))

            if (jogador_x < b[0] + b[4] and jogador_x + jogador_largura > b[0] - b[4] and
                jogador_y < b[1] + b[4] and jogador_y + jogador_altura > b[1] - b[4]):
                
                if b[2] == "vermelha":
                    pontos -= 5
                    TocarSom("dano.wav")
                else:
                    pontos += 15
                    TocarSom("ponto.wav")
                    
                    # --- CONDIÇÃO DO "OI DI" (TOASTY!) ---
                    # Se o jogador estiver pulando (no_chao == False) e pegar a bolinha verde ao mesmo tempo!
                    if not no_chao:
                        mostrar_toasty = 45 # Mantém o aviso na tela por 45 frames
                        TocarSom("toasty_di.mp3")

                bolas.remove(b)
            elif b[1] > 400:
                bolas.remove(b)

        # Colisão com a barra vermelha da matéria
        obs_y_pos = 395 - obs_altura_atual
        if (jogador_x < obs_x + obs_largura and
            jogador_x + jogador_largura > obs_x and
            jogador_y + jogador_altura > obs_y_pos):
            pontos -= 3
            TocarSom("dano.wav")

        # Elementos Visuais
        pygame.draw.line(TELA, PRETO, (0, 395), (800, 395), 4)
        pygame.draw.rect(TELA, VERDE_IF, (jogador_x, jogador_y, jogador_largura, jogador_altura))
        pygame.draw.rect(TELA, VERMELHO, (obs_x, obs_y_pos, obs_largura, obs_altura_atual))
        
        txt_materia = FONTE.render(materia_atual_barra[:4], True, BRANCO)
        TELA.blit(txt_materia, (obs_x + 2, obs_y_pos + 5))

        # Interface superior (Mostra a Fase atual e o tempo)
        txt_info = FONTE_MEDIA.render(f"Fase: {NOMES_FASES[fase_atual]} | Tempo: {tempo_restante}s | Pts: {pontos}", True, PRETO)
        TELA.blit(txt_info, (20, 20))

        # --- DESENHAR O EASTER EGG "OI DI!" NA TELA (ESTILO TOASTY) ---
        if mostrar_toasty > 0:
            txt_toasty = FONTE_TOASTY.render("🔥 CBV! 🎓", True, (255, 69, 0))
            # Desenha no canto inferior direito, igualzinho ao Mortal Kombat
            TELA.blit(txt_toasty, (580, 320))
            mostrar_toasty -= 1

    elif estado_jogo == "VITORIA":
        msg = FONTE_GRANDE.render("PARABÉNS! Você venceu o IFRR na Comunidade!", True, VERDE_IF)
        TELA.blit(msg, (80, 180))
        pts_final = FONTE_MEDIA.render(f"Pontuação Total: {pontos} pontos salva no Ranking!", True, PRETO)
        TELA.blit(pts_final, (200, 240))

    pygame.display.flip()
    relogio.tick(60)