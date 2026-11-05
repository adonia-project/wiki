import os
ART = r'B:\02_GIT CONNECTED\wiki\articles\Countries'
NAV = '{{Countries in Lurandia}}'
def w(name, content):
    d = os.path.join(ART, name)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f'{name}.mediawiki'), 'w', encoding='utf-8', newline='\n').write(content)
    print('synced', name, len(content))

w('Amiera', """{{Infobox country
|common_name                 = Amiera
|image_map                   = Location of Amiera.svg
|map_caption                 = Location of Amiera
|area_km2                    = 101662
}}

'''Amiera''' is a small country in northern [[Lurandia]]. It covers an area of approximately 101,662 km² and borders [[Etawa]] and [[Sinchew]].

{{Stub}}
""" + NAV + """
[[Category:Lurandia]]
[[Category:Countries in Lurandia]]
""")

w('Etawa', """{{Infobox country
|common_name                 = Etawa
|image_map                   = Location of Etawa.svg
|map_caption                 = Location of Etawa
|area_km2                    = 588942
}}

'''Etawa''' is a country in northern [[Lurandia]]. It covers an area of approximately 588,942 km² and borders [[Amiera]], [[Louyang]], [[Sinchew]] and the [[United Midlands]].

{{Stub}}
""" + NAV + """
[[Category:Lurandia]]
[[Category:Countries in Lurandia]]
""")

w('Winnipi', """{{Infobox country
|common_name                 = Winnipi
|image_map                   = Location of Winnipi.svg
|map_caption                 = Location of Winnipi
|area_km2                    = 7431406
}}

'''Winnipi''' is a country in the far south of [[Lurandia]]. It is the second-largest country on the continent after [[Louyang]], covering an area of approximately 7,431,406 km². Its population is predominantly [[w:Cree|Cree]] and [[w:Anishinaabe|Anishinaabe]]. It borders [[Kaneda]], [[Kavik]], [[Kawalidipa]], [[Markland]], [[Mishko]], [[Neakyrena]], [[Nuuchi]], [[Tuvayo]] and the [[United Midlands]].

{{Stub}}
""" + NAV + """
[[Category:Lurandia]]
[[Category:Countries in Lurandia]]
""")

w('Sinchew', """{{Infobox country
|common_name                 = Sinchew
|image_map                   = Location of Sinchew.svg
|map_caption                 = Location of Sinchew
|area_km2                    = 2017722
}}

'''Sinchew''' is a country in northern [[Lurandia]]. It covers an area of approximately 2,017,722 km², making it one of the larger countries of the continent's north. It borders [[Amiera]], [[Balboa]], [[Etawa]] and [[Louyang]].

{{Stub}}
""" + NAV + """
[[Category:Lurandia]]
[[Category:Countries in Lurandia]]
""")

# UM: append borders + navbox to existing local file
p = os.path.join(ART, 'United Midlands', 'United Midlands.mediawiki')
c = open(p, encoding='utf-8').read()
old = "a colonial possession of the [[Kingdom of Merica]]."
if old in c and 'It borders [[Etawa]]' not in c:
    c = c.replace(old, old + " It borders [[Etawa]], [[Kawalidipa]], [[Louyang]], [[Nawat]] and [[Winnipi]].")
if NAV not in c:
    c = c.replace('{{Stub}}', '{{Stub}}\n' + NAV)
open(p, 'w', encoding='utf-8', newline='\n').write(c)
print('synced United Midlands', len(c))
