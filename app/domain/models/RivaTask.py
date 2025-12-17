from datetime import datetime
from email.policy import default
from peewee import CharField, DateTimeField, IntegerField, Model, TextField

import app.core.consts as consts

class RivaTask(Model):
    text = TextField(null=True)
    voice_name = CharField(null=True)
    language_code = CharField(null=True)
    status = CharField(null=True)
    started_at = DateTimeField(null=True)
    completed_at = DateTimeField(null=True)
    processing_time = IntegerField(null=True)
    audio_duration = IntegerField(null=True)
    audio_path = CharField(null = True)
    error_message = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)


    class Meta:
        database = consts.db