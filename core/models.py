from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=255) # NOTNULL
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    
class UnidadeMedida(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    descricao = models.CharField(max_length=50)
    
class Produto(models.Model):
    nome = models.CharField(max_length=255) # NOTNULL
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    unidade = models.CharField(max_length=3)
    qtd_estoque = models.IntegerField()
    
class Loja(models.Model):
    nome = models.CharField(max_length=50)
    endereco = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    
class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    loja = models.ForeignKey(Loja, on_delete=models.PROTECT)
    data_venda = models.DateField()
    vendedor = models.CharField(max_length=50)
    
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    

