
from pickletools import markobject
from tkinter import Y
from turtle import color
import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from load_css import local_css

st.set_page_config(page_title='Neobpo IN',
                    page_icon=':bar_chart',
                    layout='wide')

local_css("css/style.css")


# SIDEBAR

start_date = st.sidebar.date_input("Data início", value=pd.to_datetime("2022-01-01", format="%Y-%m-%d"))
end_date = st.sidebar.date_input("Data Fim", value=pd.to_datetime("today", format="%Y-%m-%d"))


cboCoordenador = st.sidebar.selectbox(
    "Selecione o coordenador",
    options=["Todos","VERONICA SANTOS DE MORAES", "LUCAS  REZENDE"]
)

# FUNCION KPIS CARDS 

def notaQualidadeTodos():
    db_connection = psycopg2.connect(host='ec2-54-235-98-1.compute-1.amazonaws.com', database='da9l8k9c6ulbd5', user='lcmulsicvhazdl', password='0101b23af78c44e6bf095833662077d9909afdc669962f0fd8b7ef593916fd91', port='5432')
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

def quantidadeMonitoriasTodos():
    db_connection = psycopg2.connect(host='ec2-54-235-98-1.compute-1.amazonaws.com', database='da9l8k9c6ulbd5', user='lcmulsicvhazdl', password='0101b23af78c44e6bf095833662077d9909afdc669962f0fd8b7ef593916fd91', port='5432')
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

def ncgPercentTodos():
    db_connection = psycopg2.connect(host='ec2-54-235-98-1.compute-1.amazonaws.com', database='da9l8k9c6ulbd5', user='lcmulsicvhazdl', password='0101b23af78c44e6bf095833662077d9909afdc669962f0fd8b7ef593916fd91', port='5432')
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

def noPrazoPercentTodos():
    db_connection = psycopg2.connect(host='ec2-54-235-98-1.compute-1.amazonaws.com', database='da9l8k9c6ulbd5', user='lcmulsicvhazdl', password='0101b23af78c44e6bf095833662077d9909afdc669962f0fd8b7ef593916fd91', port='5432')
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

def foraDoPrazoPercentTodos():
    db_connection = psycopg2.connect(host='ec2-54-235-98-1.compute-1.amazonaws.com', database='da9l8k9c6ulbd5', user='lcmulsicvhazdl', password='0101b23af78c44e6bf095833662077d9909afdc669962f0fd8b7ef593916fd91', port='5432')
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

# FUNCION CHARTS 

def dataFrameSupervisorTodos():
    db_connection = psycopg2.connect(host='ec2-54-235-98-1.compute-1.amazonaws.com', database='da9l8k9c6ulbd5', user='lcmulsicvhazdl', password='0101b23af78c44e6bf095833662077d9909afdc669962f0fd8b7ef593916fd91', port='5432')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'''
        select 
            supervisor as "Supervisor",
            round(avg(replace(score, ',', '.')::numeric),2) as "Nota"
        from qualidade q
        where supervisor <> ''
        and to_char(to_date(segmentstarttime,'dd-mm-yyyy'), 'yyyy-mm-dd')::date >= '{start_date}'
        and to_char(to_date(segmentstarttime,'dd-mm-yyyy'), 'yyyy-mm-dd')::date <= '{end_date}'
        group by supervisor order by round(avg(replace(score, ',', '.')::numeric),2) asc 

    ''')
    result = db_cursor.fetchall()
    db_connection.close()

    columns = ['Supervisor', 'Nota']
    df = pd.DataFrame(data=result, columns=columns)

    return df

def dataframeStatusTodos():
    db_connection = psycopg2.connect(host='ec2-54-235-98-1.compute-1.amazonaws.com', database='da9l8k9c6ulbd5', user='lcmulsicvhazdl', password='0101b23af78c44e6bf095833662077d9909afdc669962f0fd8b7ef593916fd91', port='5432')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'''
            select
                status as "Status",
                count(status) as "Qtde"
            from qualidade q
            where to_char(to_date(segmentstarttime,'dd-mm-yyyy'), 'yyyy-mm-dd')::date >= '{start_date}'
            and to_char(to_date(segmentstarttime,'dd-mm-yyyy'), 'yyyy-mm-dd')::date <= '{end_date}'
            group by status
            order by count(status) desc
    ''')

    result = db_cursor.fetchall()
    db_connection.close()

    columns = ['Status', 'Qtde']
    df = pd.DataFrame(data=result, columns=columns)

    return df    

def dataframeQuartilTodos():
    db_connection = psycopg2.connect(host='ec2-54-235-98-1.compute-1.amazonaws.com', database='da9l8k9c6ulbd5', user='lcmulsicvhazdl', password='0101b23af78c44e6bf095833662077d9909afdc669962f0fd8b7ef593916fd91', port='5432')
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'''
            select 
                nome as "Nome",
                supervisor as "Supervisor",
                coordenador as "Coordenador",
                round(avg(replace(score,',','.')::numeric), 2) as "Score",
                NTILE(4) OVER( ORDER BY round(avg(replace(score,',','.')::numeric), 2) desc) as "Quartil"
                    
            FROM qualidade q 
            where nome <> '' 
            and to_char(to_date(segmentstarttime,'dd-mm-yyyy'), 'yyyy-mm-dd')::date >= '{start_date}'
            and to_char(to_date(segmentstarttime,'dd-mm-yyyy'), 'yyyy-mm-dd')::date <= '{end_date}'
            group by nome, supervisor, coordenador 
  
    ''')

    result = db_cursor.fetchall()
    db_connection.close()

    columns = ['Nome', 'Supervisor', 'Coordenador', 'Score', 'Quartil']
    df = pd.DataFrame(data=result, columns=columns)
    df['Quartil'].replace({1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}, inplace=True)

    return df  

# RESULTS KPIS CARDS 

resultNota = notaQualidadeTodos()
resultQtde = quantidadeMonitoriasTodos()
resultNcg = ncgPercentTodos()
resultNoPrazo = noPrazoPercentTodos()
resultForaDoPrazo = foraDoPrazoPercentTodos()

# RESULTS CHARTS

resultSuper = dataFrameSupervisorTodos()
resultStatus = dataframeStatusTodos()
resultQuartil = dataframeQuartilTodos()

# --------- FRONT-END --------------#

# CARDS KPI
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

# CHART QUARTIL


quartilOperadorScore = (
    round(resultQuartil.groupby(by=['Quartil'], as_index=False).mean()[['Score']].sort_values(by='Score'),2)
)
quartilOperadorQtde = (
     resultQuartil.groupby(by=['Quartil'], as_index=False).count()[['Score']].sort_values(by='Score', ascending=False).rename(columns={'Score': 'Qtde HC'})

)

chartQuartilScore = px.bar(quartilOperadorScore,
            y='Score',
            x=quartilOperadorScore.index,
            text='Score',
            color_discrete_sequence=['#2F61EE'],
            orientation='v',
            title='<b>Nota por Quartil</b>',
            template='plotly_white')
            
chartQuartilScore.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    
)


chartQuartilQtde = px.bar(quartilOperadorQtde,
            y='Qtde HC',
            x=quartilOperadorQtde.index,
            text='Qtde HC',
            color_discrete_sequence=['#2F61EE'],
            orientation='v',
            title='<b>Quantidade HC por Quartil</b>',
            template='plotly_white')
            
chartQuartilQtde.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    
)


# CHART BAR SUPERVISOR

chartSupervisor = px.bar(resultSuper,
            y='Nota',
            x=resultSuper['Supervisor'],
            text='Nota',
            color_discrete_sequence=['#7700FF'],
            orientation='v',
            title='<b>Qualidade Supervisor</b>',
            template='plotly_white')
            
chartSupervisor.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    
)

# CHART PIE STATUS FEEDBACK

chartFeedback = px.pie(resultStatus, 
            values='Qtde', 
            names='Status',
            title='<b>Status Feedback</b>',
            color_discrete_sequence=['#58D68D', '#F8C471', '#EC7063', '#85C1E9']
            )

chartFeedback.update_layout(   
    plot_bgcolor='rgba(0,0,0,0.1)',
    xaxis=(dict(showgrid=False)),
    legend=dict(orientation = "h",   # show entries horizontally
                     xanchor = "center",  # use center of legend as anchor
                     x = 0.5)
)


col1, col2, col3 = st.beta_columns(3)

with col1:
    st.plotly_chart(chartFeedback,  use_container_width=True)

with col2:
    st.plotly_chart(chartQuartilScore, use_container_width=True)

with col3:
    st.plotly_chart(chartQuartilQtde, use_container_width=True)

st.plotly_chart(chartSupervisor, use_container_width=True)

st.markdown('#')

st.dataframe(resultQuartil)








