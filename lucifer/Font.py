from tkinter import font as tk_fonts


class FontFind:
    def find_font(self, names):
        for name in names:
            if name.lower() in (x.lower() for x in tk_fonts.names(root=self)):
                font = tk_fonts.Font(name=name, exists=True, root=self)
                return font.actual()['family']
            elif name.lower() in (x.lower()
                                  for x in tk_fonts.families(root=self)):
                break
        else:
            return None
        return name
