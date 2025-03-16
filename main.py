import pgzrun
import pygame
from pygame import Rect, image, transform

# Dimensões da tela
WIDTH = 800
HEIGHT = 600

# Criando um inimigo inicial fora da tela (para vir da direita para a esquerda)
inimigo = Actor("chica", (WIDTH + 100,HEIGHT-160))
velocidade_inimigo = 7  # Velocidade do inimigo
vidas = 7
colidiu_com_inimigo = False

# Carrega as imagens
fundo_original = image.load("images/background.png")
fundo = transform.scale(fundo_original, (WIDTH, HEIGHT))
sky_original = image.load("images/sky.jpg")
sky = transform.scale(sky_original, (WIDTH, HEIGHT))

#carregar musica 
pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(2)

som_colisao = pygame.mixer.Sound("sounds/berro.mp3") # Carregue o som

# Definição dos botões
botao_jogar = Rect((WIDTH / 4 - 100, 300), (200, 50))
botao_sair = Rect((WIDTH / 3 + 200, 300), (200, 50))
icone_som = Actor("music", (WIDTH - 50, HEIGHT - 130))
espaco = True

gato = Actor("kat1", (120, HEIGHT - 100))
gato.imagens = ["kat1", "kat2", "kat3", "kat4","kat5","kat6","kat7","kat8","kat9"]  # Lista de imagens do sprite
gato.indice_animacao = 0  # Índice inicial

ground = Actor("ground", (WIDTH-320, HEIGHT - 121))

velocidade_y = 0
gravidade = 0.4
no_chao = False
tempo_animacao = 0


som_mutado = False  # Começa com som ligado
estado_jogo = "start"  # Pode ser "start", "game" ou "end"

def update():
    global estado_jogo, vidas, colidiu_com_inimigo, velocidade_y, no_chao, inimigo
    if estado_jogo == "game":
        ground.left -= 2 #velocidade
        if ground.left < -180:
            ground.x = WIDTH - 320 

        # Aplica gravidade
        velocidade_y += gravidade
        gato.y += velocidade_y

        # Impede que o personagem caia do chão
        if gato.y >= 500:
            gato.y = 500
            velocidade_y = 0
            no_chao = True

        global tempo_animacao
        tempo_animacao += 1

        global inimigo
        colidiu_com_inimigo = False
        som_colisao
        
        # Move o inimigo para a esquerda
        inimigo.x -= velocidade_inimigo
        
        # Quando o inimigo sair da tela, cria um novo
        if inimigo.x < 0:
            colidiu_com_inimigo = True
            inimigo = Actor("chica", ((WIDTH + 100,HEIGHT-160)))
            

        # Troca de sprites a cada 10 frames
        if tempo_animacao % 10 == 0:
            gato.indice_animacao = (gato.indice_animacao + 1) % len(gato.imagens)
            gato.image = gato.imagens[gato.indice_animacao]  # Muda a imagem


        if gato.colliderect(inimigo) and not colidiu_com_inimigo and inimigo.image == "chica":
            colidiu_com_inimigo = True  # Marca que esse inimigo já causou dano
            vidas = vidas - 1         
            inimigo.image = "chica2"
            som_colisao.play() 

        elif not gato.colliderect(inimigo):
            colidiu_com_inimigo = False 
            # Verifica se o jogo deve terminar

        if vidas <= 0:
             estado_jogo = "end"

def draw():
    screen.clear()
      
    if estado_jogo == "start":
        screen.blit(fundo, (0, 0)) # Desenha a imagem de fundo
        screen.draw.text("Bem vindo!", center=(WIDTH // 2, HEIGHT // 2 - 180), fontsize=100, color="lightblue")
        screen.draw.filled_rect(botao_jogar, "darkblue")
        screen.draw.filled_rect(botao_sair, "lightblue")
        screen.draw.text("1 - Jogar", center=botao_jogar.center, fontsize=30, color="white")
        screen.draw.text("2 - Sair", center=botao_sair.center, fontsize=30, color="black")
        icone_som.draw()

    elif estado_jogo == "game":
        screen.blit(sky,(0,0))
        
        gato.draw()  # Apenas o gato e o fundo aparecem
        ground.draw()
        inimigo.draw()
        screen.draw.text(f"Vidas: {vidas}", (WIDTH - 100, HEIGHT - 80), fontsize=30, color="white") # type: ignore
        if espaco:
            screen.draw.text("Pressione espaço para pular", center=(WIDTH // 2, HEIGHT // 2), fontsize=70, color="red")
    
    else:
        screen.draw.text("GAME OVER!", center=(WIDTH // 2, HEIGHT // 2), fontsize=80, color="red")
        screen.draw.text("Pressione Enter para reiniciar", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")

def on_key_down(key):
    global velocidade_y, no_chao, estado_jogo, vidas, inimigo, espaco
    if key == keys.SPACE and no_chao:  # Permite pular apenas se estiver no chão
        velocidade_y = -20        
        no_chao = False
        espaco = False

    elif key == keys.RETURN:
        estado_jogo = "start"
        vidas = 7  # Resetar vidas
        inimigo = Actor("chica", (WIDTH + 100, HEIGHT - 160))  # Reposicionar inimigo


def on_mouse_down(pos):
    global som_mutado, estado_jogo
     
    if estado_jogo == "start":
        if botao_jogar.collidepoint(pos):
            estado_jogo = "game"  # Muda o estado para "game"
        elif botao_sair.collidepoint(pos):
            exit()

        elif icone_som.collidepoint(pos):
            som_mutado = not som_mutado
           
            if som_mutado:
                pygame.mixer.music.pause()  # Pausa a música
                # pygame.mixer.music.set_volume(0)
                icone_som.image = "music1"
            else:
                pygame.mixer.music.unpause()  # Retoma a música
                icone_som.image = "music"


pgzrun.go()
