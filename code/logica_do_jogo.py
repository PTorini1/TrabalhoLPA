import random

class CampoMinado:
    def __init__(self, linhas=16, colunas=16, bombas=40):
        self.linhas = linhas
        self.colunas = colunas
        self.bombas = bombas
        self.tabuleiro = [[0 for _ in range(colunas)] for _ in range(linhas)]
        self.revelado = [[False for _ in range(colunas)] for _ in range(linhas)]
        self.marcado = [[False for _ in range(colunas)] for _ in range(linhas)]
        self.jogo_terminado = False
        self.jogo_ganho = False
        self.posicoes_bombas = set()
        self.primeiro_clique = True
        
    def insereBombas(self, linha_segura, coluna_segura):
        """Coloca as minas no tabuleiro, evitando a posição do primeiro clique"""
        bombas_colocadas = 0
        while bombas_colocadas < self.bombas:
            linha = random.randint(0, self.linhas - 1)
            coluna = random.randint(0, self.colunas - 1)
            
            if (abs(linha - linha_segura) <= 1 and abs(coluna - coluna_segura) <= 1) or (linha, coluna) in self.posicoes_bombas:
                continue
                
            self.posicoes_bombas.add((linha, coluna))
            self.tabuleiro[linha][coluna] = -1
            bombas_colocadas += 1
        
        self.calculaNumerosDeBombasAoRedor()
    
    def calculaNumerosDeBombasAoRedor(self):
        """Calcula os números para cada célula baseado nas minas adjacentes"""
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if self.tabuleiro[linha][coluna] != -1: 
                    contador = 0
                    for dl in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dl == 0 and dc == 0:
                                continue
                            nova_linha, nova_coluna = linha + dl, coluna + dc
                            if (0 <= nova_linha < self.linhas and 
                                0 <= nova_coluna < self.colunas and 
                                self.tabuleiro[nova_linha][nova_coluna] == -1):
                                contador += 1
                    self.tabuleiro[linha][coluna] = contador
    
    def revelaCampo(self, linha, coluna):
        """Revela uma célula e retorna True se é uma mina"""
        if (linha < 0 or linha >= self.linhas or 
            coluna < 0 or coluna >= self.colunas or 
            self.revelado[linha][coluna] or 
            self.marcado[linha][coluna]):
            return False
        
        if self.primeiro_clique:
            self.insereBombas(linha, coluna)
            self.primeiro_clique = False
        
        self.revelado[linha][coluna] = True
        
        if self.tabuleiro[linha][coluna] == -1:
            self.jogo_terminado = True
            return True
        
        if self.tabuleiro[linha][coluna] == 0:
            for dl in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dl == 0 and dc == 0:
                        continue
                    self.revelaCampo(linha + dl, coluna + dc)
        
        self.verifica_vitoria()
        return False
    
    def troca_para_bandeira(self, linha, coluna):
        """Alterna a bandeira em uma célula"""
        if (linha < 0 or linha >= self.linhas or 
            coluna < 0 or coluna >= self.colunas or 
            self.revelado[linha][coluna]):
            return
        
        self.marcado[linha][coluna] = not self.marcado[linha][coluna]
    
    def verifica_vitoria(self):
        """Verifica se o jogador ganhou"""
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                if not self.revelado[linha][coluna] and self.tabuleiro[linha][coluna] != -1:
                    return False
        self.jogo_ganho = True
        return True
    
    def retorna_numero_de_bombas(self):
        """Retorna o número de minas restantes (minas totais - bandeiras colocadas)"""
        bandeiras_contadas = sum(sum(linha) for linha in self.marcado)
        return self.bombas - bandeiras_contadas
    
    def reinicia_jogo(self):
        """Reinicia o jogo"""
        self.tabuleiro = [[0 for _ in range(self.colunas)] for _ in range(self.linhas)]
        self.revelado = [[False for _ in range(self.colunas)] for _ in range(self.linhas)]
        self.marcado = [[False for _ in range(self.colunas)] for _ in range(self.linhas)]
        self.jogo_terminado = False
        self.jogo_ganho = False
        self.posicoes_bombas = set()
        self.primeiro_clique = True
