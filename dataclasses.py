from typing import Dict


class Meta(object):
    STRING = 1
    INT = 2
    DATE = 3
    DATETIME = 4

    """Мета-описание сущности"""
    name: str
    """имя сущности"""
    namespace: str
    """простратнство, которому принадлежить сущность"""
    origin: any
    """исходный тип, на базе которого создана мета"""
    attributes: Dict[str, int]
    """список атрибутов сущности"""

    def __init__(self, name, namespace='', origin: any = None):
        self.name = name
        self.namespace = namespace
        self.origin = origin
        self.attributes = {'id': self.STRING}
