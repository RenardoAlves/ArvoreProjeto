from ArvoreProjeto import ArvoreBin, NoAVL

class ArvoreAVL(ArvoreBin):
    
    def __init__(self):
        super().__init__()
    
    # ----------------------------------------------------------------------
    
    def _insere_rec(self, node, valor):
        
        if node is None:
            return NoAVL(valor)
            
        if valor < node.valor:
            node.esquerda = self._insere_rec(node.esquerda, valor)
            node.esquerda.pai = node
            
        elif valor > node.valor:
            node.direita = self._insere_rec(node.direita, valor)
            node.direita.pai = node
            
        else:
            return node
            
        node.atualizaAltura()
        return self._balancear(node)
    
    # ----------------------------------------------------------------------
    
    def _deleta_rec(self, node, valor):
        
        node = super()._deleta_rec(node, valor)
        
        if node is None:
            return None
            
        node.atualizaAltura()
        return self._balancear(node)
    
    # ----------------------------------------------------------------------
    
    def _balancear(self, node):
        
        fb = node.fatorBalanceamento()
        
        if fb < -1 and node.esquerda.fatorBalanceamento() <= 0:
            return node.rotacionaDireita()
            
        if fb < -1 and node.esquerda.fatorBalanceamento() > 0:
            node.esquerda = node.esquerda.rotacionaEsquerda()
            return node.rotacionaDireita()
            
        if fb > 1 and node.direita.fatorBalanceamento() >= 0:
            return node.rotacionaEsquerda()
            
        if fb > 1 and node.direita.fatorBalanceamento() < 0:
            node.direita = node.direita.rotacionaDireita()
            return node.rotacionaEsquerda()
            
        return node
    
    # ----------------------------------------------------------------------
    
    def insereNo(self, valor):
        if isinstance(valor, int):
            self._raiz = self._insere_rec(self._raiz, valor)
    
    # ----------------------------------------------------------------------
    
    def deletaNo(self, valor):
        if isinstance(valor, int):
            self._raiz = self._deleta_rec(self._raiz, valor)