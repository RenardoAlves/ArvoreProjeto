from No import No

class NoAVL(No):
    
    def __init__(self, valor = None):
        super().__init__(valor)
        self.__altura = 0
        
    # GETTERS ----------------------------------------------------------------
    
    @property
    def altura(self):
        return self.__altura
        
    # SETTER ----------------------------------------------------------------
    
    @altura.setter
    def altura(self, valor):
        self.__altura = valor
        
    # ------------------------------------------------------------------------

    def atualizaAltura(self):
        alturaESQ = self.esquerda.altura if self.esquerda else -1
        alturaDIR = self.direita.altura if self.direita else -1
        self.altura = max(alturaESQ, alturaDIR) + 1

    def fatorBalanceamento(self):
        alturaESQ = self.esquerda.altura if self.esquerda else -1
        alturaDIR = self.direita.altura if self.direita else -1
        return alturaDIR - alturaESQ

    # ------------------------------------------------------------------------

    def rotacionaDireita(self):
        novaRaiz = self.esquerda
        self.esquerda = novaRaiz.direita
        novaRaiz.direita = self
        
        if self.esquerda:
            self.esquerda.pai = self
            
        novaRaiz.pai = self.pai
        self.pai = novaRaiz
        
        self.atualizaAltura()
        novaRaiz.atualizaAltura()
        
        return novaRaiz

    # ------------------------------------------------------------------------

    def rotacionaEsquerda(self):
        novaRaiz = self.direita
        self.direita = novaRaiz.esquerda
        novaRaiz.esquerda = self
        
        if self.direita:
            self.direita.pai = self
            
        novaRaiz.pai = self.pai
        self.pai = novaRaiz

        self.atualizaAltura()
        novaRaiz.atualizaAltura()
        
        return novaRaiz