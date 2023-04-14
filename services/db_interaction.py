from typing import List, Union

import pytz
import pandas as pd

from models.db_model import *
from aiogram.types import Message
from sqlalchemy import select, delete, update, text
from dateutil import parser
from aiogram.dispatcher import FSMContext
from sqlalchemy import func, desc
from datetime import timedelta, date
from services.common import get_hour_diff, add_hours_to_time
from datetime import time, datetime
from keyboards.emotion_gather import dont_know_button, first_emotion_list, second_emotion_list, \
    show_more_emotions_button, back_button, write_own_emotion_button, triggers_start_gather_buttons, \
    triggers_dict, negative_emotion_set


def get_field_from_message_user(message: Message, field: str) -> Union[str, None, int]:
    try:
        return message.from_user[field]
    except KeyError as e:
        return


class DB:
    """DB abstraction layer"""

    def __init__(self, session):
        self.session = session

    async def return_user_if_exist(self, message: Message) -> User:
        user_id = message.from_user
        statement = select(User).filter_by(user_id=user_id)
        user_info = await self.session.execute(statement)
        user = user_info.first()
        if user is None:
            user = await self.add_user(message)
            return user
        return user[0]


    async def has_user_premium(self, message: Message) -> bool:
        user = await self.return_user_if_exist(message)
        return user.premium_until >= datetime.now(pytz.utc) if user.premium_until is not None else False


    async def return_user_by_id(self, user_id: Union[int, str]) -> Union[User, None]:
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        statement = select(User).filter_by(user_id=user_id)
        user_info = await self.session.execute(statement)
        user = user_info.scalars().all()
        if user is None or len(user) == 0:
            return
        return user[0]

    async def has_user_completed_questionnaire(self, message: Message) -> bool:
        user = await self.return_user_if_exist(message)
        return user.completed_questionnaire

    async def add_user(self, message: Message) -> User:
        user_id = message.from_id
        user = await self.return_user_by_id(user_id)
        if user is None:
            user = User(user_id=user_id,
                        username=get_field_from_message_user(message, 'username'),
                        first_name=get_field_from_message_user(message, 'first_name'),
                        last_name=get_field_from_message_user(message, 'last_name'),
                        language_code=get_field_from_message_user(message, 'language_code'),
                        premium_until=datetime.utcnow() + timedelta(days=7)
                        )
            self.session.add(user)
            await self.session.commit()
        elif not user.is_active:
            user.is_active = True
            await self.session.commit()

        return user

    async def write_emotion_info(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        user_id = get_field_from_message_user(message, 'id')
        emotion = UserEmotion()
        emotion.user_id = user_id
        emotion_text = user_data.get('user_emotion')
        emotion_text = emotion_text.strip().capitalize()
        emotion.emotion = emotion_text
        try:
            emotion.emotion_ratio = int(user_data.get('emotion_intensity'))
        except:
            pass
        self.session.add(emotion)
        await self.session.commit()
        return emotion


    async def store_trigger(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        trigger = EmotionTrigger(user_emotion_id=user_data.get('user_emotion_id'),
                                 trigger=user_data.get('trigger'),
                                 trigger_second_layer=user_data.get('trigger_second_layer')
                                 )
        self.session.add(trigger)
        await self.session.commit()


    async def get_emotions_last_n_days(self, message: Message, days: int = 1):
        user_id = get_field_from_message_user(message, 'id')
        statement = select(UserEmotion).filter_by(user_id=user_id)\
            .filter(UserEmotion.created_at >= func.now() - timedelta(days=days))
        emotions = await self.session.execute(statement)
        emotions = emotions.scalars().all()
        return emotions

    async def get_emotions_period(self, message: Message, date_from: date, date_to: date):
        user_id = get_field_from_message_user(message, 'id')
        statement = select(UserEmotion).filter_by(user_id=user_id)\
            .filter(UserEmotion.created_at >= date_from, UserEmotion.created_at <= date_to + timedelta(days=1))
        emotions = await self.session.execute(statement)
        emotions = emotions.scalars().all()
        return emotions

    async def get_emotions_for_flower(self, message: Message, days: int = 7):
        user_id = message.from_id
        statement = text(f"""
        select emotion, avg(emotion_ratio) mean_ratio
            , min(emotion_ratio) min_ratio, max(emotion_ratio) max_ratio
            , count(emotion) emotion_count, array_agg(emotion_ratio) emotion_ratio_list
        from user_emotion
        where created_at  >= now() - interval '{days} days'
            and user_id = {user_id}
        group by 1""")
        emotions = await self.session.execute(statement)
        emotions = pd.DataFrame(emotions)
        return emotions

    async def get_emotions_for_flower_period(self, message: Message, date_first: date, date_second: date):
        user_id = message.from_id
        statement = text(f"""
        select emotion, avg(emotion_ratio) mean_ratio
            , min(emotion_ratio) min_ratio, max(emotion_ratio) max_ratio
            , count(emotion) emotion_count, array_agg(emotion_ratio) emotion_ratio_list
        from user_emotion
        where created_at  between '{date_first}' and '{date_second} 23:59:59'
            and user_id = {user_id}
        group by 1""")
        emotions = await self.session.execute(statement)
        emotions = pd.DataFrame(emotions)
        return emotions

    async def get_top_n_emotions(self, message: Message, days: int = 1, n: int = 3):
        user_id = message.from_id
        statement = select(UserEmotion.emotion, func.count(UserEmotion.emotion_ratio).label('emotion_count'))\
            .filter_by(user_id=user_id) \
            .filter(UserEmotion.created_at >= func.now() - timedelta(days=days))\
            .group_by(UserEmotion.emotion).order_by(desc('emotion_count')).limit(n)
        emotions = await self.session.execute(statement)
        emotions = emotions.scalars().all()
        return emotions

    async def get_emotions_sorted_list(self, message: Message, days=30):
        emotions_occurred = await self.get_top_n_emotions(message, days, 999)
        emotions_total = first_emotion_list + second_emotion_list
        emotions_show = emotions_occurred + [x for x in emotions_total if x not in emotions_occurred]
        divider = len(emotions_show)//2
        return emotions_show[:divider] + [write_own_emotion_button, show_more_emotions_button, dont_know_button], \
               emotions_show[divider:] + [write_own_emotion_button, back_button, dont_know_button]

    async def get_emotions_sorted_one_list(self, message: Message, days=30):
        emotions_occurred = await self.get_top_n_emotions(message, days, 999)
        emotions_total = first_emotion_list + second_emotion_list
        emotions_show = emotions_occurred + [x for x in emotions_total if x not in emotions_occurred]
        divider = len(emotions_show)//2
        return emotions_show + [dont_know_button]


    async def get_triggers_sorted_list(self, message, days=30):
        statement = text(f"""select t.trigger, count(1) emotion_count
                from emotion_triggers t 
                    join user_emotion e on t.user_emotion_id = e.user_emotion_id
                        and e.user_id = {message.from_id}
                where t.created_at >= now() - interval '{days} days'
                group by 1
                order by 2 desc
                limit 10;""")

        triggers_report = await self.session.execute(statement)
        triggers_listed = pd.DataFrame(triggers_report)
        triggers_listed = triggers_listed.trigger.tolist() if 'trigger' in triggers_listed.columns else []
        triggers_list = triggers_listed + [x for x in triggers_start_gather_buttons if x not in triggers_listed]
        return triggers_list


    async def get_triggers_second_layer_sorted_list(self, message, days=30):
        statement = text(f"""select t.trigger_second_layer, count(1) emotion_count
                from emotion_triggers t 
                    join user_emotion e on t.user_emotion_id = e.user_emotion_id
                        and e.user_id = {message.from_id}
                where t.created_at >= now() - interval '{days} days'
                    and t.trigger = '{message.text}'
                group by 1
                order by 2 desc
                limit 10;""")

        triggers_report = await self.session.execute(statement)
        triggers_listed = pd.DataFrame(triggers_report)
        triggers_second_layer = triggers_dict.get(message.text)
        if triggers_listed.shape[0] >= 0 and 'trigger_second_layer' in triggers_listed.columns:
            triggers_listed = triggers_listed.trigger_second_layer.tolist()
            if triggers_second_layer is not None:
                triggers_list = triggers_listed + [x for x in triggers_second_layer if x not in triggers_listed]
                return triggers_list
            else:
                return []
        else:
            return [x for x in triggers_second_layer]


    async def stop_user(self, message=None, user_id=None):
        if message is None and user_id is None:
            return
        if message is not None:
            user = await self.return_user_if_exist(message)
        elif user_id is not None:
            user = await self.return_user_by_id(user_id)
        user.is_active = False
        await self.session.commit()


    async def get_triggers_report(self, user_id, days=7, emotion=None):
        statement = text(f"""
        with top_emotion as 
                (select '' "emotion", e.emotion "trigger", count(1) emotion_count
    from emotion_triggers t 
            join user_emotion e on t.user_emotion_id = e.user_emotion_id
                and e.user_id = {user_id} 
                and t.created_at >= now() - interval '{days} days'
                and e.emotion = '{emotion}'
    group by 1,2
    ),
    triggers as
    (select e.emotion, t.trigger, count(1) emotion_count
    from emotion_triggers t 
            join user_emotion e on t.user_emotion_id = e.user_emotion_id
                and e.user_id = {user_id} 
                and t.created_at >= now() - interval '{days} days'
                and e.emotion = '{emotion}'
    group by 1,2
    ),
    triggers_second as 
    (select t.trigger 
            , case when t.trigger_second_layer != t.trigger then t.trigger_second_layer end trigger_second_layer
            , count(1) emotion_count
    from emotion_triggers t 
            join user_emotion e on t.user_emotion_id = e.user_emotion_id
                and e.user_id = {user_id} 
                and t.created_at >= now() - interval '{days} days'
                and e.emotion = '{emotion}'
    group by 1,2
    )
    select * from top_emotion
    union all 
    select * from triggers where trigger not in (select trigger from top_emotion)
    union all 
    select * from triggers_second where trigger_second_layer not in (select trigger from triggers union all select trigger from top_emotion)  
    """)

        triggers_report = await self.session.execute(statement)
        return pd.DataFrame(triggers_report)

    async def get_triggers_report_period(self, user_id, date_first, date_second, emotion=None):
        statement = text(f"""
        with top_emotion as 
                (select '' "emotion", e.emotion "trigger", count(1) emotion_count
    from emotion_triggers t 
            join user_emotion e on t.user_emotion_id = e.user_emotion_id
                and e.user_id = {user_id} 
                and t.created_at between '{date_first}' and '{date_second} 23:59:59'
                and e.emotion = '{emotion}'
    group by 1,2
    ),
    triggers as
    (select e.emotion, t.trigger, count(1) emotion_count
    from emotion_triggers t 
            join user_emotion e on t.user_emotion_id = e.user_emotion_id
                and e.user_id = {user_id} 
                and t.created_at between '{date_first}' and '{date_second} 23:59:59'
                and e.emotion = '{emotion}'
    group by 1,2
    ),
    triggers_second as 
    (select t.trigger 
            , case when t.trigger_second_layer != t.trigger then t.trigger_second_layer end trigger_second_layer
            , count(1) emotion_count
    from emotion_triggers t 
            join user_emotion e on t.user_emotion_id = e.user_emotion_id
                and e.user_id = {user_id} 
                and t.created_at between '{date_first}' and '{date_second} 23:59:59'
                and e.emotion = '{emotion}'
    group by 1,2
    )
    select * from top_emotion
    union all 
    select * from triggers where trigger not in (select trigger from top_emotion)
    union all 
    select * from triggers_second where trigger_second_layer not in (select trigger from triggers union all select trigger from top_emotion)  
    """)

        triggers_report = await self.session.execute(statement)
        return pd.DataFrame(triggers_report)


    async def get_available_emotions_for_report(self, user_id, days=None):
        statement = text(f"""select e.emotion, count(1) emotion_count
        from emotion_triggers t 
            join user_emotion e on t.user_emotion_id = e.user_emotion_id
                and e.user_id = {user_id} and t.created_at >= now() - interval '{days} days'
        group by 1 order by 2 desc
        limit 30;""")

        emotions_available = await self.session.execute(statement)
        emotions = pd.DataFrame(emotions_available)
        if emotions.shape[0] != 0:
            return emotions.emotion.tolist()
        else:
            return None

    async def get_available_emotions_for_report_period(self, user_id, date_first: date = None, date_second: date = None):
        statement = text(f"""select e.emotion, count(1) emotion_count
        from emotion_triggers t 
            join user_emotion e on t.user_emotion_id = e.user_emotion_id
                and e.user_id = {user_id} 
                and t.created_at between '{date_first}' and '{date_second} 23:59:59'
        group by 1 order by 2 desc
        limit 30;""")

        emotions_available = await self.session.execute(statement)
        emotions = pd.DataFrame(emotions_available)
        if emotions.shape[0] != 0:
            return emotions.emotion.tolist()
        else:
            return None

    async def log_message(self, message: Message):
        try:
            user_message = UserMessages(user_id=message.from_id,
                                        text=message.text)
            self.session.add(user_message)
            await self.session.commit()
        except Exception as e:
            print(e)
            pass

    async def save_feedback(self, message: Message):
        try:
            feedback = Feedback(user_id=message.from_id,
                                feedback_text=message.text)
            self.session.add(feedback)
            await self.session.commit()
        except Exception as e:
            print(e)
            pass

    async def add_source(self, message: Message, args: str):
        if args:
            source = UserSource(user_id=message.from_id,
                                source=args)
            self.session.add(source)
            await self.session.commit()

    async def add_questionnaire_info(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        user_id = message.from_id
        user = await self.return_user_if_exist(message)
        print(user_data.get('server_current_time'))
        print(user_data.get('user_chosen_times'))
        print(user_data.get('current_time'))
        user_chosen_times = user_data.get('user_chosen_times')
        current_time = user_data.get('current_time') + ':00' if ':' not in user_data.get('current_time') \
            and user_data.get('current_time') is not None else None
        server_current_time = parser.parse(user_data.get('server_current_time')).time() \
            if user_data.get('server_current_time') else None
        current_time = parser.parse(current_time).time() \
            if current_time else None
        q = OnboardingAnswer(
            user_id=user_id,
            current_time=current_time,
            server_current_time=server_current_time,
            user_chosen_times=user_chosen_times,
            sex=user_data.get('sex'),
            age=user_data.get('age'),
            psych_difficulties=user_data.get('psych_difficulties'),
            psych_disorders=user_data.get('psych_disorders'),
            attention_metric=user_data.get('attention_metric'),
            clarity_metric=user_data.get('clarity_metric'),
            communication_metric=user_data.get('communication_metric'),
            go_to_psychiatrist=user_data.get('go_to_psychiatrist'),
            how_did_you_know_about_us=user_data.get('how_did_you_know_about_us')
        )
        self.session.add(q)
        update_statement = update(SendSchedule).filter_by(user_id=user_id).values(active=False)
        await self.session.execute(update_statement)
        await self.session.commit()
        await self.update_schedule_data(message=message, state=state)

    async def update_schedule_data(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        user_id = message.from_user
        user = await self.return_user_if_exist(message)
        user_chosen_times = user_data.get('user_chosen_times')
        server_current_time = parser.parse(user_data.get('server_current_time')).time()\
                if user_data.get('server_current_time') else None
        current_time = user_data.get('current_time') + ':00' if ':' not in user_data.get('current_time') \
                                                                and user_data.get('current_time') is not None else None
        current_time = parser.parse(current_time).time() \
            if current_time else None
        update_statement = update(SendSchedule).filter_by(user_id=user_id).values(active=False)
        await self.session.execute(update_statement)
        hour_diff = get_hour_diff(current_time, server_current_time)
        user.completed_questionnaire = True
        user.hour_diff = hour_diff
        if user_chosen_times is not None:
            for schedule_time in user_chosen_times.split('; '):
                schedule_time = schedule_time if schedule_time.endswith(':00') else schedule_time +':00'
                sched = SendSchedule(user_id=user_id,
                                     send_time_server=add_hours_to_time(parser.parse(schedule_time).time(), - hour_diff),
                                     send_type=SendTypes.EMOTION_COLLECT,
                                     active=True,
                                     )
                self.session.add(sched)
        sched_weekly = SendSchedule(user_id=user_id,
                                    send_time_server=add_hours_to_time(time(21, 0), - hour_diff),
                                    send_type=SendTypes.WEEKLY_REPORT,
                                    active=True,
                                    days_of_week='7',
                                    )
        self.session.add(sched_weekly)
        await self.session.commit()


    async def get_pushes_to_send(self):
        statement = text(f"""select distinct s.send_schedule_id, s.user_id, s.send_type, s.custom_text
        from send_schedule s
            left join sent_pushes p on s.send_schedule_id = p.send_schedule_id
                and p.created_at_date = current_date
        where s.active 
            and (s.created_at::time < send_time_server or s.created_at < current_date)
            and s.send_time_server <= current_time
            and (s.days_of_week is null or s.days_of_week ~ extract(isodow from current_date)::text
                or s.date_to_send = current_date)
            and p.send_schedule_id is null
        limit 30;""").columns(SendSchedule.send_schedule_id, SendSchedule.user_id,
                              SendSchedule.send_type, SendSchedule.custom_text,
                              )

        pushes_to_send = await self.session.execute(statement)
        return pd.DataFrame(pushes_to_send)


    async def store_sent_pushes(self, user_id, send_schedule_ids, error=None):
        for send_schedule_id in send_schedule_ids:
            sent_push = SentPushes(user_id=user_id,
                                   send_schedule_id=send_schedule_id,
                                   error=error)
            self.session.add(sent_push)
        await self.session.commit()
