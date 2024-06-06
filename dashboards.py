import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output

# Função para ler o CSV e ordenar pelo valor da coluna "GREEN"
def read_and_sort_csv(file_path):
    # Lê o CSV com o delimitador correto
    df = pd.read_csv(file_path, delimiter=';')
    
    # Imprime as colunas para depuração
    print("Colunas no arquivo CSV:", df.columns)
    
    # Remove as colunas vazias
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Verifica se a coluna "GREEN" está presente
    if "GREEN" not in df.columns:
        raise KeyError("A coluna 'GREEN' não foi encontrada no arquivo CSV.")
    
    # Converte a coluna "GREEN" para numérico (caso não esteja)
    df["GREEN"] = pd.to_numeric(df["GREEN"], errors='coerce')
    
    # Ordena pelo valor da coluna "GREEN" em ordem decrescente
    df_sorted = df.sort_values(by="GREEN", ascending=False)
    return df_sorted

# Caminho para o arquivo CSV
csv_file_path = 'dados-atualizados.csv'  # Substitua pelo caminho do seu arquivo CSV

# Lê e ordena o arquivo CSV
df = read_and_sort_csv(csv_file_path)

# Cria uma aplicação Dash
app = Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H2("Dashboard"),
    html.P("Selecione o número de ligas para visualizar:"),
    dcc.Slider(
        id='num-leagues-slider',
        min=1,
        max=min(10, len(df)),  # Limita a seleção ao máximo de ligas disponíveis
        value=6,
        marks={i: str(i) for i in range(1, min(11, len(df)+1))},
        step=1
    ),
    dash_table.DataTable(
        id='league-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.head(6).to_dict('records')
    ),
    dcc.Graph(id='bar-chart')
])

# Callback para atualizar a tabela e o gráfico com base no número de ligas selecionado
@app.callback(
    [Output('league-table', 'data'),
     Output('bar-chart', 'figure')],
    [Input('num-leagues-slider', 'value')]
)
def update_output(num_leagues):
    filtered_df = df.head(num_leagues)
    
    # Cria o gráfico de barras com estilização adicional
    fig = px.bar(
        filtered_df, 
        x='LIGA', 
        y='GREEN', 
        title='Melhores ligas - 11/2021',
        labels={'LIGA': 'Liga', 'GREEN': 'Qtd de GREENS'},
        color='LIGA',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Adiciona rótulos de dados
    fig.update_traces(texttemplate='%{y}', textposition='outside')

    # Atualiza o layout do gráfico
    fig.update_layout(
        title_font_size=24,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
        yaxis=dict(tickfont=dict(size=14)),
        xaxis=dict(tickfont=dict(size=14)),
        margin=dict(l=40, r=40, t=60, b=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black'),
        hovermode='closest',
        bargap=0.15
    )

    return filtered_df.to_dict('records'), fig

# Executa a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
