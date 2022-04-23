
import dash_bootstrap_components as dbc
import dash_html_components as html


def init_dashboard():
    return html.Div(dbc.Row([
                    html.H2(children="US Overview")]))
