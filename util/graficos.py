import datetime
import plotly.graph_objs as go
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import dash
import pandas as pd
import numpy as np
#from pandas_ods_reader import read_ods
from plotly.subplots import make_subplots


def carregaDados():
    df = pd.read_csv('data/timeline.csv',delimiter='|')
    df.columns = ['data','tipo','num','texto','refs']
    #tem um "Atos de gestão" no documento, referente a ação numero 79 (06/07/2020), como tal categoria não está contemplada no documento tomei a liberdade de trocar para um ato de governo
    df.loc[df['tipo']=='Atos de gestão','tipo']='Atos de governo'
    df.loc[df['tipo']=='Atos de Governo','tipo']='Atos de governo'
    df.refs = df.refs.fillna('')
    return df

def preparaDadosGrafico(tipo,df):
    if tipo=='barras':
        dfbar = df.groupby(['tipo']).count().sort_values(by='num')
        return dfbar
    elif tipo=='calendario':
        df.data = pd.to_datetime(df.data,format="%Y-%m-%d")
        idx = pd.date_range("2020", freq="D", periods=731)
        z=df.resample('D',on='data').tipo.count().reindex(idx).fillna(0)
        return z
    elif tipo=='barras_semana':
        ds = pd.DataFrame(df.set_index(df.data).index.dayofweek.values,columns=['dia_semana'])
        ds['qtd']=1
        ds = ds.groupby(['dia_semana']).count()
        return ds
    else:
        return df

def plotaCalendario(dados):
    z = preparaDadosGrafico('calendario',dados)
    colorscale=[[False, '#eeeeee'], [True, '#7f124e']]
    fig = make_subplots(rows=2, cols=1)#vertical_spacing=

    i=1
    for year in [2020,2021]:
        d1 = datetime.date(year,1, 1)
        d2 = datetime.date(year,12,31)
        delta = d2 - d1

        dates_in_year = [d1 + datetime.timedelta(i) for i in range(delta.days+1)] #gives me a list with datetimes for each day a year
        weekdays_in_year = [i.weekday() for i in dates_in_year] #gives [0,1,2,3,4,5,6,0,1,2,3,4,5,6,…] (ticktext in xaxis dict translates this to weekdays
        weeknumber_of_dates = [i.strftime("%Gww%V")[2:] for i in dates_in_year] #gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,…] name is self-explanatory
        text = [i.strftime("%d/%m/%Y") for i in dates_in_year]
        fig.append_trace(
            go.Heatmap(
                x = weeknumber_of_dates,
                y = -np.array(weekdays_in_year),
                z = z[str(year)],
                text=text,
                hoverinfo="text",
                xgap=2, # this
                ygap=2, # and this is used to make the grid-like apperance
            showscale=False,
            colorscale=colorscale,
            ),row=i,col=1
        )
        i=i+1



    semanas2020 = ['20ww01','20ww05','20ww09','20ww14','20ww18','20ww23','20ww27','20ww31','20ww36','20ww40','20ww44','20ww49']
    semanas2021 = ['21ww01','21ww05','21ww09','21ww14','21ww18','21ww23','21ww27','21ww31','21ww36','21ww40','21ww44','21ww48']

    fig.update_layout(
        font={'size':10, 'color':'#9e9e9e'},
        plot_bgcolor=('#fff'),
        margin = dict(t=20,r=10,l=10,b=10),
        )
    fig.update_layout(clickmode='event+select')
    fig.update_yaxes(title='2020',row=1,col=1)
    fig.update_yaxes(title='2021',row=2,col=1)
    fig.update_yaxes(dict(
            title_font=dict(size=20,family='Raleway'),
            showline = False, showgrid = False, zeroline = False,
            tickmode="array",
            ticktext=["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"],
            tickvals=[0,-1,-2,-3,-4,-5,-6],
            ))
    fig.update_xaxes(dict(
            showline = False, showgrid = False, zeroline = False,
            tickmode="array",
            ticktext=["Janeiro","Fevereiro","Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro","Outubro","Novembro","Dezembro"],
            tickvals=semanas2020,
            ticklabelposition ="outside right",
            tickwidth=2,
            ),row=1,col=1)
    fig.update_xaxes(dict(
            showline = False, showgrid = False, zeroline = False,
            tickmode="array",
            ticktext=["Janeiro","Fevereiro","Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro","Outubro","Novembro","Dezembro"],
            tickvals=semanas2021,
            ticklabelposition ="outside right",
            tickwidth=2,
            ),row=2,col=1)

    return fig

def plotaTiposAcoes(dados):
    dfbar = preparaDadosGrafico('barras',dados)
    fig = go.Figure()
    fig.add_trace(go.Bar(y=dfbar.index,x=dfbar.num,
                    orientation = 'h',
                    marker=dict(color='#64113F',
                                line=dict(color='#64113F',width=1),),
                    ))
    config = {'displayModeBar': False} #isso tem que ir pro config do dcc.Graph
    fig.update_layout(clickmode='event+select')
    fig.update_layout(
            font={'size':12, 'color':'#9e9e9e'},
            plot_bgcolor=('#fff'),
            margin = dict(t=20,r=10,l=10,b=10),
            )
    fig.update_xaxes(tickfont=dict(size=12, family='Arial'))
    fig.update_yaxes(tickfont=dict(size=12))
    return fig

def plotaQtdSemana(dados):
    ds = preparaDadosGrafico('barras_semana',dados)
    semana = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=semana,y=ds.qtd,
                    orientation = 'v',
                    marker=dict(color='#64113F',
                                line=dict(color='#64113F',width=1),),
                    ))
    config = {'displayModeBar': False} #isso tem que ir pro config do dcc.Graph
    fig.update_layout(
            font={'size':12, 'color':'#9e9e9e'},
            plot_bgcolor=('#fff'),
            margin = dict(t=20,r=10,l=10,b=10),
            )
    fig.update_xaxes(tickfont=dict(size=12, family='Arial'))
    fig.update_yaxes(tickfont=dict(size=12))
    return fig
