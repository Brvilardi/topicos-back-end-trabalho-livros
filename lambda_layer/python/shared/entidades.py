import json

class Produto:
    nome: str
    id: str

    def __init__(self, nome, id):
        self.nome = nome
        self.id = id

    def to_dict(self):
        return {
            'nome': self.nome,
            'id': self.id
        }

    @staticmethod
    def from_dict(source):
        return Produto(source[u'nome'], source[u'id'])
        
    
    @staticmethod
    def from_json(source):
        dic = json.loads(source)
        return Produto.from_dict(dic)


class Feedback:
    id: str
    produto: Produto
    comentario: str
    classificacao: float

    def __init__(self, id, produto, comentario, classificacao):
        self.id = id
        self.produto = produto
        self.comentario = comentario
        self.classificacao = classificacao

    def to_dict(self):
        return {
            'id': self.id,
            'produto': self.produto.to_dict(),
            'comentario': self.comentario,
            'classificacao': self.classificacao
        }
    
    @staticmethod
    def from_dict(source):
        return Feedback(
            produto=Produto.from_dict(source['produto']), 
            id=source["id"], 
            comentario=source['comentario'], 
            classificacao=source['classificacao'])
    
    @staticmethod
    def from_json(source):
        dic = json.loads(source)
        return Feedback.from_dict(dic)
    
