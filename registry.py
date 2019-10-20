import inspect
from typing import Type

from flask import Flask
from flask_cors import CORS
from sqlalchemy.orm import Session

from dataclasses import Meta


def print_list(lst):
    result = [str(l) for l in lst]
    return '<br>'.join(result)


class Registry(object):

    _metas = {}
    _session = None

    def __init__(self, session: Session):
        self._metas = {}
        self._session = session

    def register(self, type_: Type):
        meta = self._type_to_meta(type_)
        self._metas[meta.name] = meta
        self._init_entity_storage(meta)

    def metas(self):
        return self._metas.items()

    def insert(self, obj: any) -> any:
        # сгенерировать запрос на вставку данных, исходя из структуры объекта
        meta = self._metas[type(obj).__name__]
        # сконструтировать модель или сделать sql на инсерт
        # предварительно создать структуру в БД
        # self._session.

    def _init_entity_storage(self, meta: Meta):
        # сконструировать Table или модель...
        # динамически создать таблицу
        pass

    def _type_to_meta(self, type_: Type) -> Meta:
        pass

    def run(self):
        app = Flask('Registry')
        CORS(app)

        @app.route('/')
        def home():
            names = [f'<a href="/{n}">{n}</a>' for n in self._metas.keys()]
            return print_list(names)

        @app.route('/<entity_name>')
        def attributes(entity_name: str):
            result = [
                print_list(inspect.getmembers(self._metas[entity_name]))
            ]
            return print_list(result)

        app.run()
