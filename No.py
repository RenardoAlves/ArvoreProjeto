class No:
    
    def __init__(self, valor = None):

        self.__pai = None
        self.__esquerda = None
        self.__direita = None
        self.valor = valor
            
    # ----------------------------------------------------------------------
    
    def copiaNo(self, node):
        
        if(isinstance(node, No)):

            self.__pai = node.__pai
            self.__esquerda = node.__esquerda
            self.__direita = node.__direita
            self.__valor = node.__valor
    
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

    # SETTERS --------------------------------------------------------------

    @pai.setter
    def pai(self, node):
        if(isinstance(node, No)):
            self.__pai = node
    
    @esquerda.setter
    def esquerda(self, node):
        if(isinstance(node, No)):
            self.__esquerda = node
            
    @direita.setter
    def direita(self, node):
        if(isinstance(node, No)):
            self.__direita = node

    @valor.setter
    def valor(self, num):
        
        if(isinstance(num, int) or num is None):
            self.__valor = num
            
    # ----------------------------------------------------------------------
    
    def __str__(self):
        return f'{self.valor}'   