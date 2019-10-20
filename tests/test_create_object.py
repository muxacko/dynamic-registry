from dataclasses import Meta
from registry import Registry


class Hello(object):
    value: str


class World(object):
    code: str
    name: str


def test_init_registry(registry: Registry):
    assert registry is not None


def test_type_to_meta(registry: Registry):
    meta = registry._type_to_meta(World)
    assert meta is not None
    assert meta.name == World.__name__
    assert meta.attributes is not None
    assert len(meta.attributes) == 2
    assert meta.attributes['code'] == Meta.STRING
    assert meta.attributes['name'] == Meta.STRING


def test_register_entity(registry: Registry):
    registry.register(Hello)
    assert len(registry.metas()) == 1
    registry.register(World)
    assert len(registry.metas()) == 2


def test_create_entity_instance(registry: Registry):
    h = Hello()
    h.value = 'Hello'

    new_h = registry.insert(h)

    assert len(registry.list(Hello)) == 1
    assert registry.get(Hello, new_h.id)
