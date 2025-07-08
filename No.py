class No:
    
    def __init__(self, valor = None):

        self.__pai = None
        self.__esquerda = None
        self.__direita = None
        self.__pos = [0, 0]
        self.__posicao_alvo = [0, 0]
        self.valor = valor

    # GETTERS --------------------------------------------------------------
    
    @property
    def pai(self):
        return self.__pai
    
    @property
    def esquerda(self):
        return self.__esquerda
    
    @property
    def direita(self):
        return self.__direita
    
    @property
    def valor(self):
        return self.__valor
    
    @property
    def pos(self):
        return self.__pos
        
    @property
    def posicao_alvo(self):
        return self.__posicao_alvo

    # SETTERS --------------------------------------------------------------

    @pai.setter
    def pai(self, node):
        if node is None or (isinstance(node, No)):
            self.__pai = node
    
    @esquerda.setter
    def esquerda(self, node):
        if node is None or (isinstance(node, No)):
            self.__esquerda = node
            
    @direita.setter
    def direita(self, node):
        if node is None or (isinstance(node, No)):
            self.__direita = node

    @valor.setter
    def valor(self, num):
        
        if(isinstance(num, int) or num is None):
            self.__valor = num
            
    @pos.setter
    def pos(self, value):
        self.__pos = value
        
    @posicao_alvo.setter
    def posicao_alvo(self, value):
        self.__posicao_alvo = value
            
    # ----------------------------------------------------------------------
    
    def __str__(self):
        return f'{self.valor}'   