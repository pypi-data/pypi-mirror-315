from importlib import import_module
from typing import Callable, Iterable


class Registry:
    def __init__(self, eager: set | None = None, lazy: dict | None = None):
        self._eager = eager or set()
        self._lazy = lazy or dict()
        self._dict = dict()

    def __len__(self):
        return len(self._dict)

    def update_eager(self, locations: set):
        self._eager.update(locations)

    def update_lazy(self, locations: dict):
        self._lazy.update(locations)

    @property
    def module_dict(self):
        return self._dict

    @property
    def eager(self):
        return self._eager

    @property
    def lazy(self):
        return self._lazy

    def import_locations(self, locations: Iterable):
        for location in locations:
            import_module(location)

    def get(self, name: str, key: str | None = "module"):
        if name not in self._dict:
            if name in self._lazy:
                self.import_locations([self._lazy[name]])
            else:
                self.import_locations(self._eager)
        return self._dict[name] if key is None else self._dict[name].get(key, None)

    def build(
        self,
        name: str,
        func: str | Callable | None = None,
        args: tuple = (),
        kwargs: dict = {},
    ):
        module = self.get(name)
        if func is None:
            return module(*args, **kwargs)
        elif isinstance(func, str):
            return getattr(module, func)(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    def __str__(self):
        result = []
        for name, value in self._dict.items():
            module = value["module"]
            module_type = type(module).__name__
            module_info = f"{name}: {module_type}({module})"
            result.append(module_info)

        return "\n".join(result)

    def _register(self, *, name: str | list[str] | None = None, module, **kwargs):
        name = name or module.__name__
        if isinstance(name, str):
            names = [name]
        for name in names:
            self._dict[name] = dict(module=module) | kwargs

    def register(self, name: str | list[str] | None = None, module=None, **kwargs):
        if module is not None:
            self._register(name=name, module=module, **kwargs)
            return module

        def _register(module):
            self._register(name=name, module=module, **kwargs)
            return module

        return _register
