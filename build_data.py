import re,json
s=open('raw/rsc3.txt').read()
dec=json.JSONDecoder()
i=s.find('"selectedEvents":[')
arr,_=dec.raw_decode(s,i+len('"selectedEvents":'))
print('selectedEvents',len(arr))
vid={}
def vname(v):
    if isinstance(v,dict):
        vid[v['id']]=v; return v
    return v
for o in arr:
    v=(o.get('location') or {}).get('venue')
    if isinstance(v,dict): vid[v['id']]=v
# also collect any venue objects anywhere
for m in re.finditer(r'\{"createdAt"',s):
    try:o,_=dec.raw_decode(s,m.start())
    except: continue
    if 'coordinates' in o and 'name' in o: vid[o['id']]=o
def resolve(v,depth=0):
    if isinstance(v,dict): return v
    if isinstance(v,str):
        m=re.match(r'\$6:1:props:children:props:blocks:0:selectedEvents:(\d+):location:venue',v)
        if m and depth<5: return resolve(arr[int(m.group(1))]['location']['venue'],depth+1)
        return vid.get(v)
    return None
venues={}; events=[]
for o in arr:
    loc=o.get('location') or {}
    v=resolve(loc.get('venue'))
    vn=v['name'] if v else None
    if v:
        c=v.get('coordinates') or {}
        venues.setdefault(vn,{'name':vn,'lat':c.get('latitude'),'lng':c.get('longitude'),'src':'RAS'})
    sess=[{'start':x['startTime'],'end':x['endTime']} for x in o['schedule'] if x['date'].startswith('2026-10-03') and x.get('startTime')]
    events.append({'title':o['title'],'slug':o['slug'],'venue':vn or 'TBA','detail':loc.get('locationDetails') if isinstance(loc.get('locationDetails'),str) else None,
      'sessions':sess,'free':bool((o.get('ticketing') or {}).get('isFree')),'summary':o.get('excerpt') or ''})
print(len(events), sum(1 for e in events if e['venue']=='TBA'))
json.dump({'events':events,'venues':venues},open('raw/ras_events.json','w'),indent=1)
for k,v in venues.items(): print(k,v['lat'],v['lng'])
print([ (e['title'],e['detail']) for e in events if e['detail']][:20])
