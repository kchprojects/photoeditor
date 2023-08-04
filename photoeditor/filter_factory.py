from photoeditor.base.filter import Filter,CombinedFilter,SegmentationFilter
#TODO: find a way to find every descovered package using one import
try:
    from photoeditor.basic_filters import *
except Exception:
    pass

# try:
from photoeditor.segmentation import *
# except Exception e:
#     pass

_hidden_filters = [CombinedFilter]

def get_all_filters():
    return {f.__name__:f for f in Filter.__subclasses__() if f not in _hidden_filters}

def get_segmentation_filters():
    return {f.__name__:f for f in SegmentationFilter.__subclasses__() if f not in _hidden_filters}