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
        
        self.fonte_maior = pygame.font.SysFont("Arial", 26)
        self.fonte = pygame.font.SysFont("Arial", 20)
        self.fonte_menor = pygame.font.SysFont("Arial", 16)

        # Define as cores de elementos
        self.paleta = {
            "background": (240, 240, 250),
            "no": (240, 240, 250),
            "no_destacado": (240, 210, 250),
            "borda": (70, 70, 80),
            "text": (70, 70, 80),
            "line": (70, 70, 80),
            "botao_insercao": (13, 222, 181),
            "botao_remocao": (222, 13, 181),
            "botao_busca_leitura": (242, 181, 13),
            "botao_texto": (255, 255, 255),
            "input_background": (255, 255, 255),
            "input_borda": (200, 200, 200)
        }
        
        self.raio_node = 25
        self.espacamento_y = 100  # Espaçamento vertical entre nós
        
        self.input_texto = ""
        self.input_estado = False
        self.velocidade_animacoes = 2
        self.fila_animacoes = deque()
        self.atual_animacao = None
        self.progresso_animacoes = 0
        
        # Área de visualização da árvore (abaixo dos controles)
        self.area_arvore_y = 150
        
        # Sistema de arraste (panning)
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
             botao_largura,
             botao_altura
        )
        
        self.aba_superior = pygame.Rect(
             0,
             0,
             self.largura,
             self.area_arvore_y
        )
        
    def gerenciar_eventos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verificar clique nos controles
                if self.campo_input.collidepoint(evento.pos):
                    self.input_estado = True
                elif self.botao_insercao.collidepoint(evento.pos):
                    self.inserir_valor()
                # Verificar se o clique foi na área da árvore para arrastar
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
                
            if evento.type == pygame.KEYDOWN and self.input_estado:
                if evento.key == pygame.K_RETURN:
                    self.inserir_valor()
                elif evento.key == pygame.K_BACKSPACE:
                    self.input_texto = self.input_texto[:-1]
                elif evento.unicode.isdigit():
                    self.input_texto += evento.unicode
        
        return True
    
    def inserir_valor(self):
        if not self.input_texto:
            return
            
        try:
            valor = int(self.input_texto)
            self.insereNo(valor)
            
            for acao in self.historico:
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
        
        if raiz.esquerda:
            self.atualizar_layout(raiz.esquerda, x - dx, y + self.espacamento_y, dx / 2)
        
        if raiz.direita:
            self.atualizar_layout(raiz.direita, x + dx, y + self.espacamento_y, dx / 2)

    def animar_movimento_no(self, no, progresso):
        ease_progress = 1 - (1 - progresso) ** 2
        
        if no.pai is None: 
            x0, y0 = no.pos
        else: 
            x0, y0 = no.pai.pos
        
        x_final, y_final = no.posicao_alvo
        
        x = x0 + (x_final - x0) * ease_progress
        y = y0 + (y_final - y0) * ease_progress
        
        no.pos = (x, y)

    def atualizar(self):
        
        if self._raiz:
            self.atualizar_layout(self._raiz, self.largura/2, self.area_arvore_y + 50, self.largura/4)
        
        if not self.atual_animacao and self.fila_animacoes:
            self.atual_animacao = self.fila_animacoes.popleft()
            self.progresso_animacoes = 0
        
        if self.atual_animacao:
            tipo_acao = self.atual_animacao[0]
            
            if tipo_acao in ("visitar", "criar"):
                self.progresso_animacoes += 0.02 * self.velocidade_animacoes
                if self.progresso_animacoes >= 1:
                    self.atual_animacao = None
            
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
        
        if not no:
            return
        
        pos_no = (no.pos[0] + self.offset_x, no.pos[1] + self.offset_y)
        pos_esq = (no.esquerda.pos[0] + self.offset_x, no.esquerda.pos[1] + self.offset_y) if no.esquerda else None
        pos_dir = (no.direita.pos[0] + self.offset_x, no.direita.pos[1] + self.offset_y) if no.direita else None
        
        # Ligações
        if no.esquerda:
            pygame.draw.line(self.tela, self.paleta["line"], pos_no, pos_esq, 3)
        
        if no.direita:
            pygame.draw.line(self.tela, self.paleta["line"], pos_no, pos_dir, 3)
        
        self.desenhar_arvore(no.esquerda, no_destaque)
        self.desenhar_arvore(no.direita, no_destaque)
        
        # Desenha o nó
        # Verificar se o nó está dentro da área visível (opcional, para performance)
        cor = self.paleta["no_destacado"] if no == no_destaque else self.paleta["no"]
        
        pygame.draw.circle(self.tela, cor, pos_no, self.raio_node)
        pygame.draw.circle(self.tela, self.paleta["borda"], pos_no, self.raio_node, 3)

        texto_valor = self.fonte.render(str(no.valor), True, self.paleta["text"])
        rect_valor = texto_valor.get_rect(center=pos_no)
        self.tela.blit(texto_valor, rect_valor)
        
        texto_altura = self.fonte_menor.render(f"fb = {no.fatorBalanceamento()}", True, (80, 80, 100))
        rect_altura = texto_altura.get_rect(center=(pos_no[0], pos_no[1] + self.raio_node + 15))
        self.tela.blit(texto_altura, rect_altura)

    def desenhar_interface(self):
        
        # Desenhar controles e abas
        
        pygame.draw.rect(self.tela, self.paleta["borda"], self.aba_superior)
        pygame.draw.rect(self.tela, self.paleta["input_background"], self.campo_input, border_radius=5)
        pygame.draw.rect(self.tela, self.paleta["borda"], self.campo_input, 2, border_radius=5)
        
        texto_input = self.fonte_maior.render(self.input_texto, True, self.paleta["text"])
        self.tela.blit(texto_input, (self.campo_input.x + 10, self.campo_input.y + 8))
        
        pygame.draw.rect(self.tela, self.paleta["botao_insercao"], self.botao_insercao, border_radius=5)
        texto_insercao = self.fonte_maior.render("Inserir", True, self.paleta["botao_texto"])
        self.tela.blit(texto_insercao, (self.botao_insercao.x + 25, self.botao_insercao.y + 8))

    def executar(self):
        clock = pygame.time.Clock()
        rodando = True
        
        while rodando:
            rodando = self.gerenciar_eventos()
            self.atualizar()
            
            self.tela.fill(self.paleta["background"])
            
            # Desenhar área da árvore (com offset)
            if self._raiz:
                no_destaque = None
                if self.atual_animacao:
                    tipo_acao = self.atual_animacao[0]
                    if tipo_acao in ("visitar", "rotacionar", "criar"):
                        no_destaque = self.atual_animacao[1]
                
                self.desenhar_arvore(self._raiz, no_destaque)
            
            self.desenhar_interface()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    visualizador = Visualizador()
    visualizador.executar()