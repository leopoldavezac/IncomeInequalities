from datetime import MAXYEAR
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

FILE_PATH = "./WID_clean.csv"
MS_PER_YEAR = 700

df = pd.read_csv(FILE_PATH)
MIN_YEAR = 1980
MAX_YEAR = df.year.max()
N_YEAR = MAX_YEAR - MIN_YEAR


def create_map_chart(df):
    fig = go.Figure(data=go.Choropleth(
        locations = df['code'],
        z = df['value'],
        zmin=0,
        zmax=60,
        text = df['country'],
        colorscale = 'reds',
        autocolorscale=False,
        marker_line_color='white',
        marker_line_width=0.25,
    ))

    fig.update_layout(
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0, autoexpand=True),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )

    fig = dcc.Graph(figure=fig)

    return fig


app = dash.Dash()
app.layout = html.Div(
    children=[
        dbc.Container(dbc.Row(dbc.Col(html.Div(id="chart")))),
        dcc.Interval(id="timer", interval=MS_PER_YEAR, n_intervals=0, max_intervals=N_YEAR)
        ]
)

@app.callback(
    dash.dependencies.Output("chart", "children"),
    [dash.dependencies.Input("timer", "n_intervals")]
)
def update_chart(n_intervals):

    this_year = MIN_YEAR+n_intervals
    this_year_df = df.loc[df.year == this_year]
    chart = create_map_chart(this_year_df)
    title_nm = "Share (%) of national income earned by top 1% earners - " + str(this_year)
    title = html.H1(
        title_nm,
        style={
            "text-align":"center",
            "color":"#485679",
            "font-weight":"bold",
            }
        )
    return [title, chart]

app.run_server(debug=True) 