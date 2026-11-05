import os
NAV = '{{Countries in Lurandia}}'
def stub(name, area, lead):
    d = os.path.join(name)
    os.makedirs(d, exist_ok=True)
    c = f"""{{{{Infobox country
|common_name                 = {name}
|image_map                   = Location of {name}.svg
|map_caption                 = Location of {name}
|area_km2                    = {area}
}}}}

{lead}

{{{{Stub}}}}
{NAV}
[[Category:Lurandia]]
[[Category:Countries in Lurandia]]
"""
    open(os.path.join(d, f'{name}.mediawiki'), 'w', encoding='utf-8', newline='\n').write(c)
    print('wrote', name, len(c))

stub('Kalanua', 2390324,
     "'''Kalanua''' is a country in the far south-east of [[Lurandia]]. It covers an area of approximately 2,390,324 km², making it one of the largest countries of the continent's south. It shares no land border with another Lurandian state.")
stub('Kawalidipa', 1508519,
     "'''Kawalidipa''' is a country in the south of [[Lurandia]]. It covers an area of approximately 1,508,519 km² and borders [[Louyang]], [[Mishko]], [[Nawat]], [[Nuuchi]], [[Tuvayo]], the [[United Midlands]] and [[Winnipi]].")
stub('Markland', 2313378,
     "'''Markland''' is a country in the far south of [[Lurandia]]. It covers an area of approximately 2,313,378 km² and borders [[Neakyrena]] and [[Winnipi]].")
stub('Mishko', 439724,
     "'''Mishko''' is a country in the south of [[Lurandia]]. It covers an area of approximately 439,724 km² and borders [[Kaneda]], [[Kawalidipa]], [[Tuvayo]] and [[Winnipi]].")
stub('Nawat', 697385,
     "'''Nawat''' is a country in central [[Lurandia]]. It covers an area of approximately 697,385 km² and borders [[Kawalidipa]], [[Louyang]] and the [[United Midlands]].")
stub('Neakyrena', 483153,
     "'''Neakyrena''' is a country in the far south of [[Lurandia]]. It covers an area of approximately 483,153 km² and borders [[Markland]] and [[Winnipi]].")
stub('Nuuchi', 452603,
     "'''Nuuchi''' is a country in the south of [[Lurandia]]. It covers an area of approximately 452,603 km² and borders [[Kawalidipa]], [[Tuvayo]] and [[Winnipi]].")
stub('Tuvayo', 530802,
     "'''Tuvayo''' is a country in the south of [[Lurandia]]. It covers an area of approximately 530,802 km² and borders [[Kawalidipa]], [[Mishko]], [[Nuuchi]] and [[Winnipi]].")
