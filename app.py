import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px
from load_css import local_css

st.set_page_config(page_title='Neobpo IN',
                    page_icon=':bar_chart',
                    layout='wide')

local_css("css/style.css")

start_date = st.sidebar.date_input("Data início", value=pd.to_datetime("2022-02-01", format="%Y-%m-%d"))
end_date = st.sidebar.date_input("Data Fim", value=pd.to_datetime("today", format="%Y-%m-%d"))


cboCoordenador = st.sidebar.multiselect(
    "Selecione o coordenador",
    options=["VERONICA SANTOS DE MORAES", "LUCAS  REZENDE"],
    default=["VERONICA SANTOS DE MORAES", "LUCAS  REZENDE"]
)

def notaQualidade():
    db_connection = psycopg2.connect(host='ec2-54-159-35-35.compute-1.amazonaws.com', database='d12bc1j5j4fl0k', user='gfkmakmpiswigi', password='f0c464f9d87f7803f3ce460a2e6b6b3db76f5f3a076ea4c04291dfc4c3f699a5', port='5432')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'''
        select 
            round(avg(replace(score, ',', '.')::numeric),2) as "Nota"
        from qualidade q 
    ''')
    result = db_cursor.fetchall()

    for row in result:
        result = row[0]

    db_connection.close()

    return result

def quantidadeMonitorias():
    db_connection = psycopg2.connect(host='ec2-54-159-35-35.compute-1.amazonaws.com', database='d12bc1j5j4fl0k', user='gfkmakmpiswigi', password='f0c464f9d87f7803f3ce460a2e6b6b3db76f5f3a076ea4c04291dfc4c3f699a5', port='5432')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'''
        select 
            count(score) as "Qtde"
        from qualidade q 
    ''')
    result = db_cursor.fetchall()

    for row in result:
        result = row[0]

    db_connection.close()

    return result

def ncgPercent():
    db_connection = psycopg2.connect(host='ec2-54-159-35-35.compute-1.amazonaws.com', database='d12bc1j5j4fl0k', user='gfkmakmpiswigi', password='f0c464f9d87f7803f3ce460a2e6b6b3db76f5f3a076ea4c04291dfc4c3f699a5', port='5432')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'''
        select 
            round(count(case when score  = '0' THEN 1 END)::numeric / count(*) * 100, 2)
        from qualidade q 
    ''')
    result = db_cursor.fetchall()

    for row in result:
        result = row[0]

    db_connection.close()

    return result

def noPrazoPercent():
    db_connection = psycopg2.connect(host='ec2-54-159-35-35.compute-1.amazonaws.com', database='d12bc1j5j4fl0k', user='gfkmakmpiswigi', password='f0c464f9d87f7803f3ce460a2e6b6b3db76f5f3a076ea4c04291dfc4c3f699a5', port='5432')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'''
        select 
            round(count(case when status  = 'No Prazo' THEN 1 END)::numeric / count(*) * 100, 2)
        from qualidade q 
    ''')
    result = db_cursor.fetchall()

    for row in result:
        result = row[0]

    db_connection.close()

    return result

def foraDoPrazoPercent():
    db_connection = psycopg2.connect(host='ec2-54-159-35-35.compute-1.amazonaws.com', database='d12bc1j5j4fl0k', user='gfkmakmpiswigi', password='f0c464f9d87f7803f3ce460a2e6b6b3db76f5f3a076ea4c04291dfc4c3f699a5', port='5432')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'''
        select 
            round(count(case when status  = 'Fora do Prazo' THEN 1 END)::numeric / count(*) * 100, 2)
        from qualidade q 
    ''')
    result = db_cursor.fetchall()

    for row in result:
        result = row[0]

    db_connection.close()

    return result    

def dataFrameSupervisor():
    db_connection = psycopg2.connect(host='ec2-54-159-35-35.compute-1.amazonaws.com', database='d12bc1j5j4fl0k', user='gfkmakmpiswigi', password='f0c464f9d87f7803f3ce460a2e6b6b3db76f5f3a076ea4c04291dfc4c3f699a5', port='5432')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'''
        select 
            supervisor as "Supervisor",
            round(avg(replace(score, ',', '.')::numeric),2) as "Nota"
        from qualidade q
        where supervisor <> ''
        group by supervisor order by round(avg(replace(score, ',', '.')::numeric),2) asc 

    ''')
    result = db_cursor.fetchall()
    db_connection.close()

    columns = ['Supervisor', 'Nota']
    df = pd.DataFrame(data=result, columns=columns)

    return df

# KPIS CALCULATES

resultNota = notaQualidade()
resultQtde = quantidadeMonitorias()
resultNcg = ncgPercent()
resultNoPrazo = noPrazoPercent()
resultForaDoPrazo = foraDoPrazoPercent()

st.markdown('<link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.10.0/css/all.css"/>', unsafe_allow_html=True)
st.markdown(f'''

    <div class="values">
        <div class="val-box">
            <i class="fas fa-chart-pie"></i>
            <div>
                <h3>{resultNota:,}</h3>
                <span>Nota de Qualidade</span>
            </div>
        </div>  
        <div class="val-box">
            <i class="fas fa-file-signature"></i>
            <div>
                <h3>{resultQtde:,}</h3>
                <span>Quantidade</span>
            </div>
        </div>
        <div class="val-box">
            <i class="fas fa-exclamation-triangle"></i>
            <div>
                <h3>{resultNcg:,}%</h3>
                <span>NCG %</span>
            </div>
        </div>
        <div class="val-box">
            <i class="fas fa-thumbs-up"></i>
            <div>
                <h3>{resultNoPrazo:,}%</h3>
                <span>Feed No Prazo %</span>
            </div>
        </div>
        <div class="val-box">
            <i class="fas fa-thumbs-down"></i>
            <div>
                <h3>{resultForaDoPrazo:,}%</h3>
                <span>Feed Fora do Prazo %</span>
            </div>
        </div>
    </div>
''', unsafe_allow_html=True)

# CHART CALCULATES

dataFrameSupervisors = dataFrameSupervisor()

st.dataframe(dataFrameSupervisors)


chartSupervisor = px.bar(dataFrameSupervisors,
            x='Nota',
            y=dataFrameSupervisors['Supervisor'],
            text='Nota',
            #color_discrete_sequence=['#2F61EE'],
            orientation='h',
            title='<b>Qualidade Supervisor</b>',
            template='plotly_white')
            
chartSupervisor.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    
)

st.plotly_chart(chartSupervisor)