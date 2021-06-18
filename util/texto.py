import pandas as pd
import random
import numpy as np

textos = ["""Parece que esse foi um dia tranquilo e o governo Bolsonaro não trabalhou para a disseminação do vírus.""",
         """Apesar de levar muito a sério seu plano, esse não foi um dia de grandes ações públicas para louvar o SARSCov2""",
         """Acredite se quiser, nenhum trabalho pela piora da pandemia foi registrado para este dia""",
         """Bolsonaro estava ocupado com outras tarefas, o agravamento da maior crise sanitária dos últimos 100 anos não acelerada hoje"""]


def markdownAcao(data,df):
    x = data
    x=x[6:10]+'-'+x[3:5]+'-'+x[:2]
    dados = df[df.data==x]

    if pd.to_datetime(x)<=pd.to_datetime('2020-01-02') or pd.to_datetime(x)>pd.to_datetime('30-05-2021'):
        texto=f""" ### {data} \n Sem registros para essa data."""
    else:
        if len(dados)==0:
            paragrafo = random.choice(textos)
            texto = f""" ### {data} \n {paragrafo}"""
        else:
            texto = f""" ### {data} \n"""
            refs = f"\n#### Referências\n"
            for index, row in dados.iterrows():
                texto = texto + f"#### {row['tipo']}\n {row['num']}. {row['texto']} \n"
                if len(row.refs)>0:
                    refs = refs+row['refs']
            if refs!=f"\n#### Referências\n":texto = texto + refs
    return texto

def markdownTipo(tipo):
    if tipo =='Atos normativos':
        texto = """__Atos normativos__ adotados na esfera da União, incluindo a edição
                    de normas por autoridades e órgãos federais, e vetos presidenciais;"""
    elif tipo =='Atos de governo':
        texto = """__Atos de governo__, que correspondem a _ações de obstrução_ de
            medidas de contenção da doença, adotadas principalmente por
            governos estaduais e municipais, a _omissões_ relativas à gestão da
            pandemia no âmbito federal, além de _outros elementos_ que
            permitam compreender e contextualizar atos e omissões
            governamentais;"""
    elif tipo =='Propaganda':
        texto = """__Propaganda__ contra a saúde pública, aqui definida como o
                discurso político que mobiliza argumentos econômicos,
                ideológicos e morais, além de notícias falsas e informações
                técnicas sem comprovação científica, com o propósito de
                desacreditar as autoridades sanitárias, enfraquecer a adesão
                popular a recomendações de saúde baseadas em evidências
                científicas, e promover o ativismo político contra as medidas de
                saúde pública necessárias para conter o avanço da Covid-19."""
    else:
        texto = "Selecione um dos tipos no gráfico para saber mais"
    return texto
