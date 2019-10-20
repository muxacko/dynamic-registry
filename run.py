from registry import Registry


class Hello(object):
    value: str


class World(object):
    value: str


registry = Registry()
registry.register(Hello)
registry.register(World)

registry.run()


