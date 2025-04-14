from rest_framework import serializers
from .models import Cliente, Produto, UnidadeMedida, Venda, ItemVenda, Loja

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        
class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeMedida
        fields = '__all__'
        
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
        
class LojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loja
        fields = '__all__'
        
class ItemVendaSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)

    class Meta:
        model = ItemVenda
        exclude = ['venda']
        
class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True)

    class Meta:
        model = Venda
        fields = ['id', 'cliente', 'loja', 'data_venda', 'vendedor', 'itens']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        venda = Venda.objects.create(**validated_data)
        for item in itens_data:
            ItemVenda.objects.create(venda=venda, **item)
        return venda

    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if itens_data is not None:
            instance.itens.all().delete()
            for item in itens_data:
                ItemVenda.objects.create(venda=instance, **item)

        return instance