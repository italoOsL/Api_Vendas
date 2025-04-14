from django.shortcuts import render
from .models import Cliente, Produto, UnidadeMedida, Venda, Loja
from .serializers import ClienteSerializer, ProdutoSerializer, UnidadeMedidaSerializer, VendaSerializer, LojaSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from core.permissions import IsAdmin, IsUserPro, IsUserDefault, IsAdminOrUserPro
from core.dashboard import (
    grafico_faturamento_por_produto,
    grafico_qtd_valor_cliente,
    grafico_vendas_por_loja_periodo
)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAdminOrUserPro]
    
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsUserDefault]
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "Apenas admins!"}, status=403)
        return super().destroy(request, *args, **kwargs)
    
    
class UnidadeMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadeMedida.objects.all()
    serializer_class = UnidadeMedidaSerializer
    permission_classes = [IsUserPro]
    
class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all().prefetch_related('itens')
    serializer_class = VendaSerializer
    permission_classes = [IsAdminOrUserPro]
    
class LojaViewSet(viewsets.ModelViewSet):
    queryset = Loja.objects.all()
    serializer_class = LojaSerializer
    permission_classes = [IsAdminOrUserPro]
    
class DashboardView(APIView):
    permission_classes = [IsAdminOrUserPro]

    def get(self, request):
        fig1 = grafico_faturamento_por_produto()
        fig2 = grafico_qtd_valor_cliente()
        fig3 = grafico_vendas_por_loja_periodo()

        html1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')
        html2 = fig2.to_html(full_html=False, include_plotlyjs=False)
        html3 = fig3.to_html(full_html=False, include_plotlyjs=False)

        html_final = f"""
        <html>
        <head><title>Dashboard</title></head>
        <body>
            <h1 style="text-align:center;">📊 Dashboard de Vendas 📊</h1>
            {html1}<hr>
            {html2}<hr>
            {html3}<hr>

        </body>
        </html>
        """
        return HttpResponse(html_final)