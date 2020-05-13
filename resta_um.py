import time

'''
     N
     ^
     |
O <--x--> L
     |
     v
     S
    
    DIRECOES = ['O', 'L', 'N', 'S']
'''
DIRECOES = ['O', 'L', 'N', 'S'] # ------

DELTAS_MOVER = {'N': -2, 'S': 2, 'O': -2, 'L': 2}

DELTAS_REMOVER = {'N': -1, 'S': 1, 'O': -1, 'L': 1}

COORDS_VALIDAS = (
                    (0, 2), (0, 3), (0, 4),
                    (1, 2), (1, 3), (1, 4),
    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
    (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
    (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6),
                    (5, 2), (5, 3), (5, 4),
                    (6, 2), (6, 3), (6, 4)
    )

class Movimento:
    def __init__(self, posicao: tuple, direcao: str):
        self.posicao = posicao
        self.direcao = direcao
    
    def __repr__(self):
        return f"[{self.posicao}, {self.direcao}]"

    def __eq__(self, other):
        pos_0 = self.posicao[0] == other.posicao[0]
        pos_1 = self.posicao[1] == other.posicao[1]
        mesma_dir = self.direcao == other.direcao
        return all([pos_0, pos_1, mesma_dir])

    @property
    def nova_posicao(self):
        if self.direcao == 'N' or self.direcao == 'S':
            pos = self.posicao[0]+DELTAS_MOVER[self.direcao], self.posicao[1]
        else:
            pos = self.posicao[0], self.posicao[1]+DELTAS_MOVER[self.direcao]
        return self._fix(pos)
    
    @property
    def saltada(self):
        if self.direcao == 'N' or self.direcao == 'S':
            pos = self.posicao[0]+DELTAS_REMOVER[self.direcao], self.posicao[1]
        else:
            pos = self.posicao[0], self.posicao[1]+DELTAS_REMOVER[self.direcao]
        return self._fix(pos)
    
    def _fix(self, pos):
        if pos[0] <= -1: pos = (0, pos[1])
        if pos[1] <= -1: pos = (pos[0], 0)
        if pos[0] >= 7: pos = (6, pos[1])
        if pos[1] >= 7: pos = (pos[0], 6)
        return pos

class Tabuleiro:
    def __init__(self, pos_inicial = (3, 3)):
        self.tabuleiro = [
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2]
        ]
        self.pecas_restantes = 32
        self.pos_inicial = pos_inicial
        self.movimentos = []
        self.remover(self.pos_inicial)

    def reset(self):
        self.__init__()

    def __repr__(self):
        repr_tabuleiro = '   0 1 2 3 4 5 6\n\n'
        for n_linha, linha in enumerate(self.tabuleiro):
            repr_tabuleiro += f"{n_linha}  {' '.join([str(pos) for pos in linha]).replace('2', ' ')}\n"
        return repr_tabuleiro

    def get(self, posicao: tuple, dir=None):
        return self.tabuleiro[posicao[0]][posicao[1]]

    def set(self, posicao: tuple):
        self.tabuleiro[posicao[0]][posicao[1]] = 1

    def remover(self, posicao: tuple):
        self.tabuleiro[posicao[0]][posicao[1]] = 0

    def _valido(self, movimento):
        valido = True
        if not movimento:
            valido = False
        elif movimento.posicao == movimento.saltada:
            valido = False
        elif movimento.posicao == movimento.nova_posicao:
            valido = False
        elif self.get(movimento.posicao) in (0, 2):
            valido = False
        elif self.get(movimento.nova_posicao) in (1, 2):
            valido = False
        elif self.get(movimento.saltada) in (0, 2):
            valido = False

        return valido

    def mover(self, movimento):
        valido = self._valido(movimento)
        if valido:
            pos_nova = movimento.nova_posicao
            pos_anterior = movimento.posicao
            peca_saltada = movimento.saltada

            self.set(pos_nova)
            self.remover(pos_anterior)
            self.remover(peca_saltada)
            self.pecas_restantes -= 1
            
            self.movimentos.append(movimento)
            return True
        return False

    def get_movimentos_validos(self):
        movimentos_validos = []
        for linha, coluna in COORDS_VALIDAS:
            if self.get((linha, coluna)) == 2:
                continue
            for direcao in DIRECOES:
                movimento = Movimento((linha, coluna), direcao)
                if self._valido(movimento):
                    movimentos_validos.append(movimento)
        return movimentos_validos

    def solucionavel(self):
        return len(self.get_movimentos_validos()) >= 1

    def esta_solucionado(self):
        return self.pecas_restantes == 1 and self.get(self.pos_inicial) == 1

    def desfazer_movimento(self, mov = None):
        movimento = mov or self.movimentos.pop()
        if mov:
            self.movimentos.pop()
        pos_nova = movimento.nova_posicao
        pos_anterior = movimento.posicao
        peca_saltada = movimento.saltada

        self.remover(pos_nova)
        self.set(pos_anterior)
        self.set(peca_saltada)
        self.pecas_restantes += 1


def solucionar(jogo, movimentos_realizados):
    if movimentos_realizados == 31:
        if jogo.esta_solucionado():
            return True

    for linha, coluna in COORDS_VALIDAS:
        for direcao in DIRECOES:
            movimento = Movimento((linha, coluna), direcao)
            if jogo.mover(movimento):

                if solucionar(jogo, movimentos_realizados+1):
                    return True
                    
                jogo.desfazer_movimento()

    return False


jogo = Tabuleiro()

s_time = time.time()
try:
    solucao = False
    root = solucionar(jogo, 0)
    solucao = jogo.movimentos
finally:
    e_time = time.time()
    print(f"{e_time - s_time} secs")
    print(jogo.pecas_restantes)
    if solucao:
        # solucao.reverse()
        for mov in solucao:
            mov = str(mov).replace('N', 'cima')
            mov = str(mov).replace('O', 'esq')
            mov = str(mov).replace('L', 'dir')
            mov = str(mov).replace('S', 'baixo')
            print(str(mov))
