from .Basic import Basic
from .Utils import generate_percent_breakdown


class PercentageBasic(Basic):
    def generate_display(self):
        data = super().generate_display()
        data += generate_percent_breakdown(self.statistics)
        return data
