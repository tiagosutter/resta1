from threading import Thread
import sys
import tkinter as tk
import time
import pygame
import resta_um

BRANCO = (255,255,255)
PRETO = (0,0,0)

TAMANHO_CELULA = 50

LARGURA = 7*TAMANHO_CELULA
ALTURA = 7*TAMANHO_CELULA

class Visualizacao:

    def __init__(self, jogo, recursivo):
        self.jogo = jogo
        self.recursivo = recursivo
        self.caminho = ''
        self.delay = 1
        # Pygame setup
        pygame.init()
        self.surface = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Visualização Resta 1")
        self.surface.fill(BRANCO)

        self.desenhar_celulas()
        self.desenhar_grid()

        # Tkinter setup
        self.root = tk.Tk()
        self.text_box_caminho = tk.Text(self.root, height=32, width=30)
        self.text_box_caminho.pack()
        self.root.geometry('+450+100')
    
    def start(self):
        self.ler_tabuleiro(self.jogo.tabuleiro)
        solver = resta_um.SolucionadorResta1(self.jogo, callback_visualizacao=self.callback_exibir)
        solverThread = Thread(target=solver.solucionar, kwargs={'recursivo': self.recursivo}, name="Principal", daemon=True)
        solverThread.start()
        self.root.after(100, self.atualizar_tk_e_pygame)
        self.root.mainloop()

    def atualizar_tk_e_pygame(self):
        texto = self.caminho
        self.text_box_caminho.delete('1.0', tk.END)
        self.text_box_caminho.insert(tk.END, texto)
        self.root.after(100, self.atualizar_tk_e_pygame)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                self.root.quit()
                sys.exit()
        pygame.display.update()

    def desenhar_celulas(self):
        for i in range(7):
            for j in range(7):
                COR = BRANCO if (i, j) in resta_um.COORDS_VALIDAS else PRETO
                retangulo = pygame.Rect(i*TAMANHO_CELULA, j*TAMANHO_CELULA,
                                        TAMANHO_CELULA, TAMANHO_CELULA)
                pygame.draw.rect(self.surface, COR, retangulo)

    def desenhar_grid(self):
        for i in range(7):
            pos = i*TAMANHO_CELULA
            pygame.draw.line(self.surface, PRETO, (0, pos), (LARGURA, pos), 2)
            pygame.draw.line(self.surface, PRETO, (pos, 0), (pos, ALTURA), 2)

    def ler_tabuleiro(self, tabuleiro):
        for linha in range(7):
            for coluna in range(7):
                x = coluna*TAMANHO_CELULA+TAMANHO_CELULA//2
                y = linha*TAMANHO_CELULA+TAMANHO_CELULA//2
                if tabuleiro[linha][coluna] == 1:
                    pygame.draw.circle(self.surface, PRETO, (x,y), 12)
                elif tabuleiro[linha][coluna] == 0:
                    pygame.draw.circle(self.surface, BRANCO, (x,y), 12)
    
    def callback_exibir(self, solver):
        time.sleep(self.delay)
        self.ler_tabuleiro(solver.jogo.tabuleiro)
        self.caminho = f'Total de movimentos: {solver.total_de_movimentos}\n'
        for i, mov in enumerate(solver.jogo.movimentos):
            self.caminho += f'{i+1:02}. {mov}\n'

if __name__ == "__main__":    
    # Inicialização do Pygame
    visualizacao = Visualizacao(resta_um.Tabuleiro(), False)
    visualizacao.start()
