from .Short import Short
from .Utils import generate_percent_breakdown


class PercentageShort(Short):
    def generate_display(self):
        data = super().generate_display()
        data += generate_percent_breakdown(self.statistics)
        return data
