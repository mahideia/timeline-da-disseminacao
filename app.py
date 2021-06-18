import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

import util.layout_app as la
import util.graficos as gr
import util.texto as txt

dados=gr.carregaDados()

texto_sobre = """ O conteúdo aqui apresentado é uma tentativa de disseminar a informação com gráficos. Todos os textos referentes a atos normativos, atos de governo e propaganda,
    foram retirados diretamente do PDF do relatório. Isso significa que se algo não tá batendo com o documento, bem, a culpa é minha. Podem ter dias trocados, podem ter espaços
    em lugares errados (tipo no meio de links), podem ter outas confusões textuais que derivam do trabalho manual de extrair dados dum pdf na mão(*).

    O desenvolvimento foi todo meu, usando Dash (usem o dash!). E como foi feito no meu tempo 'livre' é possível que tenha uma série de errinhos perdidos.
    Não tenho vínculo algum com o CEPEDISA, o grupo que desenvolveu o relatório ou a USP (dela, só saudades).
    """

texto_acao = """ #### Ações do dia selecionado\nAo clicar em um dia no calendário você poderá ver neste espaço a lista de ações cometidas."""

card_barras = dbc.Card([
                dbc.CardHeader(html.H5("Tipos de ações")),
                dbc.CardBody([
                #dcc.Markdown(texto_cal),
                    dcc.Graph(id='tipos-de-acoes',figure=gr.plotaTiposAcoes(dados),config = {'displayModeBar': False}),
                ]),
                dbc.CardFooter(dcc.Markdown(id='descricao-tipo',children=''))
                ])

card_calendario = dbc.Card([
                    dbc.CardHeader(html.H5("Timeline de ações")),
                    dbc.CardBody([
                        #dcc.Markdown(texto_cal),
                        dcc.Graph(id='timeline-da-morte',figure=gr.plotaCalendario(dados),config = {'displayModeBar': False})
                    ]),
                    dbc.CardFooter(dcc.Markdown(id='descricao-acao',children='',dangerously_allow_html=True))
                    ])

card_semana = dbc.Card([
                dbc.CardHeader(html.H5("Produtividade na semana")),
                dbc.CardBody([
                #dcc.Markdown(texto_cal),
                    dcc.Graph(id='produtividade-semana',figure=gr.plotaQtdSemana(dados),config = {'displayModeBar': False}),
                ]),
                dbc.CardFooter(dcc.Markdown(id='descricao-semana',children='Toda quinta-feira Bolsonaro faz uma live no facebook e youtube onde fala livremente sobre o que achar conveniente.'))
                ])

card_texto = dbc.Card([
                dbc.CardHeader(html.H5("Sobre esse dashboard")),
                dbc.CardBody([
                dcc.Markdown(texto_sobre),
                ]),
                dbc.CardFooter(dcc.Markdown(id='texto-sobre',children='Sintam-se a vontade para enviar email com sugestões, críticas e apontamento de erros no ma.monteiro.m [a] gmail.'))
                ])

conteudo= html.Div([
            html.Div([
                html.Div(card_calendario,className='col-lg-12'),
            ],className='row'),
            html.Div([
                html.Div(card_barras,className='col-lg-6'),
                html.Div(card_semana,className='col-lg-6')
            ],className='row'),
            html.Div([
                html.Div(card_texto,className='col-lg-12'),
            ],className='row'),
        ])



app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])

app.layout =  la.defineLayout(conteudo)

server = app.server

@app.callback(
    Output('descricao-acao','children'),
    Input('timeline-da-morte','clickData')
)
def updateDescricaoAcao(clickdata):
    texto=texto_acao
    if clickdata:
        texto = txt.markdownAcao(clickdata['points'][0]['text'],dados)
    return texto

@app.callback(
    Output('descricao-tipo','children'),
    Input('tipos-de-acoes','clickData')
)
def updateDescricaoTipo(clickdata):
    texto="Selecione um dos tipos no gráfico para saber mais."
    if clickdata:
        texto = txt.markdownTipo(clickdata['points'][0]['y'])
    return texto

app.title="A timeline da morte do Brasil"
if __name__ == '__main__':
    app.run_server(debug=False)
