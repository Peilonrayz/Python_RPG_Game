from collections import namedtuple as _namedtuple


_MixinVariable = _namedtuple('MixinVariable', 'name ext_name type')


class _MixinMeta(type):
    def __new__(mcs, typename, bases, ns):
        if ns.get('_root', False):
            return super().__new__(mcs, typename, bases, ns)
        variables = []
        for base in bases:
            variables.extend(getattr(base, f'_{base.__name__}__variables', []))
        types = ns.get('__annotations__', {})
        variables += [
            _MixinVariable(name, ns.pop(name, name), type_)
            for name, type_ in types.items()
        ]

        variables_by_name = {v.name: v for v in variables}
        overwritten_variables = []
        for v in reversed(variables):
            v = variables_by_name.pop(v.name, None)
            if v is None:
                continue
            overwritten_variables.append(v)

        ns[f'_{typename}__variables'] = list(reversed(variables))
        return type.__new__(mcs, typename, bases, ns)


class Mixin(metaclass=_MixinMeta):
    _root = True

    @classmethod
    def from_external(cls, entity: dict):
        instance = cls()
        for variable in getattr(instance, f'_{cls.__name__}__variables'):
            setattr(instance, variable.name, entity[variable.ext_name])
        return instance

    @classmethod
    def from_internal(cls, entity: dict):
        instance = cls()
        for variable in getattr(instance, f'_{cls.__name__}__variables'):
            setattr(instance, variable.name, entity[variable.name])
        return instance

    def to_external(self):
        return {
            variable.ext_name: getattr(self, variable.name, None)
            for variable in getattr(self, f'_{type(self).__name__}__variables')
        }

    def to_internal(self):
        return {
            variable.name: getattr(self, variable.name, None)
            for variable in getattr(self, f'_{type(self).__name__}__variables')
        }
