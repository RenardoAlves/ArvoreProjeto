from ArvoreBin import ArvoreBin
from NoAVL import NoAVL

class ArvoreAVL(ArvoreBin):
    
    def __init__(self):
        super().__init__()
    
    # ------------------------------------------------------------------------
    
    def _insere_rec(self, node, valor):

        if node is not None and node.valor is not None:
            self.historico.append(("visitar", node))
            
        if node is None or node.valor is None:
            
            novo_no = NoAVL(valor)
            self.historico.append(("inserir", novo_no))
            return novo_no
            
        if valor < node.valor:
            
            node.esquerda = self._insere_rec(node.esquerda, valor)
            
            if node.esquerda:
                node.esquerda.pai = node
                
        elif valor > node.valor:
            
            node.direita = self._insere_rec(node.direita, valor)
            
            if node.direita:
                node.direita.pai = node
                
        else:
            return node
            
        node.atualizaAltura()
        
        return self._balancear(node)
    
    # ------------------------------------------------------------------------
    
    def _deleta_rec(self, node, valor):
        
        node = super()._deleta_rec(node, valor)
        
        if node is None or node.valor is None:
            return None
            
        node.atualizaAltura()
        
        return self._balancear(node)
    
    # ------------------------------------------------------------------------
    
    def _balancear(self, node):
        
        fb = node.fatorBalanceamento()
        
        if fb < -1:
            
            if node.esquerda.fatorBalanceamento() <= 0:
                self.historico.append(("rotacionar", node, "direita"))
                return node.rotacionaDireita()
            else:
                self.historico.append(("rotacionar", node, "esquerda-direita"))
                node.esquerda = node.esquerda.rotacionaEsquerda()
                return node.rotacionaDireita()
                
        elif fb > 1:
            
            if node.direita.fatorBalanceamento() >= 0:
                self.historico.append(("rotacionar", node, "esquerda"))
                return node.rotacionaEsquerda()
            else:
                self.historico.append(("rotacionar", node, "direita-esquerda"))
                node.direita = node.direita.rotacionaDireita()
                return node.rotacionaEsquerda()
                
        return node
    
    # ------------------------------------------------------------------------
    
    def insereNo(self, valor):
        if isinstance(valor, int):
            self.historico = []
            self._raiz = self._insere_rec(self._raiz, valor)
    
    # ------------------------------------------------------------------------
    
    def deletaNo(self, valor):
        if isinstance(valor, int):
            self.historico = []
            self._raiz = self._deleta_rec(self._raiz, valor)

    # ----------------------------------------------------------------------    