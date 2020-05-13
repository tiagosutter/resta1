import time

"""
     N
     ^
     |
O <--x--> L
     |
     v
     S
    
    DIRECOES = ['O', 'L', 'N', 'S']
"""
DIRECOES = ['O', 'L', 'N', 'S']

# Distâncias a qual as peças serão movidas
DELTAS_MOVER = {'N': -2, 'S': 2, 'O': -2, 'L': 2}

# Distância da peça adjacente (será saltada)
DELTAS_REMOVER = {'N': -1, 'S': 1, 'O': -1, 'L': 1}

# Lista de coordenadas válidas para o tabuleiro
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
        """Inicializa o objeto Movimento.

        Arguments:
            posicao {tuple} -- Posição da peça que será movida.
            direcao {str} -- Direção em que a peça será movida.
        """
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
        """
        Retorna a nova posição da peça.

        Caso a coordenada da nova posição da peça seja inválida esta prorpriedade 
        retornará a própria posição da peça a ser movida.

        Returns:
            tuple -- (linha, coluna) para onde a peça será movida.
        """
        if self.direcao == 'N' or self.direcao == 'S':
            pos = self.posicao[0]+DELTAS_MOVER[self.direcao], self.posicao[1]
        else:
            pos = self.posicao[0], self.posicao[1]+DELTAS_MOVER[self.direcao]
        return self._fix(pos)
    
    @property
    def saltada(self):
        """
        Retorna a posição da peça que será saltada após o movimento ser realizado.

        Caso a coordenada da peça saltada seja inválida esta prorpriedade retornará
        a posição da própria peça a ser movida.

        Returns:
            tuple -- (linha, coluna) da peça saltada.
        """
        if self.direcao == 'N' or self.direcao == 'S':
            pos = self.posicao[0]+DELTAS_REMOVER[self.direcao], self.posicao[1]
        else:
            pos = self.posicao[0], self.posicao[1]+DELTAS_REMOVER[self.direcao]
        return self._fix(pos)
    
    def _fix(self, pos):
        """Faz com que posições fora dos limites sejam colocadas como a mesma
        que a posição da peça.

        Arguments:
            pos {tuple} -- Posição a ser verificada

        Returns:
            tuple -- Nova posição para casos fora dos limites, posição recebida 
            para casos regulares
        """
        if pos not in COORDS_VALIDAS:
            return self.posicao
        return pos

class Tabuleiro:
    """
    Classe que contém tabuleiro e implementa as regras do jogo.
    """
    def __init__(self, pos_inicial = (3, 3), peca_final_no_buraco_inicial=True):
        """Inicializa o tabuleiro do jogo.

        Keyword Arguments:
            pos_inicial {tuple} -- Posição onde do primeiro buraco (default: {(3, 3)})
            peca_final_no_buraco_inicial {bool} -- Se True será exigido que a solução 
            tenha a peça restante na mesma posição do buraco inicial (default: {True})
        """

        # valor 2 é posição inválida
        # valor 1 é uma peça
        # valor 0 é um burcao
        self.tabuleiro = [
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2]
        ]
        self.pos_inicial = pos_inicial
        self.remover(self.pos_inicial)

        self.pecas_restantes = 32
        self.peca_final_no_buraco_inicial = peca_final_no_buraco_inicial

        # pilha de movimentos realizados
        self.movimentos = []

    def reset(self):
        """ Reseta o jogo
        """
        self.__init__(self.pos_inicial, self.peca_final_no_buraco_inicial)

    def __repr__(self):
        repr_tabuleiro = '   0 1 2 3 4 5 6\n\n'
        for n_linha, linha in enumerate(self.tabuleiro):
            repr_tabuleiro += f"{n_linha}  {' '.join([str(pos) for pos in linha]).replace('2', ' ')}\n"
        return repr_tabuleiro

    def get(self, posicao: tuple):
        """Retorna o elemento do tabuleiro na posição indicada

        Arguments:
            posicao {tuple} -- (linha, coluna) da posição no tabuleiro

        Returns:
            int -- valor da posição solicitada
        """
        return self.tabuleiro[posicao[0]][posicao[1]]

    def set(self, posicao: tuple):
        """ Coloca uma peça (valor 1) no tabuleiro na posição especificada.

        Arguments:
            posicao {tuple} -- (linha, coluna) para inserir a peça
        """
        self.tabuleiro[posicao[0]][posicao[1]] = 1

    def remover(self, posicao: tuple):
        """Remove uma peça (coloca valor 0) no tabuleiro na posição indicada

        Arguments:
            posicao {tuple} -- (linha, coluna) da posição que terá a peça removida
        """
        self.tabuleiro[posicao[0]][posicao[1]] = 0

    def _valido(self, movimento):
        """Verifica se um movimento é válido.

        Arguments:
            movimento {Movimento} -- movimento a ser verificado em relação ao 
            estado atual do tabuleiro.

        Returns:
            bool -- Verdadeiro para movimento válido, e movimento inválido
        """
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
        """Realiza o movimento se este for válido.

        Arguments:
            movimento {Movimento} -- movimento válido a ser realizado.

        Returns:
            bool -- Retorna True caso o movimento tenha sido realizado, 
            False caso contrário
        """
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
        """Retorna uma lista de todos os movimentos válidos.

        Returns:
            list -- Lista de instâncias válidas de Movimento
        """
        movimentos_validos = []
        for linha, coluna in COORDS_VALIDAS:
            if self.get((linha, coluna)) == 2:
                continue
            for direcao in DIRECOES:
                movimento = Movimento((linha, coluna), direcao)
                if self._valido(movimento):
                    movimentos_validos.append(movimento)
        return movimentos_validos

    def tem_movimentos(self):
        """Verifica se o estado atual do tabuleiro é tem movimentos válidos.

        Returns:
            bool -- True caso o jogo tenha movimentos válidos, False caso contrário
        """
        return len(self.get_movimentos_validos()) >= 1

    def esta_solucionado(self):
        """Verifica se o estado atual do jogo é uma solução.

        Returns:
            bool -- True caso o jogo esteja solucionado, False caso contrário
        """
        solucionado = False
        if self.peca_final_no_buraco_inicial:
            solucionado = self.pecas_restantes == 1 and self.get(self.pos_inicial) == 1
        else:
            solucionado = self.pecas_restantes == 1
        return solucionado

    def desfazer_movimento(self):
        """Desfaz o último movimento realizado.
        """

        movimento = self.movimentos.pop()
        pos_nova = movimento.nova_posicao
        pos_anterior = movimento.posicao
        peca_saltada = movimento.saltada

        self.remover(pos_nova)
        self.set(pos_anterior)
        self.set(peca_saltada)

        # como um movimento foi desfeito, a peça removida por ele voltou
        self.pecas_restantes += 1
    
    def ident(self):
        """Retorna string de representação do tabuleiro do jogo.

        Returns:
            str -- representação do tabuleiro do jogo.
        """
        ident = ''
        for linha in self.tabuleiro:
            for item in linha:
                ident += str(item)
        return ident


class SolucionadorResta1:
    def __init__(self, jogo: Tabuleiro, callback_visualizacao = None):
        """Inicializa o solucionador para o jogo.

        A callback_visualizacao quando chamda recebe como parâmetro a instância 
        do solucionador.
        Atenção: a callback_visualizacao não deve alterar qualquer estrutura
        de dados da instância recebida, para que não cause problemas.

        Arguments:
            jogo {Tabuleiro} -- tabuleiro do jogo

        Keyword Arguments:
            callback_visualizacao {function} -- Função que será chamada
            para cada alteração do tabuleiro. Está função tem assinatura
            callback_visualizacao(solucionador). (default: {None})
        """
        self.jogo = jogo
        nop = lambda *args: None
        self.callback_visualizacao = callback_visualizacao or nop
        self.total_de_movimentos = 0
        # self.callback_visualizacao(self)

    def solucionar(self, recursivo=True):
        """Soluciona o jogo se possível.

        Keyword Arguments:
            recursivo {bool} -- Define se será utilizado o algoritmo recursivo. (default: {True})

        Returns:
            bool -- Retorna True se encontrar uma solução, False caso contrário.
        """
        self.jogo.reset()
        self.total_de_movimentos = 0
        if recursivo:
            return self._solucionar()
        else:
            return self._solucionar_nao_recursivo()

    def _solucionar(self, movimentos_realizados = 0):
        """Tenta solucionar o jogo utilizando backtracking.

        Keyword Arguments:
            movimentos_realizados {int} -- Numero de movimentos realizados 
            (deve ser utilizado apenas internamente para verificação da 
            condição de parada) (default: {0})

        Returns:
            bool -- True se existe solução, False se não existe solução.
        """
        if movimentos_realizados == 31:
            if self.jogo.esta_solucionado():
                return True

        for linha, coluna in COORDS_VALIDAS:
            for direcao in DIRECOES:
                movimento = Movimento((linha, coluna), direcao)
                if self.jogo.mover(movimento):
                    self.callback_visualizacao(self)
                    self.total_de_movimentos += 1
                    if self._solucionar(movimentos_realizados+1):
                        return True
                    
                    self.jogo.desfazer_movimento()
                    self.callback_visualizacao(self)
        
        # retorna False caso tenha tentado todas as possibilidades
        # e nenhuma solução foi encontrada
        return False

    def _solucionar_nao_recursivo(self):
        """Tenta solucionar o jogo utilizando backtracking sem o uso de recursão.

        Returns:
            bool -- True se existe solução, False se não existe solução.
        """
        # mantém uma pilha de movimentos váilidos para cada estado visitado,
        # quando a pilha fica vazia significa que todos os movimentos 
        # para aquele estado foram visitados
        estados = {}
        id_inicial = self.jogo.ident()
        estados[id_inicial] = {'visitados': [], 'movimentos': self.jogo.get_movimentos_validos()}
        movimentos_realizados = 0
        while estados[id_inicial]['movimentos']:
            id_jogo = self.jogo.ident()

            if estados[id_jogo]['movimentos']:
                movimento = estados[id_jogo]['movimentos'].pop()
            else:
                self.jogo.desfazer_movimento()
                movimentos_realizados-=1
                self.callback_visualizacao(self)
                continue

            if self.jogo.mover(movimento):
                self.total_de_movimentos += 1
                self.callback_visualizacao(self)
                id_jogo = self.jogo.ident()

                movimentos_realizados+=1
                if movimentos_realizados == 31:
                    if self.jogo.esta_solucionado():
                        return True

                if not estados.get(id_jogo):
                    estados[id_jogo] = {'visitados': [movimento], 'movimentos': self.jogo.get_movimentos_validos()}
                else:
                    estados[id_jogo]['visitados'].append(movimento)

        # retorna False caso tenha tendado todas as possibilidades
        # e nenhuma solução foi encontrada
        return False

if __name__ == "__main__":
    jogo = Tabuleiro()

    tempo_inicio = time.time()
    solucao = False
    solver = SolucionadorResta1(jogo)
    print("Por favor aguarde!")
    tem_solucao = solver.solucionar()
    # tem_solucao = solver.solucionar(False)

    print(f"Tempo de execução: {time.time() - tempo_inicio} secs")
    print("Solução: ")
    if tem_solucao:
        for mov in jogo.movimentos:
            # mapeia N, S, L, O para cima, baixo, direita, esquerda
            mov = str(mov).replace('N', 'cima')
            mov = str(mov).replace('S', 'baixo')
            mov = str(mov).replace('L', 'direita')
            mov = str(mov).replace('O', 'esquerda')
            print(str(mov))
        print(f"Total de movimentos válidos realizados para alcançar a solução: {solver.total_de_movimentos}")
    else:
        print("Este jogo não tem solução.")