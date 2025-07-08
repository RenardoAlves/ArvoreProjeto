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
            "botao_texto": (255, 255, 255),
            "input_background": (255, 255, 255),
            "no_buscado":(180,240,250)
        }
        
        self.instrucoes = [
        "Teclas:",
        "BAIXO - Em Ordem",
        "ESQUERDA - Pré-Ordem",
        "DIREITA - Pós-Ordem",
        "O - Centralizar",
        "I - Inserir",
        "B - Buscar",
        "R - Remover",
        "ENTER - Confirmar"
        ]
        
        self.no_encontrado = None
        self.no_removido = None
        self.no_rem_pai = None
        self.raio_no = 25
        self.espacamento_y = 100  # Espaçamento vertical entre nós
        self.count = 0
    
        self.em_tela = []
        
        self.input_texto = ""
        self.input_estado = False
        self.velocidade_animacoes = 2
        self.fila_animacoes = deque()
        self.fila_leitura = deque()
        self.atual_animacao = None
        self.progresso_animacoes = 0
        self.no_destacado = set()
        
        self.leitura_index = 0
        self.tempo_ultima_atualizacao = 0
        self.intervalo_leitura = 500
        self.lendo = False
        
        # Área de visualização da árvore
        self.area_arvore_y = 150
        
        # Sistema de arraste
        self.arrastando = False
        self.offset_x = 0
        self.offset_y = 0
        self.mouse_pos_inicial_arraste = (0, 0)
        self.offset_inicial_arraste = (0, 0)
        
        #Para animações
        self.animando = False
        self.posicoes_antigas = {}
        self.posicoes_novas = {}
        self.anim_frame = 0
        self.anim_passos = 30
        self.animando_sucessor = False
        
        self.criar_elementos_interface()
        
# Método para criar os elementos da interface -------------------------------------------------------------------------------
    
    def criar_elementos_interface(self):
        
        botao_largura = self.largura * 0.1
        botao_altura = self.altura / 20
        
        self.campo_input = pygame.Rect(
             self.largura / 40,
             self.altura / 30,
             botao_largura,
             botao_altura
        )
        
        self.campo_output = pygame.Rect(
             self.largura - 200,
             self.altura / 20,
             botao_largura - 50,
             botao_altura
        )
        
        self.botao_insercao = pygame.image.load("botoes/Insere.png")
        self.retangulo_insercao = self.botao_insercao.get_rect()
        self.retangulo_insercao.topleft = (self.campo_input.right + self.largura / 80, (self.altura / 30))

        self.botao_remocao = pygame.image.load("botoes/Remove.png")
        self.retangulo_remocao = self.botao_remocao.get_rect()
        self.retangulo_remocao.topleft = (self.retangulo_insercao.right + self.largura / 80, self.altura / 30)
        
        self.botao_busca = pygame.image.load("botoes/Busca.png")
        self.retangulo_busca = self.botao_busca.get_rect()
        self.retangulo_busca.topleft = (self.retangulo_remocao.right + self.largura / 80, self.altura / 30)

        self.aba_superior = pygame.Rect(
             0,
             0,
             self.largura,
             self.area_arvore_y
        )
        
# Método para gerenciar eventos (Teclas, clicks, posições do mouse) ---------------------------------------------------------
        
    def gerenciar_eventos(self):
        
        mouse_x, mouse_y = pygame.mouse.get_pos() # Obtém a posição do mouse
        
        for evento in pygame.event.get():
            
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica clique nos botões e campos
                
                if self.campo_input.collidepoint(evento.pos):
                    self.input_estado = True
                    
                elif self.retangulo_insercao.collidepoint(evento.pos):
                    self.inserir_valor()
                    
                elif self.retangulo_busca.collidepoint(evento.pos):
                    self.buscar_valor()
                    
                elif self.retangulo_remocao.collidepoint(evento.pos):
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
                # ENTER: inserir valor
                if evento.key == pygame.K_RETURN:
                    if self.input_estado:
                        self.no_encontrado = None   # remove destaque do nó buscado
                        self.lendo = False
                        self.leitura.clear()
                        self.inserir_valor()
                        
                if evento.key == pygame.K_o:
                    self.offset_x = 0
                    self.offset_y = 0
                elif evento.key == pygame.K_DOWN:
                    self.emOrdem()
                    self.leitura_index = 0
                    self.lendo = True
                    self.tempo_ultima_atualizacao = pygame.time.get_ticks()
                elif evento.key == pygame.K_LEFT:
                    self.preOrdem()
                    self.leitura_index = 0
                    self.lendo = True
                    self.tempo_ultima_atualizacao = pygame.time.get_ticks()
                elif evento.key == pygame.K_RIGHT:
                    self.posOrdem()
                    self.leitura_index = 0
                    self.lendo = True
                    self.tempo_ultima_atualizacao = pygame.time.get_ticks()

                # Outras teclas: backspace, dígitos, busca e remoção
                elif self.input_estado:
                    if evento.key == pygame.K_BACKSPACE:
                        self.input_texto = self.input_texto[:-1]
                    elif evento.unicode.isdigit():
                        self.input_texto += evento.unicode
                    elif evento.key == pygame.K_i:
                        self.inserir_valor()        # atalho "i" para inserir
                    elif evento.key == pygame.K_b:
                        if self.no_encontrado:
                            self.no_encontrado = None
                        else:
                            self.buscar_valor()         # atalho “b” para buscar
                    elif evento.key == pygame.K_r:
                        self.remover_valor()        # atalho “r” para remover

        return True
    
# Método gerenciar as atualizações das leituras -----------------------------------------------------------------------------
    
    def atualizar_leitura(self):
        
        if not self.lendo or not self.leitura:
            return
        
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultima_atualizacao > self.intervalo_leitura:
            self.leitura_index = (self.leitura_index + 1) % len(self.leitura)
            self.tempo_ultima_atualizacao = tempo_atual

# Método para inserir elementos na árvore -----------------------------------------------------------------------------------

    def inserir_valor(self):
        
        if not self.input_texto:
            return
        
        try:
            
            valor = int(self.input_texto)

            # Captura posições antigas (em node.pos)
            if self._raiz:
                self.atualizar_layout(self._raiz,
                                      self.largura/2,
                                      self.area_arvore_y + 50,
                                      self.largura/4)
                self.posicoes_antigas = {
                    no: no.pos
                    for no in self.iterar_nos(self._raiz)
                }
            else:
                self.posicoes_antigas = {}

            # Realiza a inserção + rotações internas
            self.insereNo(valor)

            # Captura posições novas (posicao_alvo)
            self.atualizar_layout(self._raiz,
                                  self.largura/2,
                                  self.area_arvore_y + 50,
                                  self.largura/4)
            self.posicoes_novas = {
                no: no.posicao_alvo
                for no in self.iterar_nos(self._raiz)
            }

            # Ajusta posições iniciais para nós recém-criados
            for no, target in self.posicoes_novas.items():
                if no not in self.posicoes_antigas:
                    if no.pai:
                        # Inicia na posição do pai
                        self.posicoes_antigas[no] = no.pai.pos
                    else:
                        # Raiz recém-criada
                        self.posicoes_antigas[no] = (self.largura/2, self.area_arvore_y + 50)

            # Inicializa animação global
            self.anim_frame = 0
            self.animando = True

            # Limpa estado de busca/animações antigas
            self.no_encontrado = None
            self.no_destacado.clear()
            self.input_texto = ""

        except ValueError:
            self.input_texto = "Iiih..."
            pygame.display.flip()
            pygame.time.delay(500)
            self.input_texto = ""
            
# Método para busca de elementos na árvore ----------------------------------------------------------------------------------
    
    def buscar_valor(self):
        if not self.input_texto:
            return

        try:
            valor = int(self.input_texto)
            self.historico = [] # Limpa ações anteriores
            self.no_encontrado = None # Limpa destaque anterior
            self.no_destacado.clear()

            self.buscaBin(valor)
        
            for acao in self.historico:
                self.fila_animacoes.append(acao)
                if acao[0] == "encontrar":
                    self.no_encontrado = acao[1] # Armazena o nó encontrado

            self.input_texto = "" # Limpa o campo de input

        except ValueError:
            self.input_texto = "Iiih..."
            pygame.display.flip()
            pygame.time.delay(500)
            self.input_texto = ""
#
            
# Método para remover elemento da árvore -----------------------------------------------------------------------------------

    def remover_valor(self):
        if not self.input_texto:
            return

        try:
            valor = int(self.input_texto)
            
            self.no_encontrado = None
            self.no_destacado.clear()
        
            no_a_remover = self.buscaBin(valor)
            if not no_a_remover:
                self.input_texto = ""
                return

            # 1. Salva posições antigas
            self.atualizar_layout(
                self._raiz,
                self.largura / 2,
                self.area_arvore_y + 50,
                self.largura / 4
            )
            self.posicoes_antigas = {no: no.pos for no in self.iterar_nos(self._raiz)}

            # 2. Descobre o sucessor
            sucessor = None
            if no_a_remover.direita:
                sucessor = no_a_remover.direita
                while sucessor.esquerda:
                    sucessor = sucessor.esquerda

            self.no_removido = no_a_remover
            self.sucessor_remocao = sucessor
            self.sucessor_antigo_filho_direita = sucessor.direita if sucessor else None
            
            if sucessor:
                self.sucessor_pos_antiga = tuple(sucessor.pos)
                self.sucessor_pos_alvo = tuple(no_a_remover.pos)
            else:
                self.sucessor_pos_antiga = None
                self.sucessor_pos_alvo = None

            self.input_texto = ""

            self.fila_animacoes.clear()

            # Caso em que o filho é folha (serve para esquerdo e direito)
            filho = None
            if (no_a_remover.esquerda and not no_a_remover.direita):
                filho = no_a_remover.esquerda
            elif (no_a_remover.direita and not no_a_remover.esquerda):
                filho = no_a_remover.direita

            if filho and not (filho.esquerda or filho.direita):
                
                # Filho é folha: anima esse caso
                self.filho_remocao = filho
                self.filho_pos_antiga = tuple(filho.pos)
                self.filho_pos_nova = tuple(no_a_remover.pos)
                self.fila_animacoes.append(("mover_filho_folha", filho))
                
                # INÍCIO IMEDIATO DA ANIMAÇÃO:
                self.atual_animacao = self.fila_animacoes.popleft()
                self.progresso_animacoes = 0
                self.anim_frame = 0
                
                return
            # ------------------------------------------------------------

            if sucessor:
                # Anima percurso até o sucessor
                caminho = self.animar_busca_sucessor(no_a_remover)
                for acao in caminho:
                    self.fila_animacoes.append(acao)
                # Após destacar, anima movimentação do sucessor
                self.fila_animacoes.append(("mover_sucessor", sucessor))
                # Inicialize flags de controle para animação do sucessor
                self.atual_animacao = None
                self.progresso_animacoes = 0
                self.animando_sucessor = False
                self.anim_frame = 0
            else:
                # Caso sem sucessor : remoção direta com animação padrão dos nós
                self.deletaNo(valor)
                # Captura novas posições após a remoção
                if self._raiz:
                    self.atualizar_layout(
                        self._raiz,
                        self.largura / 2,
                        self.area_arvore_y + 50,
                        self.largura / 4
                    )
                    self.posicoes_novas = {no: no.posicao_alvo for no in self.iterar_nos(self._raiz)}
                else:
                    self.posicoes_novas = {}
                # Sinaliza animação padrão
                self.anim_frame = 0
                self.animando = True
                self.no_destacado = set()
                self.no_encontrado = None

        except ValueError:
            self.input_texto = "Iiih..."
            pygame.display.flip()
            pygame.time.delay(500)
            self.input_texto = ""
            
# Método para atualizar o layout da árvore ----------------------------------------------------------------------------------
    
    def atualizar_layout(self, raiz, x, y, dx):
        if not raiz:
            return

        raiz.posicao_alvo = (x, y)

        if raiz.esquerda:
            self.atualizar_layout(raiz.esquerda, x - dx, y + self.espacamento_y, dx / 2)
        if raiz.direita:
            self.atualizar_layout(raiz.direita, x + dx, y + self.espacamento_y, dx / 2)
          
# Método para animar o movimento dos nós ------------------------------------------------------------------------------------

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
      
# Método para percorrer todos os nos ----------------------------------------------------------------------------------------
    
    def iterar_nos(self, raiz):
        if not raiz:
            return
        yield raiz
        yield from self.iterar_nos(raiz.esquerda)
        yield from self.iterar_nos(raiz.direita)


# Método responsável pelo gerenciamento das animações -----------------------------------------------------------------------

    def atualizar(self):
        
        # Fase 1: animação do sucessor indo até a posição do nó removido
        if getattr(self, "animando_sucessor", False) and self.sucessor_remocao and self.sucessor_pos_antiga and self.sucessor_pos_alvo:
            t = min(self.anim_frame / self.anim_passos, 1)
            suavizar = 1 - (1 - t) ** 2
            x0, y0 = self.sucessor_pos_antiga
            x1, y1 = self.sucessor_pos_alvo
            x = x0 + (x1 - x0) * suavizar
            y = y0 + (y1 - y0) * suavizar
            self.sucessor_remocao.pos = (x, y)

            self.anim_frame += 1
            if self.anim_frame > self.anim_passos:
                valor = self.no_removido.valor
                self.deletaNo(valor)
                if self._raiz:
                    self.atualizar_layout(
                        self._raiz,
                        self.largura / 2,
                        self.area_arvore_y + 50,
                        self.largura / 4
                    )
                    self.posicoes_novas = {no: no.posicao_alvo for no in self.iterar_nos(self._raiz)}
                else:
                    self.posicoes_novas = {}

                self.anim_frame = 0
                self.animando_sucessor = False
                self.sucessor_antigo_filho_direita = None
                self.animando = True
                self.no_destacado = set()
                self.no_encontrado = None

            return  # Não faz mais nada enquanto anima o sucessor

        if self.atual_animacao and self.atual_animacao[0] == "mover_filho_folha":
            filho = self.atual_animacao[1]
            t = min(self.anim_frame / self.anim_passos, 1)
            suavizar = 1 - (1 - t) ** 2
            x0, y0 = self.filho_pos_antiga
            x1, y1 = self.filho_pos_nova
            x = x0 + (x1 - x0) * suavizar
            y = y0 + (y1 - y0) * suavizar
            filho.pos = (x, y)
            self.anim_frame += 1
            if self.anim_frame > self.anim_passos:
                valor = self.no_removido.valor
                
                # Atualiza as posições antigas antes da deleção
                if self._raiz:
                    self.atualizar_layout(
                        self._raiz,
                        self.largura / 2,
                        self.area_arvore_y + 50,
                        self.largura / 4
                    )
                    
                    # Impede movimento duplo do filho "promovido":
                    self.posicoes_antigas = {}
                    for no in self.iterar_nos(self._raiz):
                        if no is self.filho_remocao:
                            self.posicoes_antigas[no] = self.filho_pos_nova
                        else:
                            self.posicoes_antigas[no] = no.pos
                else:
                    self.posicoes_antigas = {}
                self.deletaNo(valor)
                # Captura as posições novas para animação global
                if self._raiz:
                    self.atualizar_layout(
                        self._raiz,
                        self.largura / 2,
                        self.area_arvore_y + 50,
                        self.largura / 4
                    )
                    self.posicoes_novas = {no: no.posicao_alvo for no in self.iterar_nos(self._raiz)}
                else:
                    self.posicoes_novas = {}
                self.anim_frame = 0
                self.animando = True
                self.atual_animacao = None
                self.filho_remocao = None
                self.filho_pos_antiga = None
                self.filho_pos_nova = None
            return

        # Fase 2: animação do restante da árvore (inserção ou remoção padrão)
        if self.animando:
            t = min(self.anim_frame / self.anim_passos, 1)
            for no in self.posicoes_novas:
                x0, y0 = self.posicoes_antigas.get(no, no.posicao_alvo)
                x1, y1 = self.posicoes_novas[no]
                no.pos = (
                    x0 + (x1 - x0) * t,
                    y0 + (y1 - y0) * t
                )
            self.anim_frame += 1
            if self.anim_frame > self.anim_passos:
                self.animando = False
                for no in self.posicoes_novas:
                    no.pos = no.posicao_alvo
                self.sucessor_remocao = None
                self.sucessor_pos_antiga = None
                self.sucessor_pos_alvo = None
                self.no_removido = None
            return

        if self._raiz:
            self.atualizar_layout(
                self._raiz,
                self.largura / 2,
                self.area_arvore_y + 50,
                self.largura / 4
            )

        if not self.atual_animacao and self.fila_animacoes:
            self.atual_animacao = self.fila_animacoes.popleft()
            self.progresso_animacoes = 0

        if self.atual_animacao:
            entry = self.atual_animacao
            tipo_acao = entry[0]
            nodo = entry[1] if len(entry) > 1 else None

            if tipo_acao in ("visitar", "encontrar"):
                self.progresso_animacoes += 0.03 * self.velocidade_animacoes
                if self.progresso_animacoes >= 1:
                    if tipo_acao == "encontrar" and nodo:
                        self.no_destacado = {nodo}
                        self.no_encontrado = nodo
                    else:
                        self.no_destacado = {nodo}
                    self.atual_animacao = None

            elif tipo_acao == "mover_sucessor" and self.sucessor_remocao:
                self.no_destacado = {self.sucessor_remocao}
                self.animando_sucessor = True
                self.anim_frame = 0
                self.atual_animacao = None

            elif tipo_acao == "rotacionar":
                self.progresso_animacoes += 0.01 * self.velocidade_animacoes
                if self.progresso_animacoes >= 1:
                    self.atual_animacao = None

            return

        if self._raiz:
            self.animar_nos(self._raiz)

# Método para buscar o sucessor do nó a ser removido ------------------------------------------------------------------------

    def animar_busca_sucessor(self, node_removido):
        """
        Retorna uma sequência de animações destacando o nó a ser removido
        e o caminho na subárvore direita até o sucessor.
        """
        fila = []
        # Primeiro destaca o nó a ser removido
        fila.append(("visitar", node_removido))
        atual = node_removido.direita
        if not atual:
            return fila
        # Percorre da direita até o sucessor
        while atual:
            fila.append(("visitar", atual))
            if atual.esquerda:
                atual = atual.esquerda
            else:
                break
        fila.append(("encontrar", atual))  # Marca como encontrado
        return fila
    
# Método para animar os nós -------------------------------------------------------------------------------------------------
    
    def animar_nos(self, no):
        
        if not no:
            return
        
        if no.pos != no.posicao_alvo:
            self.animar_movimento_no(no, self.progresso_animacoes)
            
        self.animar_nos(no.esquerda)
        self.animar_nos(no.direita)
        
# Método para desenhar linhas entre os nós ----------------------------------------------------------------------------------
        
    def desenha_aresta(self, paiNode, node):
        
        if self.animando_sucessor and node == self.sucessor_remocao:
            # Quando a animação da substituição do nó removido pelo sucessor está sendo feita a aresta não é desenhada
            return
    
        x1, y1 = paiNode.pos[0] + self.offset_x, paiNode.pos[1] + self.offset_y
        x2, y2 = node.pos[0] + self.offset_x, node.pos[1] + self.offset_y

        # Ângulo da linha
        angle = math.atan2(y2 - y1, x2 - x1)

        # Ponto inicial e final da linha (com margem no círculo)
        start = (x1 + math.cos(angle) * self.raio_no, y1 + math.sin(angle) * self.raio_no)
        end = (x2 - math.cos(angle) * self.raio_no, y2 - math.sin(angle) * self.raio_no)

        # Desenha a linha principal
        pygame.draw.line(self.tela, self.paleta["line"], start, end, 3)
        
# Método para mostrar instruções --------------------------------------------------------------------------------------------

    def desenhar_instrucoes(self):

        # Cria uma superfície semi-transparente
        instrucoes_surface = pygame.Surface((250, 200), pygame.SRCALPHA)
        instrucoes_surface.fill((0, 0, 0, 100)) # Quarto parâmetro é para ajustar a opacidade
    
        # Renderiza cada linha de instrução
        y_offset = 10
        for i, texto in enumerate(self.instrucoes):
            cor = (240, 240, 240) if i == 0 else (200, 200, 200)
            texto_surf = self.fonte.render(texto, True, cor)
            instrucoes_surface.blit(texto_surf, (10, y_offset))
            y_offset += 20
    
        self.tela.blit(instrucoes_surface, (20, self.altura - 210))

# Método para desenhar a árvore ---------------------------------------------------------------------------------------------

    def desenhar_arvore(self, no, no_destaque=None):
        
        if not no:
            return
        
        pos_no = (no.pos[0] + self.offset_x, no.pos[1] + self.offset_y)
        
        # Ligações
        if no.esquerda:
            self.desenha_aresta(no, no.esquerda)
            
        if no.direita:
            if not (self.animando_sucessor and no == self.sucessor_remocao and getattr(self, "sucessor_antigo_filho_direita", None) == no.direita):
                self.desenha_aresta(no, no.direita)
            
        self.desenhar_arvore(no.esquerda, no_destaque)
        self.desenhar_arvore(no.direita, no_destaque)
        
        # Desenha o nó
        # Verifica se o nó está dentro da área visível
        if no == self.no_encontrado and no in self.no_destacado:
            cor = self.paleta["no_buscado"]
        elif no == no_destaque:
            cor = self.paleta["no_destacado"]
        else:
            cor = self.paleta["no"]
        
        pygame.draw.circle(self.tela, cor, pos_no, self.raio_no)
        pygame.draw.circle(self.tela, self.paleta["borda"], pos_no, self.raio_no, 3)
        
        texto_valor = self.fonte.render(str(no.valor), True, self.paleta["text"] )
        retangulo_valor = texto_valor.get_rect(center=pos_no)
        self.tela.blit(texto_valor, retangulo_valor)
        
        if not self.no_removido or no != self.no_removido:
            texto_FB = self.fonte_menor.render(f"FB = {no.fatorBalanceamento()}", True, (80, 80, 100))
            retangulo_altura = texto_FB.get_rect(center=(pos_no[0], pos_no[1] + self.raio_no + 15))
            self.tela.blit(texto_FB, retangulo_altura)
        
# Método para desenhar a interface ------------------------------------------------------------------------------------------

    def desenhar_interface(self):
        # Desenha aba superior escura
        pygame.draw.rect(self.tela, self.paleta["borda"], self.aba_superior)
        
        # Desenha campo de input
        pygame.draw.rect(self.tela, self.paleta["input_background"], self.campo_input, border_radius=5)
        pygame.draw.rect(self.tela, self.paleta["borda"], self.campo_input, 2, border_radius=5)
        
        pygame.draw.rect(self.tela, self.paleta["input_background"], self.campo_output, border_radius=5)
        
        texto_input = self.fonte_maior.render(self.input_texto, True, self.paleta["text"])
        self.tela.blit(texto_input, (self.campo_input.x + 10, self.campo_input.y + 5))
        
        if self.leitura and len(self.leitura) != 0:
            primeiroNum = self.leitura[0]
            
        if self.lendo and self.leitura:
            
            numero = self.leitura[self.leitura_index]
            
            if primeiroNum and primeiroNum == (int)(numero):
                self.count += 1
            
            if self.count > 32:
                self.lendo = False
                self.count = 0
            
            leitura_output = self.fonte_maior.render(str(numero), True, self.paleta["borda"])
            self.tela.blit(leitura_output, (self.campo_output.x + 10, self.campo_output.y + 5))

            # Blit passa o texto criado para a tela principal
        
        self.tela.blit(self.botao_insercao, self.retangulo_insercao)
        self.tela.blit(self.botao_remocao, self.retangulo_remocao)
        self.tela.blit(self.botao_busca, self.retangulo_busca)
        
# Método de execução --------------------------------------------------------------------------------------------------------

    def executar(self):
        
        clock = pygame.time.Clock() # Inicializa o clock, para regular frames posteriormente
        self.tempo_ultima_atualizacao = pygame.time.get_ticks()
        rodando = True
        
        while rodando:
            
            rodando = self.gerenciar_eventos() # Recebe false quando fecha a janela
            self.atualizar()
            
            self.tela.fill(self.paleta["background"] ) # Pinta a tela de branco
            
            # Desenhar área da árvore (com offset)
            if self._raiz:
                no_destaque = None
                if self.atual_animacao:
                    tipo_acao = self.atual_animacao[0]
                    if tipo_acao in ("visitar","rotacionar", "criar","encontrar"):
                        no_destaque = self.atual_animacao[1]
                        
                self.desenhar_arvore(self._raiz, no_destaque)
                
            self.atualizar_leitura()
            self.desenhar_interface()
            self.desenhar_instrucoes()
            
            pygame.display.flip()
            clock.tick(60) # 60 FPS
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    visualizador = Visualizador()
    visualizador.executar()

