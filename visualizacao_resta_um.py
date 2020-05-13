from threading import Thread
import sys
import tkinter as tk
import time
import pygame
import resta_um

# Configurações

# Tempo entre movimentos
DELAY = 0.5
# Usar ou não implementação recursiva de backtracking
RECURSIVO = True

# Variáveis globais
BRANCO = (255,255,255)
PRETO = (0,0,0)

TAMANHO_CELULA = 50

LARGURA = 7*TAMANHO_CELULA
ALTURA = 7*TAMANHO_CELULA

# Inicialização do Pygame
pygame.init()
surface = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Visualização Resta 1")
surface.fill(BRANCO)

class Visualizacao:
    caminho = ''
    def __init__(self):
        self.root = tk.Tk()
        self.text_box_caminho = tk.Text(self.root, height=32, width=30)
        self.text_box_caminho.pack()
        self.root.geometry('+450+100')
        self.root.after(100, self.atualizar_tk_e_pygame)
        self.root.mainloop()

    def atualizar_tk_e_pygame(self):
        texto = Visualizacao.caminho
        self.text_box_caminho.delete('1.0', tk.END)
        self.text_box_caminho.insert(tk.END, texto)
        self.root.after(100, self.atualizar_tk_e_pygame)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                self.root.quit()
                sys.exit()
        pygame.display.update()

def desenhar_celulas(surface):
    for i in range(7):
        for j in range(7):
            COR = BRANCO if (i, j) in resta_um.COORDS_VALIDAS else PRETO
            retangulo = pygame.Rect(i*TAMANHO_CELULA, j*TAMANHO_CELULA,
                                    TAMANHO_CELULA, TAMANHO_CELULA)
            pygame.draw.rect(surface, COR, retangulo)

def desenhar_grid(surface):
    for i in range(7):
        pos = i*TAMANHO_CELULA
        pygame.draw.line(surface, PRETO, (0, pos), (LARGURA, pos), 2)
        pygame.draw.line(surface, PRETO, (pos, 0), (pos, ALTURA), 2)

def ler_tabuleiro(tabuleiro):
    for linha in range(7):
        for coluna in range(7):
            x = coluna*TAMANHO_CELULA+TAMANHO_CELULA//2
            y = linha*TAMANHO_CELULA+TAMANHO_CELULA//2
            if tabuleiro[linha][coluna] == 1:
                pygame.draw.circle(surface, PRETO, (x,y), 12)
            elif tabuleiro[linha][coluna] == 0:
                pygame.draw.circle(surface, BRANCO, (x,y), 12)

def callback_exibir(solver):
    time.sleep(DELAY)
    ler_tabuleiro(solver.jogo.tabuleiro)
    Visualizacao.caminho = ''
    for i, mov in enumerate(solver.jogo.movimentos):
        Visualizacao.caminho += f'{i+1:02}. {mov}\n'
   
desenhar_celulas(surface)
desenhar_grid(surface)

jogo = resta_um.Tabuleiro()

solver = resta_um.SolucionadorResta1(jogo, callback_visualizacao=callback_exibir)

solverThread = Thread(target=solver.solucionar, kwargs={'recursivo': RECURSIVO}, name="Principal", daemon=True)
solverThread.start()

visualizacao = Visualizacao()
