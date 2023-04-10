from services.common import generate_random_string
from messages.trigger_report import trigger_report_days_title, trigger_report_period_title
import plotly.graph_objects as go

async def get_emotion_triggers_report(triggers_report, emotion, days=None, date_first=None, date_second=None):
    fig = go.Figure()
    trace = go.Sunburst(
        labels=triggers_report.trigger.tolist(),
        parents=triggers_report.emotion.tolist(),
        values=triggers_report.emotion_count.tolist(),
        branchvalues="total",
        outsidetextfont={"size": 20, "color": "#377eb8"},
        marker={"line": {"width": 2}},
    )

    layout = go.Layout(
        margin=go.layout.Margin(t=40, l=0, r=0, b=0)
    )
    if date_first and date_second:
        title = trigger_report_period_title.format(emotion=emotion, date_first=date_first, date_second=date_second)
    else:
        title = trigger_report_days_title.format(emotion=emotion, days=days)

    fig.add_trace(trace)
    fig.layout = layout
    fig.update_layout(
        title_text=title, title_x=0.5, title={'font': {'size': 15}}
    )
    fig.update_traces(textinfo="label+percent root")
    img_title = generate_random_string(10) + '.jpeg'
    fig.write_image(img_title, scale=2)
    del fig
    return img_title