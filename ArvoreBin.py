from No import No

class ArvoreBin:
    
    def __init__(self):
        self._raiz = None
        self.leitura = []
        self.historico = []
        
    # ----------------------------------------------------------------------

    def _em_ordem_rec(self, node):
        
        if node is not None and node.valor is not None:
            
            self._em_ordem_rec(node.esquerda)
            self.leitura.append(node.valor)
            self._em_ordem_rec(node.direita)
            
    # ----------------------------------------------------------------------
            
    def _pre_ordem_rec(self, node):
        
        if node is not None and node.valor is not None:
            self.leitura.append(node.valor)
            self._pre_ordem_rec(node.esquerda)
            self._pre_ordem_rec(node.direita)
            
    # ----------------------------------------------------------------------
            
    def _pos_ordem_rec(self, node):
        
        if node is not None and node.valor is not None:
            self._pos_ordem_rec(node.esquerda)
            self._pos_ordem_rec(node.direita)
            self.leitura.append(node.valor)
    
    # ----------------------------------------------------------------------    
        
    def emOrdem(self):
        self.leitura = []
        self._em_ordem_rec(self._raiz)
        
    # ----------------------------------------------------------------------    
        
    def preOrdem(self):
        self.leitura = []
        self._pre_ordem_rec(self._raiz)
        
    # ----------------------------------------------------------------------    
        
    def posOrdem(self):
        self.leitura = []
        self._pos_ordem_rec(self._raiz)    
    
    # ----------------------------------------------------------------------    
        
    def menorValor(self, node):
        
        atual = node
        while atual and atual.esquerda is not None:
            atual = atual.esquerda
            
        return atual
    
    # ----------------------------------------------------------------------   
    
    def _calcular_profundidade(self, no):
        profundidade = 0
        atual = no
        while atual.pai is not None:
            profundidade += 1
            atual = atual.pai
        return profundidade
    
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
        if node is None or node.valor is None:
            return None
        
        if num < node.valor:
            
            node.esquerda = self._deleta_rec(node.esquerda, num)
        elif num > node.valor:
            
            node.direita = self._deleta_rec(node.direita, num)
        else:
            
            if node.esquerda is None or node.esquerda.valor is None:
                
                node_removido = node.direita
                node.valor = None
                node.esquerda = node.direita = None
                return node_removido
            
            elif node.direita is None or node.direita.valor is None:
                
                node_removido = node.esquerda
                node.valor = None
                node.esquerda = node.direita = None
                return node_removido
            
            else:
                
                temp = self.menorValor(node.direita)
                node.valor = temp.valor
                node.direita = self._deleta_rec(node.direita, temp.valor)
                
        return node
    # ----------------------------------------------------------------------        
            
    def _busca_bin_rec(self, node, num):
        
        if node is None or node.valor is None:
            return None
        
        self.historico.append(("visitar", node))
        
        if num > node.valor:
            return self._busca_bin_rec(node.direita, num)
        
        elif num < node.valor:
            return self._busca_bin_rec(node.esquerda, num)
        
        self.historico.append(("encontrar", node))
        
        return node
    
    # ----------------------------------------------------------------------self.emOrdem()
    
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
