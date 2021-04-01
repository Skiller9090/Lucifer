from enum import Enum


class States(Enum):
    Root = 0
    InFileDirectiveInitializer = 1
    InFileDirective = 2
    InFileDirectiveAndLink = 3
