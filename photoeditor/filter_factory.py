from photoeditor.base.filter import Filter
#TODO: find a way to find every descovered package using one import
try:
    from photoeditor.basic_filters import *
except Exception:
    pass


def get_all_filters():
    return {f.__name__:f for f in Filter.__subclasses__()}