import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Configuración de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong Game')

# Variables globales
player1_score = 0
player2_score = 0

# Función para mostrar el menú principal
def show_menu():
    while True:
        screen.fill(WHITE)
        # Dibujar texto del menú
        font = pygame.font.Font(None, 36)
        title_text = font.render('Menú Principal', True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Opciones del menú
        options = ['Jugar', 'Configuración', 'Instrucciones', 'Créditos', 'Salir']
        option_rects = []
        for i, option in enumerate(options):
            text = font.render(f'{i + 1}. {option}', True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 50))
            screen.blit(text, text_rect)
            option_rects.append(text_rect)

        pygame.display.flip()

        # Eventos del teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 0
                elif event.key == pygame.K_2:
                    return 1
                elif event.key == pygame.K_3:
                    return 2
                elif event.key == pygame.K_4:
                    return 3
                elif event.key == pygame.K_5:
                    return 4

# Función principal para el juego
def main():
    global player1_score, player2_score
    while True:
        choice = show_menu()

        if choice == 0:  # Jugar
            player1_score, player2_score = run_game()
        elif choice == 1:  # Configuración
            show_settings()
        elif choice == 2:  # Instrucciones
            show_instructions()
        elif choice == 3:  # Créditos
            show_credits()
        elif choice == 4:  # Salir
            pygame.quit()
            sys.exit()

# Función para correr el juego de Pong
def run_game():
    # Variables de juego
    ball_speed = 5
    player_speed = 5
    ball_dir = [1, 1]  # Dirección inicial de la pelota

    # Posiciones iniciales
    ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    player1_pos = [50, SCREEN_HEIGHT // 2]
    player2_pos = [SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2]

    # Puntuaciones
    player1_score = 0
    player2_score = 0

    clock = pygame.time.Clock()

    while True:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento de jugadores
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if player1_pos[1] > 0:
                player1_pos[1] -= player_speed
        if keys[pygame.K_s]:
            if player1_pos[1] < SCREEN_HEIGHT - 100:
                player1_pos[1] += player_speed
        if keys[pygame.K_UP]:
            if player2_pos[1] > 0:
                player2_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            if player2_pos[1] < SCREEN_HEIGHT - 100:
                player2_pos[1] += player_speed

        # Movimiento de la pelota
        ball_pos[0] += ball_dir[0] * ball_speed
        ball_pos[1] += ball_dir[1] * ball_speed

        # Colisiones con las paredes
        if ball_pos[1] <= 0 or ball_pos[1] >= SCREEN_HEIGHT - 20:
            ball_dir[1] = -ball_dir[1]

        # Colisiones con las paletas
        if ball_pos[0] <= player1_pos[0] + 20 and player1_pos[1] <= ball_pos[1] <= player1_pos[1] + 100:
            ball_dir[0] = 1
        elif ball_pos[0] >= player2_pos[0] - 20 and player2_pos[1] <= ball_pos[1] <= player2_pos[1] + 100:
            ball_dir[0] = -1

        # Puntos
        if ball_pos[0] <= 0:
            player2_score += 1
            ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
            ball_dir = [1, 1]
        elif ball_pos[0] >= SCREEN_WIDTH:
            player1_score += 1
            ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
            ball_dir = [-1, 1]

        # Verificar final del juego
        if player1_score == 10:
            show_winner("GANADOR JUGADOR 1")
            return player1_score, player2_score
        elif player2_score == 10:
            show_winner("GANADOR JUGADOR 2")
            return player1_score, player2_score

        # Dibujar elementos en la pantalla
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, pygame.Rect(player1_pos[0], player1_pos[1], 20, 100))
        pygame.draw.rect(screen, BLACK, pygame.Rect(player2_pos[0], player2_pos[1], 20, 100))
        pygame.draw.ellipse(screen, BLACK, pygame.Rect(ball_pos[0], ball_pos[1], 20, 20))
        font = pygame.font.Font(None, 36)
        player1_text = font.render(str(player1_score), True, BLACK)
        player2_text = font.render(str(player2_score), True, BLACK)
        screen.blit(player1_text, (SCREEN_WIDTH // 4, 50))
        screen.blit(player2_text, (3 * SCREEN_WIDTH // 4, 50))

        pygame.display.flip()
        clock.tick(FPS)

# Función para mostrar el ganador
def show_winner(winner_text):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    text = font.render(winner_text, True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Espera 3 segundos antes de volver al menú

# Función para mostrar la pantalla de configuración
def show_settings():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    title_text = font.render('Configuración', True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    # Opciones de configuración (ejemplo: velocidad de la pelota)
    settings_text = font.render('Configuración: Velocidad, Tamaño de Paletas, Dificultad.', True, BLACK)
    screen.blit(settings_text, (SCREEN_WIDTH // 2 - settings_text.get_width() // 2, 200))

    pygame.display.flip()
    pygame.time.wait(3000)  # Espera 3 segundos para que el jugador vea la configuración

# Función para mostrar la pantalla de instrucciones
def show_instructions():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    title_text = font.render('Instrucciones', True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    # Texto de instrucciones
    instructions_text = [
        'Bienvenido a Pong!',
        'Jugador 1 (izquierda): Utiliza W y S para mover la paleta hacia arriba y abajo.',
        'Jugador 2 (derecha): Utiliza las teclas de flecha arriba y abajo para mover la paleta.',
        'El objetivo es evitar que la pelota pase por tu lado de la pantalla.',
        'El primer jugador en alcanzar 10 puntos gana el juego.'
    ]

    y_offset = 200
    for line in instructions_text:
        line_text = font.render(line, True, BLACK)
        screen.blit(line_text, (SCREEN_WIDTH // 2 - line_text.get_width() // 2, y_offset))
        y_offset += 40

    pygame.display.flip()
    pygame.time.wait(5000)  # Espera 5 segundos para que el jugador vea las instrucciones

# Función para mostrar la pantalla de créditos
def show_credits():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    title_text = font.render('Créditos', True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    # Información de créditos
    credits_text = [
        'Desarrollado por: Luca Fattorini',
        'Github: https://github.com/LucaFattorini',
        'Versión: 1.0',
        '¡Gracias por jugar!'
    ]

    y_offset = 200
    for line in credits_text:
        line_text = font.render(line, True, BLACK)
        screen.blit(line_text, (SCREEN_WIDTH // 2 - line_text.get_width() // 2, y_offset))
        y_offset += 40

    pygame.display.flip()
    pygame.time.wait(3000)  # Espera 3 segundos para que el jugador vea los créditos

# Ejecutar el juego
if __name__ == '__main__':
    main()
