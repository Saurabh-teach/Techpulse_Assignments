import json
from datetime import datetime
from abc import ABC, abstractmethod


class PluginRegistry:
    _plugins = []

    @classmethod
    def register(cls, plugin_cls):
        cls._plugins.append(plugin_cls.__name__)

    @classmethod
    def list_plugins(cls):
        return cls._plugins

class Loggable:

    def log(self, message: str, level: str = "INFO") -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] [{self.__class__.__name__}] {message}")

    def log_error(self, message: str) -> None:
        self.log(message, level="ERROR")

    def log_debug(self, message: str) -> None:
        self.log(message, level="DEBUG")



class Serializable:

    def to_dict(self) -> dict:
        
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent )

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(**data)

class Cacheable:

    def __init__(self, *args, **kwargs):
        self._cache = {}
        super().__init__(*args, **kwargs)  

    def cache_set(self, key: str, value):
        self._cache[key] = value

    def cache_get(self, key: str, default=None):
        return self._cache.get(key, default)

    def cache_clear(self):
        self._cache.clear()



class ValidationError(Exception):
    pass


class Validatable(ABC):

    @abstractmethod
    def validate(self) -> bool:
        pass

    def validate_or_raise(self):
        if not self.validate():
            raise ValidationError("Validation failed")


class Plugin:

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.enabled = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PluginRegistry.register(cls)


class DataProcessor(Loggable, Serializable, Validatable, Plugin):

    def __init__(self, name, version="1.0.0", data_format="json"):
        self.data_format = data_format
        super().__init__(name, version)

    def validate(self) -> bool:
        return isinstance(self.name, str) and len(self.name) > 0


class CachePlugin(Cacheable, Loggable, Validatable, Plugin):

    def validate(self) -> bool:
        return self.enabled in [True, False]


class FullFeaturedPlugin(Cacheable, Loggable, Serializable, Validatable, Plugin):

    def validate(self) -> bool:
        return True        


print(DataProcessor.__mro__)

p = DataProcessor("test")
p.log("test")

p = DataProcessor("test")

print(p.to_dict())


c = CachePlugin("cache1")
c.cache_set("k", "v")
print(c.cache_get("k"))

print(c.validate())

print(PluginRegistry.list_plugins())

f = FullFeaturedPlugin("full")

f.log("hello")        
f.cache_set("x", 1)   
f.to_json()           
f.validate()          
f.enable()           

