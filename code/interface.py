import pygame
import os
import sys
from .logica_do_jogo import CampoMinado

class InterfaceCampoMinado:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.TAMANHO_CELULA = 30
        self.MARGEM = 100
        self.jogo = None
        self.dificuldade = "medio"
        self.dificuldades = {
            "facil": (9, 9, 10),
            "medio": (16, 16, 40),
            "dificil": (16, 30, 99)
        }
        
        # Cores
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.CINZA = (128, 128, 128)
        self.CINZA_CLARO = (192, 192, 192)
        self.CINZA_ESCURO = (64, 64, 64)
        self.VERMELHO = (255, 0, 0)
        self.VERDE = (0, 255, 0)
        self.AZUL = (0, 0, 255)
        self.AMARELO = (255, 255, 0)
        
        # Cores para números
        self.CORES_NUMEROS = {
            1: (0, 0, 255),      # Azul
            2: (0, 128, 0),      # Verde
            3: (255, 0, 0),      # Vermelho
            4: (128, 0, 128),    # Roxo
            5: (128, 0, 0),      # Marrom
            6: (0, 128, 128),    # Turquesa
            7: (0, 0, 0),        # Preto
            8: (128, 128, 128)   # Cinza
        }
        
        # Estado do jogo
        self.estado = "menu" 
        self.carregar_recursos()
        self.inicializar_tela()
        self.fonte = pygame.font.Font(None, 24)
        self.fonte_grande = pygame.font.Font(None, 48)
    
    def carregar_recursos(self):
        """Carrega as imagens e sons"""
        caminho_recursos = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        
        try:
            self.imagem_bomba = pygame.image.load(os.path.join(caminho_recursos, "bomb.png"))
            self.imagem_bandeira = pygame.image.load(os.path.join(caminho_recursos, "flag.png"))
            
            self.imagem_bomba = pygame.transform.scale(self.imagem_bomba, (self.TAMANHO_CELULA - 4, self.TAMANHO_CELULA - 4))
            self.imagem_bandeira = pygame.transform.scale(self.imagem_bandeira, (self.TAMANHO_CELULA - 4, self.TAMANHO_CELULA - 4))
            
            self.som_bomba = pygame.mixer.Sound(os.path.join(caminho_recursos, "bomb-sound.wav"))
            self.som_game_over = pygame.mixer.Sound(os.path.join(caminho_recursos, "game-over.mp3"))
            self.som_acerto = pygame.mixer.Sound(os.path.join(caminho_recursos, "right-flag.mp3"))  # Som quando acerta uma célula
            self.som_vitoria = pygame.mixer.Sound(os.path.join(caminho_recursos, "game-win.mp3"))
            
        except Exception as e:
            print(f"Erro ao carregar assets: {e}")
            self.imagem_bomba = pygame.Surface((self.TAMANHO_CELULA - 4, self.TAMANHO_CELULA - 4))
            self.imagem_bomba.fill(self.VERMELHO)
            self.imagem_bandeira = pygame.Surface((self.TAMANHO_CELULA - 4, self.TAMANHO_CELULA - 4))
            self.imagem_bandeira.fill(self.AMARELO)
            self.som_bomba = None
            self.som_game_over = None
            self.som_acerto = None
            self.som_vitoria = None
    
    def inicializar_tela(self):
        """Inicializa a tela baseada na dificuldade atual"""
        if self.estado == "menu":
            self.largura_tela = 600
            self.altura_tela = 500
        else:
            linhas, colunas, _ = self.dificuldades[self.dificuldade]
            self.largura_tela = colunas * self.TAMANHO_CELULA + 40
            self.altura_tela = linhas * self.TAMANHO_CELULA + self.MARGEM + 40
        
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption("Campo Minado")
    
    def desenhar_menu(self):
        """Desenha o menu principal"""
        self.tela.fill(self.BRANCO)
        
        titulo = self.fonte_grande.render("CAMPO MINADO", True, self.PRETO)
        retangulo_titulo = titulo.get_rect(center=(self.largura_tela // 2, 100))
        self.tela.blit(titulo, retangulo_titulo)
        
        informacoes_dificuldades = [
            ("Fácil (9x9, 10 minas)", "facil", 200),
            ("Médio (16x16, 40 minas)", "medio", 250),
            ("Difícil (16x30, 99 minas)", "dificil", 300)
        ]
        
        self.botoes_menu = []
        for texto, dific, y in informacoes_dificuldades:
            cor = self.VERDE if dific == self.dificuldade else self.CINZA_CLARO
            retangulo_botao = pygame.Rect(150, y, 300, 40)
            pygame.draw.rect(self.tela, cor, retangulo_botao)
            pygame.draw.rect(self.tela, self.PRETO, retangulo_botao, 2)
            
            superficie_texto = self.fonte.render(texto, True, self.PRETO)
            retangulo_texto = superficie_texto.get_rect(center=retangulo_botao.center)
            self.tela.blit(superficie_texto, retangulo_texto)
            
            self.botoes_menu.append((retangulo_botao, dific))
        
        botao_jogar = pygame.Rect(200, 380, 200, 50)
        pygame.draw.rect(self.tela, self.VERDE, botao_jogar)
        pygame.draw.rect(self.tela, self.PRETO, botao_jogar, 3)
        
        texto_jogar = self.fonte_grande.render("JOGAR", True, self.PRETO)
        retangulo_texto_jogar = texto_jogar.get_rect(center=botao_jogar.center)
        self.tela.blit(texto_jogar, retangulo_texto_jogar)
        
        self.botao_jogar = botao_jogar
    
    def desenhar_jogo(self):
        """Desenha o jogo"""
        self.tela.fill(self.BRANCO)
        
        if not self.jogo:
            return
        
        bombas_restantes = self.jogo.retorna_numero_de_bombas()
        texto_bombas = self.fonte.render(f"Minas: {bombas_restantes}", True, self.PRETO)
        self.tela.blit(texto_bombas, (10, 10))
        
        if self.jogo.jogo_ganho:
            texto_status = self.fonte.render("VOCÊ GANHOU!", True, self.VERDE)
        elif self.jogo.jogo_terminado:
            texto_status = self.fonte.render("GAME OVER!", True, self.VERMELHO)
        else:
            texto_status = self.fonte.render("Botão esquerdo: Revela | Botão direito: Bandeira", True, self.PRETO)

        retangulo_status = texto_status.get_rect(center=(self.largura_tela // 2, 30))
        self.tela.blit(texto_status, retangulo_status)
        
        botao_menu = pygame.Rect(10, self.altura_tela - 40, 100, 30)
        pygame.draw.rect(self.tela, self.CINZA_CLARO, botao_menu)
        pygame.draw.rect(self.tela, self.PRETO, botao_menu, 2)
        texto_menu = self.fonte.render("Menu", True, self.PRETO)
        retangulo_texto_menu = texto_menu.get_rect(center=botao_menu.center)
        self.tela.blit(texto_menu, retangulo_texto_menu)
        self.botao_menu = botao_menu
        
        botao_reiniciar = pygame.Rect(120, self.altura_tela - 40, 100, 30)
        pygame.draw.rect(self.tela, self.CINZA_CLARO, botao_reiniciar)
        pygame.draw.rect(self.tela, self.PRETO, botao_reiniciar, 2)
        texto_reiniciar = self.fonte.render("Reiniciar", True, self.PRETO)
        retangulo_texto_reiniciar = texto_reiniciar.get_rect(center=botao_reiniciar.center)
        self.tela.blit(texto_reiniciar, retangulo_texto_reiniciar)
        self.botao_reiniciar = botao_reiniciar
        
        self.desenhar_tabuleiro()
    
    def desenhar_tabuleiro(self):
        """Desenha o tabuleiro do jogo"""
        inicio_x = 20
        inicio_y = 60
        
        for linha in range(self.jogo.linhas):
            for coluna in range(self.jogo.colunas):
                x = inicio_x + coluna * self.TAMANHO_CELULA
                y = inicio_y + linha * self.TAMANHO_CELULA
                retangulo = pygame.Rect(x, y, self.TAMANHO_CELULA, self.TAMANHO_CELULA)
                
                if self.jogo.revelado[linha][coluna]:
                    if self.jogo.tabuleiro[linha][coluna] == -1:
                        pygame.draw.rect(self.tela, self.VERMELHO, retangulo)
                    else:
                        pygame.draw.rect(self.tela, self.BRANCO, retangulo)
                else:
                    pygame.draw.rect(self.tela, self.CINZA_CLARO, retangulo)
                
                pygame.draw.rect(self.tela, self.PRETO, retangulo, 1)
                
                if self.jogo.marcado[linha][coluna] and not self.jogo.revelado[linha][coluna]:
                    self.tela.blit(self.imagem_bandeira, (x + 2, y + 2))
                elif self.jogo.revelado[linha][coluna]:
                    if self.jogo.tabuleiro[linha][coluna] == -1:
                        self.tela.blit(self.imagem_bomba, (x + 2, y + 2))
                    elif self.jogo.tabuleiro[linha][coluna] > 0:
                        numero = str(self.jogo.tabuleiro[linha][coluna])
                        cor = self.CORES_NUMEROS.get(self.jogo.tabuleiro[linha][coluna], self.PRETO)
                        texto = self.fonte.render(numero, True, cor)
                        retangulo_texto = texto.get_rect(center=retangulo.center)
                        self.tela.blit(texto, retangulo_texto)
    
    def obter_celula_da_posicao(self, posicao):
        """Converte posição do mouse para coordenadas da célula"""
        if self.estado != "jogando" or not self.jogo:
            return None, None
        
        inicio_x = 20
        inicio_y = 60
        
        x, y = posicao
        coluna = (x - inicio_x) // self.TAMANHO_CELULA
        linha = (y - inicio_y) // self.TAMANHO_CELULA
        
        if 0 <= linha < self.jogo.linhas and 0 <= coluna < self.jogo.colunas:
            return linha, coluna
        return None, None
    
    def processar_clique(self, posicao, botao):
        """Processa cliques do mouse"""
        if self.estado == "menu":
            self.processar_clique_menu(posicao, botao)
        elif self.estado == "jogando":
            self.processar_clique_jogo(posicao, botao)
    
    def processar_clique_menu(self, posicao, botao):
        """Processa cliques no menu"""
        if botao != 1: 
            return
        
        for retangulo_botao, dificuldade in self.botoes_menu:
            if retangulo_botao.collidepoint(posicao):
                self.dificuldade = dificuldade
                return
        
        if self.botao_jogar.collidepoint(posicao):
            self.iniciar_jogo()
    
    def processar_clique_jogo(self, posicao, botao):
        """Processa cliques no jogo"""
        if botao == 1: 
            if hasattr(self, 'botao_menu') and self.botao_menu.collidepoint(posicao):
                self.estado = "menu"
                self.inicializar_tela()
                return
            
            if hasattr(self, 'botao_reiniciar') and self.botao_reiniciar.collidepoint(posicao):
                self.iniciar_jogo()
                return
        
        if self.jogo.jogo_terminado or self.jogo.jogo_ganho:
            return
        
        linha, coluna = self.obter_celula_da_posicao(posicao)
        if linha is None or coluna is None:
            return
        
        if botao == 1: 
            ja_revelada = self.jogo.revelado[linha][coluna]
            
            acertou_bomba = self.jogo.revelaCampo(linha, coluna)
            if acertou_bomba:
                if self.som_bomba:
                    self.som_bomba.play()
                if self.som_game_over:
                    pygame.time.wait(500)
                    self.som_game_over.play()
            elif not ja_revelada and self.jogo.revelado[linha][coluna]:
                if self.som_acerto:
                    self.som_acerto.play()
                    
            if self.jogo.jogo_ganho and self.som_vitoria:
                self.som_vitoria.play()
        elif botao == 3: 
            self.jogo.troca_para_bandeira(linha, coluna)
    
    def iniciar_jogo(self):
        """Inicia um novo jogo"""
        linhas, colunas, bombas = self.dificuldades[self.dificuldade]
        self.jogo = CampoMinado(linhas, colunas, bombas)
        self.estado = "jogando"
        self.inicializar_tela()
    
    def executar(self):
        """Loop principal do jogo"""
        relogio = pygame.time.Clock()
        executando = True
        
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.processar_clique(evento.pos, evento.button)
            
            if self.estado == "menu":
                self.desenhar_menu()
            elif self.estado == "jogando":
                self.desenhar_jogo()
            
            pygame.display.flip()
            relogio.tick(60)
        
        pygame.quit()
        sys.exit()
