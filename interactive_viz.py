"""
Interactive GEMM Memory Access Pattern Visualizer using Dash

A web-based interactive visualization tool for exploring different
GEMM loop orderings and their memory access patterns.
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from gemm_simulator import GEMMSimulator
from cache_simulator import CacheSimulator


# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "GEMM Visualizer"

# Global state for simulation data
simulation_data = {
    'simulator': None,
    'tracks': [],
    'current_frame': 0,
    'cache_stats': {},
    'heatmaps': {}
}

# Color scheme for matrices
COLORS = {
    'A': 'rgba(255, 0, 0, 0.7)',      # Red
    'B': 'rgba(0, 255, 0, 0.7)',      # Green
    'C': 'rgba(0, 0, 255, 0.7)',      # Blue
}

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("🔬 GEMM Memory Access Pattern Visualizer",
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 10}),
        html.P("Explore different loop orderings and their impact on cache performance",
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': 16})
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'borderRadius': '10px'}),

    html.Div([
        # Left panel - Controls
        html.Div([
            html.H3("⚙️ Configuration", style={'color': '#34495e'}),

            html.Label("Matrix Size (n × n):", style={'fontWeight': 'bold', 'marginTop': 15}),
            dcc.Slider(
                id='matrix-size-slider',
                min=4, max=32, step=2, value=16,
                marks={i: str(i) for i in [4, 8, 16, 24, 32]},
                tooltip={"placement": "bottom", "always_visible": True}
            ),

            html.Label("Block Size:", style={'fontWeight': 'bold', 'marginTop': 25}),
            dcc.Slider(
                id='block-size-slider',
                min=2, max=16, step=2, value=4,
                marks={i: str(i) for i in [2, 4, 8, 16]},
                tooltip={"placement": "bottom", "always_visible": True}
            ),

            html.Label("Loop Order:", style={'fontWeight': 'bold', 'marginTop': 25}),
            dcc.Dropdown(
                id='loop-order-dropdown',
                options=[
                    {'label': 'IJK (row-column-depth)', 'value': 'ijk'},
                    {'label': 'IKJ (row-depth-column)', 'value': 'ikj'},
                    {'label': 'JIK (column-row-depth)', 'value': 'jik'},
                    {'label': 'JKI (column-depth-row)', 'value': 'jki'},
                    {'label': 'KIJ (depth-row-column)', 'value': 'kij'},
                    {'label': 'KJI (depth-column-row)', 'value': 'kji'},
                ],
                value='kji',
                clearable=False
            ),

            html.Div([
                html.Label("Blocking:", style={'fontWeight': 'bold', 'marginTop': 25}),
                dcc.RadioItems(
                    id='blocking-radio',
                    options=[
                        {'label': ' Blocked', 'value': True},
                        {'label': ' Unblocked', 'value': False}
                    ],
                    value=True,
                    inline=True,
                    style={'marginTop': 10}
                )
            ]),

            html.Hr(style={'marginTop': 30, 'marginBottom': 20}),

            html.H3("🎬 Animation Controls", style={'color': '#34495e'}),

            html.Div([
                html.Button('▶ Play', id='play-button', n_clicks=0,
                           style={'marginRight': 10, 'padding': '10px 20px'}),
                html.Button('⏸ Pause', id='pause-button', n_clicks=0,
                           style={'marginRight': 10, 'padding': '10px 20px'}),
                html.Button('🔄 Reset', id='reset-button', n_clicks=0,
                           style={'padding': '10px 20px'}),
            ], style={'marginTop': 15, 'marginBottom': 15}),

            html.Label("Animation Speed:", style={'fontWeight': 'bold', 'marginTop': 15}),
            dcc.Slider(
                id='speed-slider',
                min=1, max=100, step=1, value=10,
                marks={1: 'Slow', 50: 'Medium', 100: 'Fast'},
                tooltip={"placement": "bottom", "always_visible": True}
            ),

            html.Label("Frame:", style={'fontWeight': 'bold', 'marginTop': 25}),
            dcc.Slider(
                id='frame-slider',
                min=0, max=100, step=1, value=0,
                marks={},
                tooltip={"placement": "bottom", "always_visible": True}
            ),

            html.Div(id='frame-info', style={'marginTop': 10, 'fontSize': 14, 'color': '#7f8c8d'}),

            # Hidden components for state management
            dcc.Interval(id='animation-interval', interval=100, disabled=True),
            dcc.Store(id='animation-state', data={'playing': False, 'frame': 0}),

        ], style={
            'width': '25%',
            'padding': '20px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '10px',
            'marginRight': '2%'
        }),

        # Right panel - Visualizations
        html.Div([
            # Main animation display
            dcc.Graph(id='main-animation', style={'height': '450px'}),

            # Statistics and cache performance
            html.Div([
                html.Div([
                    dcc.Graph(id='cache-performance', style={'height': '250px'})
                ], style={'width': '48%', 'display': 'inline-block'}),

                html.Div([
                    html.Div(id='statistics-panel', style={
                        'padding': '20px',
                        'backgroundColor': '#fff',
                        'borderRadius': '10px',
                        'height': '250px',
                        'overflowY': 'auto'
                    })
                ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'}),
            ]),

            # Heatmaps
            html.H3("📊 Access Frequency Heatmaps", style={'marginTop': 30, 'color': '#34495e'}),
            dcc.Graph(id='heatmaps', style={'height': '300px'}),

        ], style={'width': '73%'}),

    ], style={'display': 'flex', 'marginTop': 20}),

], style={'padding': '20px', 'backgroundColor': '#ffffff', 'fontFamily': 'Arial, sans-serif'})


# Callback to initialize/update simulation
@app.callback(
    [Output('frame-slider', 'max'),
     Output('frame-slider', 'marks'),
     Output('statistics-panel', 'children'),
     Output('animation-state', 'data')],
    [Input('matrix-size-slider', 'value'),
     Input('block-size-slider', 'value'),
     Input('loop-order-dropdown', 'value'),
     Input('blocking-radio', 'value'),
     Input('reset-button', 'n_clicks')]
)
def update_simulation(n, block_size, loop_order, blocked, reset_clicks):
    """Initialize or update the simulation when parameters change."""
    # Create simulator
    sim = GEMMSimulator(n=n, block_size=block_size if blocked else None)
    tracks = sim.simulate(loop_order, blocked=blocked)

    # Run cache simulation
    # Use a smaller cache to better demonstrate the impact of different loop orderings
    # For n=16: 3 matrices * 16*16*8 bytes = 6KB total
    # Using 4KB cache creates realistic cache pressure
    cache_size = max(4096, n * n * 8)  # Scale cache size with matrix size, minimum 4KB
    cache = CacheSimulator(cache_size=cache_size, line_size=64, associativity=4)
    cache_stats = cache.simulate_accesses(tracks, matrix_size=n)

    # Store in global state
    simulation_data['simulator'] = sim
    simulation_data['tracks'] = tracks
    simulation_data['cache_stats'] = cache_stats
    simulation_data['heatmaps'] = sim.get_heatmap_data()

    # Prepare slider marks
    max_frame = len(tracks) - 1
    step = max(1, max_frame // 10)
    marks = {i: str(i) for i in range(0, max_frame + 1, step)}

    # Statistics panel content
    stats_content = html.Div([
        html.H4("📈 Statistics", style={'color': '#34495e', 'marginBottom': 15}),
        html.P([html.Strong("Matrix Size: "), f"{n} × {n}"]),
        html.P([html.Strong("Block Size: "), f"{block_size}" if blocked else "Unblocked"]),
        html.P([html.Strong("Loop Order: "), loop_order.upper()]),
        html.Hr(),
        html.P([html.Strong("Total Operations: "), f"{len(tracks):,}"]),
        html.P([html.Strong("Memory Accesses: "), f"{cache_stats['total_accesses']:,}"]),
        html.P([html.Strong("Cache Size: "), f"{cache_size // 1024}KB"], style={'fontSize': 12, 'color': '#7f8c8d'}),
        html.Hr(),
        html.H5("🎯 Cache Performance", style={'color': '#34495e', 'marginTop': 15}),
        html.P([html.Strong("Hit Rate: "),
                html.Span(f"{cache_stats['hit_rate']:.2f}%",
                         style={'color': '#27ae60' if cache_stats['hit_rate'] > 80 else '#e74c3c',
                               'fontSize': 18, 'fontWeight': 'bold'})]),
        html.P([html.Strong("Hits: "), f"{cache_stats['hits']:,}"]),
        html.P([html.Strong("Misses: "), f"{cache_stats['misses']:,}"]),
    ])

    return max_frame, marks, stats_content, {'playing': False, 'frame': 0}


# Callback to handle play/pause
@app.callback(
    [Output('animation-interval', 'disabled'),
     Output('animation-state', 'data', allow_duplicate=True)],
    [Input('play-button', 'n_clicks'),
     Input('pause-button', 'n_clicks')],
    [State('animation-state', 'data')],
    prevent_initial_call=True
)
def control_animation(play_clicks, pause_clicks, state):
    """Control play/pause of animation."""
    ctx = callback_context
    if not ctx.triggered:
        return True, state

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'play-button':
        state['playing'] = True
        return False, state  # Enable interval
    else:  # pause-button
        state['playing'] = False
        return True, state  # Disable interval


# Callback to update frame
@app.callback(
    [Output('frame-slider', 'value'),
     Output('animation-state', 'data', allow_duplicate=True)],
    [Input('animation-interval', 'n_intervals'),
     Input('frame-slider', 'value'),
     Input('reset-button', 'n_clicks')],
    [State('animation-state', 'data'),
     State('frame-slider', 'max'),
     State('speed-slider', 'value')],
    prevent_initial_call=True
)
def update_frame(n_intervals, slider_value, reset_clicks, state, max_frame, speed):
    """Update the current frame."""
    ctx = callback_context
    if not ctx.triggered:
        return 0, state

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'reset-button':
        state['frame'] = 0
        state['playing'] = False
        return 0, state

    if trigger_id == 'frame-slider':
        state['frame'] = slider_value
        return slider_value, state

    if trigger_id == 'animation-interval' and state['playing']:
        # Calculate frame increment based on speed
        increment = max(1, speed // 10)
        new_frame = state['frame'] + increment

        if new_frame >= max_frame:
            new_frame = max_frame
            state['playing'] = False

        state['frame'] = new_frame
        return new_frame, state

    return state['frame'], state


# Callback to update visualizations
@app.callback(
    [Output('main-animation', 'figure'),
     Output('frame-info', 'children'),
     Output('cache-performance', 'figure'),
     Output('heatmaps', 'figure')],
    [Input('frame-slider', 'value'),
     Input('matrix-size-slider', 'value')]
)
def update_visualizations(frame, n):
    """Update all visualizations based on current frame."""
    tracks = simulation_data.get('tracks', [])
    cache_stats = simulation_data.get('cache_stats', {})
    heatmaps = simulation_data.get('heatmaps', {})

    if not tracks:
        # Return empty figures
        empty_fig = go.Figure()
        return empty_fig, "", empty_fig, empty_fig

    frame = min(frame, len(tracks) - 1)
    current_access = tracks[frame]

    # Main animation figure
    main_fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Matrix A', 'Matrix B', 'Matrix C'),
        horizontal_spacing=0.1
    )

    # Create grid for each matrix
    for idx, (matrix_name, pos) in enumerate([('A', current_access[0]),
                                                ('B', current_access[1]),
                                                ('C', current_access[2])]):
        # Background grid
        grid = np.zeros((n, n))
        grid[pos[0], pos[1]] = 1

        main_fig.add_trace(
            go.Heatmap(
                z=grid,
                colorscale=[[0, 'white'], [1, COLORS[matrix_name]]],
                showscale=False,
                hovertemplate=f'{matrix_name}[%{{y}}, %{{x}}]<extra></extra>'
            ),
            row=1, col=idx + 1
        )

    main_fig.update_xaxes(showticklabels=False, showgrid=True, gridcolor='lightgray')
    main_fig.update_yaxes(showticklabels=False, showgrid=True, gridcolor='lightgray', autorange='reversed')
    main_fig.update_layout(
        title=f"Memory Access Pattern (Frame {frame}/{len(tracks)-1})",
        height=450,
        showlegend=False
    )

    # Frame info
    a_pos, b_pos, c_pos = current_access
    frame_info = html.Div([
        html.P(f"Frame: {frame} / {len(tracks)-1}", style={'fontWeight': 'bold'}),
        html.P(f"A[{a_pos[0]},{a_pos[1]}] • B[{b_pos[0]},{b_pos[1]}] • C[{c_pos[0]},{c_pos[1]}]")
    ])

    # Cache performance chart
    hit_rate_history = cache_stats.get('hit_rate_history', [])
    cache_fig = go.Figure()
    cache_fig.add_trace(go.Scatter(
        y=hit_rate_history,
        mode='lines',
        line=dict(color='#27ae60', width=2),
        fill='tozeroy',
        name='Hit Rate'
    ))
    cache_fig.update_layout(
        title="Cache Hit Rate Over Time",
        xaxis_title="Access (×100)",
        yaxis_title="Hit Rate (%)",
        yaxis=dict(range=[0, 100]),
        height=250,
        margin=dict(l=40, r=20, t=40, b=40)
    )

    # Heatmaps
    heatmap_fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Matrix A Access Frequency',
                       'Matrix B Access Frequency',
                       'Matrix C Access Frequency'),
        horizontal_spacing=0.1
    )

    for idx, matrix_name in enumerate(['A', 'B', 'C']):
        heatmap_data = heatmaps.get(matrix_name, np.zeros((n, n)))
        heatmap_fig.add_trace(
            go.Heatmap(
                z=heatmap_data,
                colorscale='YlOrRd',
                showscale=(idx == 2),
                hovertemplate=f'{matrix_name}[%{{y}}, %{{x}}]: %{{z}} accesses<extra></extra>'
            ),
            row=1, col=idx + 1
        )

    heatmap_fig.update_xaxes(showticklabels=False)
    heatmap_fig.update_yaxes(showticklabels=False, autorange='reversed')
    heatmap_fig.update_layout(height=300)

    return main_fig, frame_info, cache_fig, heatmap_fig


if __name__ == '__main__':
    print("🚀 Starting GEMM Interactive Visualizer...")
    print("📱 Open your browser to: http://127.0.0.1:8050")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=8050)
