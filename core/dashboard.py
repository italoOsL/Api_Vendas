import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from django.db import connection
from plotly.subplots import make_subplots

def grafico_faturamento_por_produto():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.nome, SUM(iv.quantidade * iv.valor_unitario) AS total
            FROM core_itemvenda iv
            JOIN core_produto p ON iv.produto_id = p.id
            GROUP BY p.nome
            ORDER BY total DESC
        """)
        dados = cursor.fetchall()
    df = pd.DataFrame(dados, columns=['produto', 'total'])

    fig = px.bar(df, x='produto', y='total', title='<b>Faturamento por Produto</b>')

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(t=50, b=120),
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    fig.update_yaxes(tickprefix='R$ ', showgrid=True)

    return fig

def grafico_qtd_valor_cliente():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.nome AS cliente,
                   COUNT(DISTINCT v.id) AS qtd_compras,
                   SUM(iv.quantidade * iv.valor_unitario) AS valor_total
              FROM core_venda v
        INNER JOIN core_cliente c ON v.cliente_id = c.id
        INNER JOIN core_itemvenda iv ON iv.venda_id = v.id
        GROUP BY c.nome
        ORDER BY valor_total DESC;
        """)
        dados = cursor.fetchall()

    df = pd.DataFrame(dados, columns=["cliente", "qtd_compras", "valor_total"])

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["cliente"],
        y=df["qtd_compras"],
        name="Compras Realizadas",
        marker_color="lightblue",
        hovertemplate="Cliente: %{x}<br>Compras: %{y}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=df["cliente"],
        y=df["valor_total"],
        name="Valor Total (R$)",
        marker_color="lightsalmon",
        hovertemplate="Cliente: %{x}<br>R$: %{y:.2f}<extra></extra>"
    ))

    fig.update_layout(
        title="<b>Compras por Cliente: Quantidade e Valor Total</b>",
        barmode="group",
        xaxis_tickangle=-45,
        height=500,
        margin=dict(t=60, b=120),
        legend=dict(x=0.8, y=1.1),
        xaxis_title='',
        yaxis_title=''
    )

    # path = "core/static/cliente_compras_valor.html"
    # fig.write_html(path, include_plotlyjs='cdn')
    return fig

def grafico_distribuicao_clientes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.nome,
                   SUM(iv.quantidade) AS quantidade,
                   SUM(iv.quantidade * iv.valor_unitario) AS total
              FROM core_venda v
        JOIN core_cliente c ON v.cliente_id = c.id
        JOIN core_itemvenda iv ON iv.venda_id = v.id
        GROUP BY c.nome;
        """)
        dados = cursor.fetchall()

    df = pd.DataFrame(dados, columns=['cliente', 'quantidade', 'total'])

    df['ticket_medio'] = df.apply(
        lambda row: row['total'] / row['quantidade'] if row['quantidade'] else 0,
        axis=1
    )

    fig = px.scatter(
        df,
        x='quantidade',
        y='total',
        text='cliente',
        size='ticket_medio',
        color='ticket_medio',
        color_continuous_scale='RdBu',
        title='<b>Distribuição de Clientes: Engajamento x Valor</b>',
        labels={
            'quantidade': 'Qtd. Comprada',
            'total': 'Valor Total (R$)',
            'ticket_medio': 'Ticket Médio'
        },
        hover_data={
            'cliente': True,
            'quantidade': True,
            'total': ':.2f',
            'ticket_medio': ':.2f'
        }
    )

    fig.update_layout(margin=dict(t=60, b=60), height=500)

    return fig

def grafico_vendas_por_loja_periodo():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT l.nome, SUM(iv.quantidade * iv.valor_unitario) AS total
              FROM core_venda v
              JOIN core_loja l ON v.loja_id = l.id
              JOIN core_itemvenda iv ON iv.venda_id = v.id
             WHERE v.data_venda BETWEEN '2025-04-01' AND '2025-04-10'
          GROUP BY l.nome
          ORDER BY total DESC;
        """)
        dados = cursor.fetchall()

    df = pd.DataFrame(dados, columns=['loja', 'total'])
    return px.pie(df, names='loja', values='total', title='<b>Faturamento por Loja (Período)</b>')