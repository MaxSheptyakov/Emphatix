from models.db_model import UserEmotion
import pandas as pd
from keyboards.emotion_gather import positive_emotion_set, negative_emotion_set
from messages.emotion_report import report_title, report_title_period
from services.common import generate_random_string
import plotly.graph_objects as go
from collections import Counter
from datetime import date


def get_emotion_type(x):
    if x in positive_emotion_set:
        return 'Positive'
    elif x in negative_emotion_set:
        return 'Negative'
    else:
        return 'Other'

def prep_to_chart_loc_on_start(x):
    if x.shape[0] == 0:
        return x
    x.reset_index(drop=True, inplace=True)
    x = pd.concat([x, pd.DataFrame([[x.iloc[0].emotion, 0, None, None, None, None, x.iloc[0].emotion_type]],
                                   columns=x.columns)])
    x = pd.concat([x, pd.DataFrame([[x.iloc[0].emotion, x.iloc[0].mean_ratio, None, None, None, None, x.iloc[0].emotion_type]],
                                   columns=x.columns)])
    # x = x.append(pd.Series([x.iloc[0].emotion, 0, None, None, None, None, x.iloc[0].emotion_type],
    #                          index = x.columns, name=0))
    # x = x.append(pd.Series([x.iloc[0].emotion, x.iloc[0].mean_ratio, None, None, None, None, x.iloc[0].emotion_type],
    #                          index = x.columns, name=0))
    return x


async def generate_emotion_flower(emotions: pd.DataFrame, days: int = 7,
                                  date_first: date = None, date_second: date = None):
    emotions['emotion_type'] = emotions.emotion.apply(get_emotion_type)
    sorter = ['Positive', 'Negative', 'Other']
    translator = {'Positive': "Позитивные",
                  "Negative":'Негативные',
                  "Other": "Свои"}
    colors = {'Positive': 'green', 'Negative': 'red', 'Other': 'gray'}
    fig = go.Figure()
    first_time = 0
    for emotion_type in sorter:
        grp = emotions.loc[emotions.emotion_type == emotion_type]
        if grp.shape[0] == 0:
            continue
        grp = prep_to_chart_loc_on_start(grp)
        fig.add_trace(go.Scatterpolar(
            r=grp.mean_ratio,
            theta=grp.emotion,
            marker=dict(color='white', size=0.0001),
            mode='markers',
            name='Средняя интенсивность:',
            showlegend=True if first_time == 0 else False
        ))
        first_time += 1
        fig.add_trace(go.Scatterpolar(
            r=grp.mean_ratio,
            theta=grp.emotion,
            fill='toself',
            name=f'{translator[emotion_type]} эмоции',
            marker=dict(color=colors[grp.emotion_type.iloc[0]]),
            showlegend=True
        ))

    fig.add_trace(go.Scatterpolar(
        r=[0],
        theta=[emotions.emotion.iloc[0]],
        marker=dict(color='white', size=0.0001),
        mode='markers',
        name='Отмечено раз:',
        showlegend=True
    ))

    legend_set = set()
    for i, row in emotions.iterrows():
        ratios = Counter(row.emotion_ratio_list)
        for ratio, cnt in ratios.items():
            fig.add_trace(go.Scatterpolar(
                r=[ratio],
                theta=[row.emotion],
                fill='none',
                marker=dict(color='black', size=cnt * 2),
                mode='markers',
                name=str(cnt),
                showlegend=True if cnt not in legend_set else False
            ))
            legend_set.add(cnt)
    if date_first is not None and date_second is not None:
        title = report_title_period.format(date_first=date_first, date_second=date_second)
    else:
        title = report_title.format(days=days)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10.5]
            )),
        showlegend=True,
        title_text=title, title_x=0.5,
    )
    fig.update_polars(radialaxis=dict(linecolor='rgba(0,0,0,0)'))
    flower_title = generate_random_string(10) + '.jpeg'
    fig.write_image(flower_title, scale=2)
    del fig
    return flower_title