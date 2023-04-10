from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer, BigInteger
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy import Boolean
from sqlalchemy import JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class SendTypes:
    EMOTION_COLLECT='Emotion collect'
    DAILY_REPORT='Daily report'
    WEEKLY_REPORT='Weekly report'

class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    completed_questionnaire = Column(Boolean, default=False)
    hour_diff = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    premium_until = Column(DateTime(timezone=True))

    __mapper_args__ = {"eager_defaults": True}


class SendSchedule(Base):
    __tablename__ = "send_schedule"
    send_schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), index=True)
    user = relationship("User")
    send_time_server = Column(Time, nullable=False)
    send_type = Column(String)
    active = Column(Boolean)
    days_of_week = Column(String)
    date_to_send = Column(Date)
    custom_text = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}


class SentPushes(Base):
    __tablename__ = "sent_pushes"
    sent_push_id = Column(Integer, primary_key=True, autoincrement=True)
    send_schedule_id = Column(Integer, ForeignKey("send_schedule.send_schedule_id"), index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), index=True)
    error = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    created_at_date = Column(Date, server_default=func.now(), index=True)

    __mapper_args__ = {"eager_defaults": True}


class OnboardingAnswer(Base):
    __tablename__ = 'onboarding_answer'
    questionnaire_answer_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), index=True)
    user = relationship("User")
    sex = Column(String)
    age = Column(String)
    current_time = Column(Time)
    server_current_time = Column(Time)
    user_chosen_times = Column(String)
    psych_difficulties = Column(String)
    psych_disorders = Column(String)
    attention_metric = Column(String)
    clarity_metric = Column(String)
    communication_metric = Column(String)
    go_to_psychiatrist = Column(String)
    how_did_you_know_about_us = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserEmotion(Base):
    __tablename__ = "user_emotion"
    user_emotion_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), index=True)
    user = relationship("User")
    emotion = Column(String)
    emotion_ratio = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}


class UserMessages(Base):
    __tablename__ = 'user_messages'
    user_message_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"))
    text = Column(String)
    sent_timestamp = Column(DateTime, server_default=func.now())
    sent_date = Column(Date, server_default=func.now())


class EmotionTrigger(Base):
    __tablename__ = 'emotion_triggers'
    trigger_id = Column(Integer, primary_key=True, autoincrement=True)
    user_emotion_id = Column(Integer, ForeignKey("user_emotion.user_emotion_id"))
    trigger = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    trigger_second_layer = Column(String)


class UserSource(Base):
    __tablename__ = 'user_source'
    user_source_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    source = Column(String)
    created_at = Column(DateTime, server_default=func.now())


class Feedback(Base):
    __tablename__ = 'feedback'
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    feedback_text = Column(String)
    created_at = Column(DateTime, server_default=func.now())
