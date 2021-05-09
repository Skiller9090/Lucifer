from .Debug import Debug
from .Utils import generate_percent_breakdown


class PercentageDebug(Debug):
    def generate_display(self):
        data = super().generate_display()
        data += generate_percent_breakdown(self.statistics)
        return data
