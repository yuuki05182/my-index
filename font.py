import matplotlib.font_manager as fm

for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'Gothic' in font or 'Noto' in font or 'Yu' in font or 'IPA' in font:
        print(font)
