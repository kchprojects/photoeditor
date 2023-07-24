from photoeditor.base.filter import Filter,CombinedFilter
#TODO: find a way to find every descovered package using one import
try:
    from photoeditor.basic_filters import *
except Exception:
    pass

_hidden_filters = [CombinedFilter]

def get_all_filters():
    return {f.__name__:f for f in Filter.__subclasses__() if f not in _hidden_filters}