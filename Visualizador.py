from ArvoreAVL import ArvoreAVL
import pygame
import sys
from collections import deque
import math

class Visualizador(ArvoreAVL):
    
    def __init__(self):
        super().__init__()
        pygame.init()
        
        self.largura = 1600
        self.altura = 800
        
        # Cria a tela e o título
        self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
        pygame.display.set_caption("Visualizador de Árvore AVL")
        
        self.fonte_maior = pygame.font.SysFont("Roboto", 44, bold=True)
        self.fonte = pygame.font.SysFont("Arial", 18, bold=True)
        self.fonte_menor = pygame.font.SysFont("Arial", 14)

        # Define as cores de elementos
        self.paleta = {
            "background": (240, 240, 250),
            "no": (240, 240, 250),
            "no_destacado": (240, 210, 250),
            "borda": (70, 70, 80),
            "text": (70, 70, 80),
            "line": (70, 70, 80),
            "botao_insercao": (13, 200, 160),
            "botao_remocao": (222, 13, 121),
            "botao_busca_leitura": (222, 181, 13),
            "botao_texto": (255, 255, 255),
            "input_background": (255, 255, 255),
            "no_buscado":(180,240,250)
        }
        
        self.no_encontrado = None
        self.no_removido = None
        self.raio_no = 25
        self.espacamento_y = 100  # Espaçamento vertical entre nós
        
        self.input_texto = ""
        self.input_estado = False
        self.velocidade_animacoes = 2
        self.fila_animacoes = deque()
        self.atual_animacao = None
        self.progresso_animacoes = 0
        self.no_destacado = set()
        
        # Área de visualização da árvore
        self.area_arvore_y = 150
        
        # Sistema de arraste
        self.arrastando = False
        self.offset_x = 0
        self.offset_y = 0
        self.mouse_pos_inicial_arraste = (0, 0)
        self.offset_inicial_arraste = (0, 0)
        
        self.criar_elementos_interface()
        
    def criar_elementos_interface(self):
        
        botao_largura = self.largura * 0.1
        botao_altura = self.altura / 20
        
        self.campo_input = pygame.Rect(
             self.largura / 40,
             self.altura / 30,
             botao_largura,
             botao_altura
        )
        
        self.botao_insercao = pygame.Rect(
             self.largura / 8 + (self.largura / 80),
             self.altura / 30,
             botao_largura + 20,
             botao_altura
        )

        #UPDATE
        self.botao_remocao = pygame.Rect(
            self.botao_insercao.right + (self.largura / 80),
            self.altura / 30,
            botao_largura + 20,
            botao_altura
        )
        
        self.botao_busca = pygame.Rect(
            self.botao_remocao.right + (self.largura / 80),
            self.altura / 30,
            botao_largura + 20,
            botao_altura
        )

        self.aba_superior = pygame.Rect(
             0,
             0,
             self.largura,
             self.area_arvore_y
        )
        
    def gerenciar_eventos(self):
        
        mouse_x, mouse_y = pygame.mouse.get_pos() # Obtém a posição do mouse
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica clique nos botões e campos
                
                if self.campo_input.collidepoint(evento.pos):
                    self.input_estado = True
                    
                elif self.botao_insercao.collidepoint(evento.pos):
                    self.inserir_valor()

                elif self.botao_busca.collidepoint(evento.pos):
                    self.buscar_valor()

                #UPDATE
                elif self.botao_remocao.collidepoint(evento.pos):
                    self.remover_valor()
  
                # Verifica se o clique foi na área da árvore para arrastar
                elif mouse_y > self.area_arvore_y:
                    self.arrastando = True
                    self.mouse_pos_inicial_arraste = (mouse_x, mouse_y)
                    self.offset_inicial_arraste = (self.offset_x, self.offset_y)
                else:
                    self.input_estado = False
            
            if evento.type == pygame.MOUSEBUTTONUP:
                self.arrastando = False
                
            if evento.type == pygame.MOUSEMOTION and self.arrastando:
                # Calcular o deslocamento do mouse
                dx = mouse_x - self.mouse_pos_inicial_arraste[0]
                dy = mouse_y - self.mouse_pos_inicial_arraste[1]
                # Atualizar o offset
                self.offset_x = self.offset_inicial_arraste[0] + dx
                self.offset_y = self.offset_inicial_arraste[1] + dy
                
            if evento.type == pygame.KEYDOWN:
                if self.input_estado:
                    if evento.key == pygame.K_BACKSPACE:
                        self.input_texto = self.input_texto[:-1]
                    elif evento.unicode.isdigit():
                        self.input_texto += evento.unicode
                    elif evento.key == pygame.K_b:
                        self.buscar_valor()
                    elif evento.key == pygame.K_r:
                        self.remover_valor()
                    elif evento.key == pygame.K_RETURN or pygame.K_i:
                        self.no_encontrado = None #remove o destaque do no buscado quando pressionar enter
                        self.inserir_valor()
        return True
    
    def inserir_valor(self):
        if not self.input_texto:
            return
            
        try:
            valor = int(self.input_texto)
            self.insereNo(valor)
            self.no_encontrado = None  

            for acao in self.historico:
                self.fila_animacoes.append(acao)
            
            self.input_texto = ""
            
        except ValueError:
            self.input_texto = "Iiih..."
            pygame.display.flip()
            pygame.time.delay(500)
            self.input_texto = ""

    def buscar_valor(self):
        if not self.input_texto:
            return

        try:
            valor = int(self.input_texto)
            self.historico = []  # limpa ações anteriores
            self.no_encontrado = None  # limpa destaque anterior
            self.no_destacado.clear()

            self.buscaBin(valor)
        
            for acao in self.historico:
                self.fila_animacoes.append(acao)
                if acao[0] == "encontrar":
                    self.no_encontrado = acao[1]  # armazena o nó encontrado

            self.input_texto = ""  # limpa o campo de input

        except ValueError:
            self.input_texto = "Iiih..."
            pygame.display.flip()
            pygame.time.delay(500)
            self.input_texto = ""

    #UPDATE
    def remover_valor(self):
        if not self.input_texto:
            return

        try:
            valor = int(self.input_texto)
            self.historico = []
            self.no_removido = self.buscaBin(valor)
            self.no_rem_pai = self.no_removido.pai if self.no_removido else None
        
            for acao in self.historico:
                if acao[0] == "encontrar":
                    self.fila_animacoes.append(("remover", acao[1]))
                else:
                    self.fila_animacoes.append(acao)

            self.input_texto = ""

        except ValueError:
            self.input_texto = "Iiih..."
            pygame.display.flip()
            pygame.time.delay(500)
            self.input_texto = ""

    def atualizar_layout(self, raiz, x, y, dx):
        if not raiz:
            return
              
        raiz.posicao_alvo = (x, y)
        
        if self.no_removido and raiz is self.no_removido and self.no_rem_pai:
            raiz.posicao_alvo = self.no_rem_pai.pos

        if raiz.esquerda:
            self.atualizar_layout(raiz.esquerda, x - dx, y + self.espacamento_y, dx / 2)
        
        if raiz.direita:
            self.atualizar_layout(raiz.direita, x + dx, y + self.espacamento_y, dx / 2)

    def animar_movimento_no(self, no, progresso):
        
        suavizar = 1 - (1 - progresso) ** 2
        
        if no.pai and no is not self.no_removido:
            x0, y0 = no.pai.pos
        else:
            x0, y0 = no.pos

        if no is self.no_removido and no.pai:
            x0, y0 = no.pos
            x_final, y_final = no.pai.pos
        else:
            x_final, y_final = no.posicao_alvo
        
        x = x0 + (x_final - x0) * suavizar
        y = y0 + (y_final - y0) * suavizar
        
        no.pos = (x, y)

    def atualizar(self):
        
        if self._raiz:
            self.atualizar_layout(self._raiz, self.largura/2, self.area_arvore_y + 50, self.largura/4)
        
        if not self.atual_animacao and self.fila_animacoes:
            self.atual_animacao = self.fila_animacoes.popleft()
            self.progresso_animacoes = 0

        if self.atual_animacao:
            tipo_acao = self.atual_animacao[0]
            
            if tipo_acao in ("visitar", "inserir", "encontrar"):
                self.progresso_animacoes += 0.02 * self.velocidade_animacoes
                if self.progresso_animacoes >= 1:
                    if self.atual_animacao[1] and self.no_encontrado:
                        self.no_destacado.add(self.atual_animacao[1])
                    self.atual_animacao = None
                    self.no_destaque = None
            
            elif tipo_acao == "remover" and self.no_removido:
                self.progresso_animacoes += 0.1 * self.velocidade_animacoes
                if self.progresso_animacoes >= 1:
                    self.deletaNo(self.no_removido.valor)
                    self.no_removido = None
                    self.atual_animacao = None
                    self.no_destaque = None

            
            elif tipo_acao == "rotacionar":
                self.progresso_animacoes += 0.01 * self.velocidade_animacoes
                if self.progresso_animacoes >= 1:
                    self.atual_animacao = None

        if self._raiz:
            self.animar_nos(self._raiz)
    
    def animar_nos(self, no):
        
        if not no:
            return
        
        if no.pos != no.posicao_alvo:
            self.animar_movimento_no(no, self.progresso_animacoes)
        
        self.animar_nos(no.esquerda)
        self.animar_nos(no.direita)

    def desenhar_arvore(self, no, no_destaque=None):
        
        if not no or no.valor is None:
            return
        
        if not no.pai and not no.esquerda and not no.direita and no != self._raiz:
            return
        
        # Posiciona os nós na tela dependendo também do quanto o usuário arrastou a visualização
        pos_no = (no.pos[0] + self.offset_x, no.pos[1] + self.offset_y)
        pos_esq = (no.esquerda.pos[0] + self.offset_x, no.esquerda.pos[1] + self.offset_y) if no.esquerda else None
        pos_dir = (no.direita.pos[0] + self.offset_x, no.direita.pos[1] + self.offset_y) if no.direita else None
        
        # Ligações
        if no.esquerda and no.esquerda.valor is not None:
            pygame.draw.line(self.tela, self.paleta["line"], pos_no, pos_esq, 3)
        
        if no.direita and no.direita.valor is not None:
            pygame.draw.line(self.tela, self.paleta["line"], pos_no, pos_dir, 3)
        
        self.desenhar_arvore(no.esquerda, no_destaque)
        self.desenhar_arvore(no.direita, no_destaque)
        
        # Desenha o nó
        # Verificar se o nó está dentro da área visível (opcional, para performance)
        if no == self.no_encontrado and no in self.no_destacado:
            cor = self.paleta["no_buscado"]  # Cor especial para nó encontrado
        elif no == no_destaque:
            cor = self.paleta["no_destacado"]
        else:
            cor = self.paleta["no"]
        
        pygame.draw.circle(self.tela, cor, pos_no, self.raio_no)
        pygame.draw.circle(self.tela, self.paleta["borda"], pos_no, self.raio_no, 3)

        texto_valor = self.fonte.render(str(no.valor), True, self.paleta["text"])
        retangulo_valor = texto_valor.get_rect(center=pos_no)
        self.tela.blit(texto_valor, retangulo_valor)
        
        #texto_FB = self.fonte_menor.render(f"FB = {no.fatorBalanceamento()}", True, (80, 80, 100))
        #retangulo_altura = texto_FB.get_rect(center=(pos_no[0], pos_no[1] + self.raio_no + 15))
        #self.tela.blit(texto_FB, retangulo_altura)

    def desenhar_interface(self):
        
        # Desenha aba superior escura
        pygame.draw.rect(self.tela, self.paleta["borda"], self.aba_superior)
        
        # Desenha campo de input
        pygame.draw.rect(self.tela, self.paleta["input_background"], self.campo_input, border_radius=5)
        pygame.draw.rect(self.tela, self.paleta["borda"], self.campo_input, 2, border_radius=5)
        
        texto_input = self.fonte_maior.render(self.input_texto, True, self.paleta["text"])
        self.tela.blit(texto_input, (self.campo_input.x + 10, self.campo_input.y + 5))
        # Blit passa o texto criado para a tela principal
        
        pygame.draw.rect(self.tela, self.paleta["botao_insercao"], self.botao_insercao, border_radius=5)
        texto_insercao = self.fonte_maior.render("INSERIR", True, self.paleta["botao_texto"])
        self.tela.blit(texto_insercao, (self.botao_insercao.x + 18, self.botao_insercao.y + 6))

        pygame.draw.rect(self.tela, self.paleta["botao_busca_leitura"], self.botao_busca, border_radius=5)
        texto_busca = self.fonte_maior.render("BUSCAR", True, self.paleta["botao_texto"])
        self.tela.blit(texto_busca, (self.botao_busca.x + 18, self.botao_busca.y + 6))

        #UPDATE
        pygame.draw.rect(self.tela, self.paleta["botao_remocao"], self.botao_remocao, border_radius=5)
        texto_remocao = self.fonte_maior.render("REMOVER", True, self.paleta["botao_texto"])
        self.tela.blit(texto_remocao, (self.botao_remocao.x + 6, self.botao_remocao.y + 6))

    def executar(self):
        
        clock = pygame.time.Clock() # Inicializa o clock, para regular frames posteriormente
        rodando = True
        
        while rodando:
            
            rodando = self.gerenciar_eventos() # Recebe false quando fecha a janela
            self.atualizar()
            
            self.tela.fill(self.paleta["background"]) # Pinta a tela de branco
            
            # Desenhar área da árvore (com offset)
            if self._raiz:
                no_destaque = None
                if self.atual_animacao:
                    tipo_acao = self.atual_animacao[0] # Armazena a instrução
                    if tipo_acao in ("visitar", "rotacionar", "inserir", "encontrar", "remover"):
                        no_destaque = self.atual_animacao[1] # Vai destacar o nó visualmente se houver uma instrução em [1]
                
                self.desenhar_arvore(self._raiz, no_destaque)
            
            self.desenhar_interface()
            
            pygame.display.flip()
            clock.tick(60) # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    visualizador = Visualizador()
    visualizador.executar()