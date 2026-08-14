import plotly.graph_objects as go


def progress_graph(title: str, max_val: float, current_val: float):
    if max_val <= 0:
        percent = 0
        res = 100
        text = f"{current_val} / {max_val}"
    else:
        visual_progress = min(current_val, max_val)
        percent = (visual_progress / max_val) * 100
        res = 100 - percent
        text = f"<b>{round(current_val, 2)}</b> / {round(max_val, 2)}"

    colores = ["#1f77b4", "#e6e6e6"]

    fig = go.Figure(
        data=[
            go.Pie(
                values=[percent, res],
                labels=["Progreso", "Restante"],
                hole=0.7,
                marker_colors=colores,
                sort=False,
                textinfo="none",
                hoverinfo="label+percent",
            )
        ]
    )

    fig.update_layout(
        title={
            "text": title,
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20},
        },
        showlegend=False,
        margin=dict(t=50, b=10, l=10, r=10),
        height=350,
        annotations=[
            {
                "text": text,
                "x": 0.5,
                "y": 0.5,
                "font_size": 24,
                "showarrow": False,
                "font_family": "Arial",
            }
        ],
    )

    return fig
