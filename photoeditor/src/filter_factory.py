from photoeditor.base.filter import Filter
from photoeditor.filters import *


all_filters = {f.__name__:f for f in Filter.__subclasses__()}