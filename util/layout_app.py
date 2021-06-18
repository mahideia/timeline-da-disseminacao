import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


texto_p = """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's
   standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."""

titulo_do_trabalho = "A linha do tempo da estratégia federal de disseminação da covid-19"

subtitulo_pagina  = """Dados retirados do documento A LINHA DO TEMPO DA ESTRATÉGIA FEDERAL DE DISSEMINAÇÃO DA COVID-19
                    desenvolvido pelo Centro de Estudos e Pesquisas de Direito Sanitário (CEPEDISA - USP)
                    enviado à CPI da Pandemia do Senado Federal.
                    """

nome_dash = "A timeline da morte"

texto_cal = """ Para ver mais sobre as ações cometidas pelo governo federal em um dia específico basta selecioná-lo no calendário, a descrição aparecerá logo abaixo dele.
    Para uma lista completa de ações basta acessar o [trabalho original](https://cepedisa.org.br/wp-content/uploads/2021/06/CEPEDISA-USP-Linha-do-Tempo-Maio-2021_v3.pdf).
    """#\nUma descrição específica das ações no dia selecionado será apresentada logo abaixo."""



titulo_sobre = """ """


def defineLayout(conteudo):

    navbar = dbc.NavbarSimple(
        children=[
            #dbc.DropdownMenu(
            #    children=[
            #        dbc.DropdownMenuItem("Mais", header=True),
            #        dbc.DropdownMenuItem("Sobre a pesquisa", href="/apps/pesquisa"),
            #        dbc.DropdownMenuItem("Sobre esse dash", href="/apps/sobre"),
            #    ],
            #    nav=True,
            #    in_navbar=True,
            #    label="More",
            #),
        ],
        brand=nome_dash,
        brand_href="#",
        color="dark",
        dark=True,
        className='navbar fixed-top'
    )



    rodape = dbc.NavbarSimple(
        children=[html.Div(dcc.Markdown("""Esse é um dash desenvolvido (às pressas) por [Marina M. Mendonça.](https://linktr.ee/mahideia)"""))],
        brand_href="#",
        color="dark",
        dark=True,
        className='navbar bottom'
    )

    titulo = html.Div([html.H2(titulo_do_trabalho,style={'padding-top':'100px','padding-bottom':'10px'}),
        #html.P(subtitulo_pagina,
        #   style={'padding-top':'0px','padding-bottom':'40px','padding-left':'25px','padding-right':'25px'}),
           dcc.Markdown(subtitulo_pagina + texto_cal,style={'padding-top':'0px','padding-bottom':'40px','padding-left':'25px','padding-right':'25px'})])

    layout = html.Div([navbar,
                      html.Div([
                            html.Div(titulo,className='container'),
                            html.Div(conteudo,className='container'),
                      ],className='container'),
                      rodape])
    return layout
