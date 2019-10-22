import inspect
from typing import Type, List

from flask import Flask
from flask_cors import CORS
from sqlalchemy import Column, Table, MetaData, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.sql.type_api import TypeEngine

from dataclasses import Meta


def print_list(lst):
    result = [str(l) for l in lst]
    return '<br>'.join(result)


class Registry(object):

    _metas = {}
    _session = None

    def __init__(self, session: Session):
        self._metas = {}
        self._models = {}
        self._session = session
        self._orm_metadata = MetaData(bind=session.get_bind())
        self._Base = declarative_base()

    def register(self, type_: Type) -> Meta:
        meta = self._get_meta_by_type(type_)
        self._metas[meta.name] = meta
        self._init_entity_storage(meta)
        return meta

    def metas(self):
        return self._metas.items()

    def insert(self, obj: any) -> any:
        # сгенерировать запрос на вставку данных, исходя из структуры объекта
        type_ = type(obj)
        meta = self.register(type_)
        model = self._meta_to_orm_model(meta)
        self._register_orm_model(meta, model)
        model_instance = model()
        self._update_model_instance_from_object(model_instance, obj)
        self._session.add(model_instance)
        self._session.commit()

    def list(self, type_: type) -> List[any]:
        meta = self._get_meta_by_type(type_)
        model = self._get_model_by_meta(meta)
        return list(map(self._serialize_model_instance, self._session.query(model).all()))

    def get(self, type_: type, key: any) -> List[any]:
        meta = self._get_meta_by_type(type_)
        model = self._get_model_by_meta(meta)
        return self._serialize_model_instance(self._session.query(model).filter_by(id=key).one())

    def _init_entity_storage(self, meta: Meta):
        # сконструировать Table или модель...
        # динамически создать таблицу
        columns = []

        for fname, ftype in meta.attributes.items():
            column = Column(fname, self._meta_type_to_orm_column(ftype), primary_key=fname.lower() == 'id')
            columns.append(column)

        table = Table(meta.name, self._orm_metadata, *columns)
        table.create()

    def _get_meta_by_type(self, type_: Type) -> Meta:
        result = Meta(name=type_.__name__, origin=type_)
        for fname, ftype in type_.__annotations__.items():
            result.attributes[fname] = self._simple_type_to_meta_type(ftype)
        return result

    @staticmethod
    def _simple_type_to_meta_type(ftype: type):
        if ftype.__name__ == 'int':
            return Meta.INT
        else:
            return Meta.STRING

    @staticmethod
    def _meta_type_to_orm_column(meta_type: int):
        if meta_type == Meta.INT:
            return Integer
        else:
            return String

    # def run(self):
    #     app = Flask('Registry')
    #     CORS(app)
    #
    #     @app.route('/')
    #     def home():
    #         names = [f'<a href="/{n}">{n}</a>' for n in self._metas.keys()]
    #         return print_list(names)
    #
    #     @app.route('/<entity_name>')
    #     def attributes(entity_name: str):
    #         result = [
    #             print_list(inspect.getmembers(self._metas[entity_name]))
    #         ]
    #         return print_list(result)
    #
    #     app.run()
    #
    def _meta_to_orm_model(self, meta: Meta):
        dict_ = {'__tablename__': meta.name.lower()}
        for fname, ftype in meta.attributes.items():
            dict_[fname] = Column(self._meta_type_to_orm_column(ftype),
                                  primary_key=fname.lower() == 'id')
        result = type(
            f'{meta.name}Model',
            (self._Base,),
            dict_)
        return result

    @staticmethod
    def _update_model_from_dict(model, dict_):
        for fname in dict_.keys():
            if hasattr(model, fname):
                setattr(model, fname, dict_[fname])

    def _update_model_instance_from_object(self, model, obj):
        dict_ = self._obj_to_dict(obj)
        self._update_model_from_dict(model, dict_)

    def _get_meta_by_object(self, obj) -> Meta:
        return self._metas[type(obj).__name__]

    def _obj_to_dict(self, obj) -> dict:
        meta = self._get_meta_by_object(obj)
        result = {}
        for fname in meta.attributes.keys():
            result[fname] = getattr(obj, fname, None)
        return result

    def _get_model_by_meta(self, meta):
        return self._models[meta.name]

    def _register_orm_model(self, meta, model):
        self._models[meta.name] = model

    def _serialize_model_instance(self, model):
        meta = self._get_meta_by_model(type(model))
        type_ = self._get_type_by_meta(meta)
        result = type_()
        for fname in meta.attributes.keys():
            setattr(result, fname, getattr(model, fname, None))
        return result

    def _get_meta_by_model(self, model) -> Meta:
        for name, m in self._models.items():
            if m == model:
                return self._metas[name]

    @staticmethod
    def _get_type_by_meta(meta: Meta) -> type:
        return meta.origin
