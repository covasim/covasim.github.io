"""
Download the icons used on the Covasim website and save recolored local copies.

These were previously loaded from icongr.am, which went offline in 2026-09.
FontAwesome icons are v4.7 (via encharm/Font-Awesome-SVG-PNG); Octicons are
the 16px versions from @primer/octicons. Each icon is saved once per color as
<set>/<name>-<color>.svg, matching the paths used in index.qmd. Rerun after adding an icon or
color below.
"""
import re
import urllib.request
from pathlib import Path

sources = dict(
    fontawesome = 'https://raw.githubusercontent.com/encharm/Font-Awesome-SVG-PNG/master/black/svg/{name}.svg',
    octicons    = 'https://unpkg.com/@primer/octicons/build/svg/{name}-16.svg',
)

icons = {
    'ffffff': ['octicons/code', 'fontawesome/lightbulb-o', 'octicons/mark-github'], # Top buttons
}

folder = Path(__file__).parent
for color, paths in icons.items():
    for path in paths:
        iconset, name = path.split('/')
        url = sources[iconset].format(name=name)
        svg = urllib.request.urlopen(url).read().decode()
        svg = re.sub(r'<\?xml[^>]*>\s*', '', svg) # Strip the XML declaration
        svg = svg.replace('<svg ', f'<svg fill="#{color}" ', 1) # Paths inherit the fill
        outfile = folder / iconset / f'{name}-{color}.svg'
        outfile.parent.mkdir(exist_ok=True)
        outfile.write_text(svg.strip() + '\n')
        print(f'Saved {outfile.relative_to(folder)}')
