from peewee import CharField, Model

import app.core.consts as consts

class Voice(Model):
    name = CharField(unique=True)
    language_code = CharField()

    class Meta:
        database = consts.db