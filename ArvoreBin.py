from ArvoreProjeto import No

class ArvoreBin:
    
    def __init__(self):
        self._raiz = None
        
    # ----------------------------------------------------------------------    
        
    def menorValor(self, node):
        
        atual = node
        while atual and atual.esquerda is not None:
            atual = atual.esquerda
            
        return atual
    
    # ----------------------------------------------------------------------    
        
    def _insere_rec(self, node, num):
        
        if node is None:
            return No(num)
            
        if num > node.valor:
            node.direita = self._insere_rec(node.direita, num)
            
        elif num < node.valor:
            node.esquerda = self._insere_rec(node.esquerda, num)
            
        return node
    
    # ----------------------------------------------------------------------    
        
    def _deleta_rec(self, node, num):
        
        if node is None:
            return None
            
        if num < node.valor:
            node.esquerda = self._deleta_rec(node.esquerda, num)
            
        elif num > node.valor:
            node.direita = self._deleta_rec(node.direita, num)
            
        else:
            if node.esquerda is None:
                return node.direita
            
            elif node.direita is None:
                return node.esquerda
            
            else:
                temp = self.menorValor(node.direita)
                
                node.valor = temp.valor
                
                node.direita = self._deleta_rec(node.direita, temp.valor)
                
        return node
    
    # ----------------------------------------------------------------------        
            
    def _busca_bin_rec(self, node, num):
        
        if node is None:
            return None
        
        if num > node.valor:
            return self._busca_bin_rec(node.direita, num)
        
        elif num < node.valor:
            return self._busca_bin_rec(node.esquerda, num)
        
        return node
    
        # ----------------------------------------------------------------------
    
    def _em_ordem_rec(self, node):
        
        if node is not None:
            self._em_ordem_rec(node.esquerda)
            print(node)
            self._em_ordem_rec(node.direita)
            
    # ----------------------------------------------------------------------
            
    def _pre_ordem_rec(self, node):
        
        if node is not None:
            print(node)
            self._pre_ordem_rec(node.esquerda)
            self._pre_ordem_rec(node.direita)
            
    # ----------------------------------------------------------------------
            
    def _pos_ordem_rec(self, node):
        
        if node is not None:
            self._pos_ordem_rec(node.esquerda)
            self._pos_ordem_rec(node.direita)
            print(node)
            
    # ----------------------------------------------------------------------
    
    def insereNo(self, num):
        if isinstance(num, int):
            self._raiz = self._insere_rec(self._raiz, num)
            
    # ----------------------------------------------------------------------
    
    def deletaNo(self, num):
        if isinstance(num, int):
            self._raiz = self._deleta_rec(self._raiz, num)
    
    # ----------------------------------------------------------------------    
        
    def buscaBin(self, num):
        if isinstance(num, int):
            return self._busca_bin_rec(self._raiz, num)
        
    # ----------------------------------------------------------------------    
        
    def emOrdem(self):
        self._em_ordem_rec(self._raiz)
        
    # ----------------------------------------------------------------------    
        
    def preOrdem(self):
        self._pre_ordem_rec(self._raiz)
        
    # ----------------------------------------------------------------------    
        
    def posOrdem(self):
        self._pos_ordem_rec(self._raiz)
