from photoeditor.base.filter import Filter
try:
    from photoeditor.basic_filters import *
except Exception:
    pass


all_filters = {f.__name__:f for f in Filter.__subclasses__()}