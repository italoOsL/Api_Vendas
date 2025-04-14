from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProdutoViewSet, UnidadeMedidaViewSet, VendaViewSet, LojaViewSet, DashboardView

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'unidadesmedidas', UnidadeMedidaViewSet)
router.register(r'vendas', VendaViewSet)
router.register(r'lojas', LojaViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('relatorios/dashboard/', DashboardView.as_view()),
]