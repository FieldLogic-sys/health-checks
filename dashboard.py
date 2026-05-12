from dash import Dash, html, dcc, Input, Output, State
import requests

app = Dash(__name__)

app.layout = html.Div([
    html.H1("System Health Architect"),
    html.Hr(),

    html.Div([
        html.H3("Passive Monitoring (Live)"),
        html.Div(id='live-cpu'),
        html.Div(id='live-disk'),
        html.Div(id='live-net-status'),
        html.Div(id='live-time'),
    ], style={'padding': '20px', 'border': '1px solid #ccc', 'borderRadius': '10px'}),

    html.Div([
        html.H3("Active Diagnostics"),
        html.Button('Run Speedtest', id='btn-speed', n_clicks=0),
        dcc.Loading(
            id="loading-speed",
            children=[html.Div(id='speed-results')],
            type="circle"
        )
    ], style={'marginTop': '20px'}),

    dcc.Interval(id='health-interval', interval=5000, n_intervals=0)
])

@app.callback(
    [Output('live-cpu', 'children'),
     Output('live-disk', 'children'),
     Output('live-net-status', 'children'),
     Output('live-time', 'children')],
    [Input('health-interval', 'n_intervals')],
    [State('live-cpu', 'children'),
     State('live-disk', 'children'),
     State('live-net-status', 'children')]
)
def refresh_health(n, old_cpu, old_disk, old_net):
    try:
        # Pinging the API with a 2-second timeout
        r = requests.get("http://127.0.0.1:8000/health", timeout=2).json()
        return (
            f"CPU Load: {r['cpu_usage']}%",
            f"Disk Status: {r['disk_info']}",
            f"Network: {'ONLINE' if r['network_ok'] else 'OFFLINE'}",
            f"Last Sync: {r['timestamp']}"
        )
    except:
        # If the API is busy or restarting, we show the old values
        # so the screen doesn't flicker or say "Syncing"
        return old_cpu, old_disk, old_net, "Syncing (API Busy)..."

@app.callback(
    Output('speed-results', 'children'),
    Input('btn-speed', 'n_clicks'),
    prevent_initial_call=True
)
def trigger_speedtest(n_clicks):
    try:
        r = requests.get("http://127.0.0.1:8000/speedtest").json()
        return f"Download: {r['download']} Mbps | Upload: {r['upload']} Mbps | Ping: {r['ping']} ms"
    except Exception as e:
        return f"Speedtest failed: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=8050)