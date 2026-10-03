import json,math
d=json.load(open('raw/ras_events.json')); g=json.load(open('raw/georef_est.json'))
def dist(a,b): return math.hypot((a[0]-b[0])*111320,(a[1]-b[1])*111320*0.8483)
L=[]
def add(name,typ,lat,lng,src,approx=False,note=None):
    L.append({'id':name,'name':name,'type':typ,'lat':round(lat,6),'lng':round(lng,6),'approx':approx,'src':src,**({'note':note} if note else {})})
for n,v in d['venues'].items():
    if n in('TBA','AgVenture Hill','Roving – Gate 1') or v['lat'] is None: continue
    add(n,'venue',v['lat'],v['lng'],'RAS venue data')
add('Gate 1 area (roving)','venue',-31.978094,115.784559,'RAS venue data')
MAP='Official 2026 show map, georeferenced (±20 m)'
add('AgVenture Hill','venue',*g['AgVenture Hill'],MAP)
add('Sideshow Alley','ride',*g['Sideshow Alley'],MAP)
add('Kids Luna Park','ride',*g['Kids Luna Park'],MAP)
add('Arena Surrounds rides','ride',*g['Arena Surrounds rides'],MAP)
add('Global Stage Precinct rides','ride',*g['Global Stage Precinct rides'],MAP)
add('Gate 10 Lawn rides','ride',*g['Gate 10 Lawn rides'],MAP)
OSM='OpenStreetMap'
add('Gate 1 (Graylands Rd)','gate',-31.978026,115.784481,OSM)
add('Gate 10 (Ashton Ave)','gate',-31.973683,115.788015,OSM)
add('Station Gate (Showgrounds station)','gate',-31.976863,115.786405,OSM)
add('Showgrounds train station','station',-31.977064,115.786883,OSM+' (Transperth)')
add('Claremont train station','station',-31.980725,115.781449,OSM+' (Transperth)')
for k in ["Woody's Bar",'Cattle Lane Bar','Good Fields','Sweetie Lane','Bush BBQ','Taste Street (Emporium)']: add(k,'food',*g[k],MAP)
add('Long Paddock food (north)','food',*g['Long Paddock (food, north)'],MAP)
add('Long Paddock food (south)','food',*g['Long Paddock (food, south)'],MAP)
add('Dairy Land (food samples)','food',-31.973483,115.787558,'RAS venue data')
venues=[x for x in L if x['type']=='venue']
for t in [(-31.977471,115.785397),(-31.973864,115.785680)]:
    nv=min(venues,key=lambda v:dist((v['lat'],v['lng']),t))
    add('Toilets – near '+nv['name'],'toilet',*t,OSM)
P='OpenStreetMap car park – check show signage for public access'
add('Car park – Graylands Rd (near Gate 6)','parking',-31.972603,115.783416,P)
add('Car park – Graylands Rd (near Gate 5)','parking',-31.973414,115.783478,P)
add('Car park – Ashton Ave (east of Gate 10)','parking',-31.97308,115.788864,P)
ids={x['id'] for x in L}
over={'Horse Competitions':'Main Arena','Police Pavilion':'Police Pavilion','Yellow Brick Road':'AgVenture Hill',
 'Creative Arts and Cookery Demonstrations':'Creative Arts & Cookery','Outback Encounters':'Rodeo Drive','Whip Cracking':'Rodeo Drive',
 'The Kitchen - Sticky Pork & Crunchy Apple Slaw':'The Long Paddock Stage','The Kitchen - The Spud Kings’ Loaded Potato Showdown with Tony Galati':'The Long Paddock Stage'}
roving={'Nova Supernovas','Spudette & Lady Carrotene Mascots'}
placed=[]
for e in d['events']:
    if e['venue']=='Roving – Gate 1': e['venue']='Gate 1 area (roving)'
    if e['venue']=='TBA' and e['title'] in over: e['venue']=over[e['title']]; e['placed']=True; placed.append(e['title'])
    if e['title'] in roving: e['venue']='Roving around the showground'; e['roving']=True
    e['venueId']=e['venue'] if e['venue'] in ids else None
    e.pop('detail',None)
miss=[e['title'] for e in d['events'] if not e['venueId']]
print('locations',len(L),'placed',len(placed),'no venue:',miss)
json.dump({'date':'2026-10-03','source':'https://raswa.org.au/perth-royal-show/show-schedule-3-oct','mapPdf':'https://cdn.raswa.org.au/media/6b459dc8-1a96-4301-bbc7-203a03055381.pdf',
 'events':d['events'],'locations':L},open('data.json','w'),ensure_ascii=False,separators=(',',':'))
