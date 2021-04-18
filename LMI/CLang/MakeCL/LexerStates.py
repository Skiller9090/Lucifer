from enum import Enum


class States(Enum):
    Root = 0
    Keyword = 2
    String = 3
    Comment = 4
