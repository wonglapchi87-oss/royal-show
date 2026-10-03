import json,math
d=json.load(open('raw/osm_full.json'))['elements']
nodes={e['id']:(e['lat'],e['lon']) for e in d if e['type']=='node'}
S,N,W,E=-31.9805,-31.9695,115.7800,115.7905
skip={'motorway','motorway_link','construction','proposed','raceway','bus_guideway'}
idx={};pts=[];names=[];nameidx={};adj={}
def ni(n):
    if n not in idx: idx[n]=len(pts); pts.append([round(nodes[n][0],6),round(nodes[n][1],6)])
    return idx[n]
def dist(a,b):
    return math.hypot((a[0]-b[0])*111320,(a[1]-b[1])*111320*math.cos(math.radians(31.975)))
ways=0
pub={'Gate 1','Gate 10','Train Station Gate'}
blocked={e['id'] for e in d if e['type']=='node' and e.get('tags',{}).get('barrier') in ('gate','lift_gate','fence','wall') and e['tags'].get('name') not in pub}
print('blocked gate nodes',len(blocked))
for e in d:
    t=e.get('tags',{})
    if e['type']!='way' or 'highway' not in t or t['highway'] in skip: continue
    if t.get('foot')=='no' or t.get('access')=='no' and t.get('foot') not in('yes','designated','permissive'): continue
    ns=[n for n in e['nodes'] if n in nodes]
    segs_ok=lambda a,b: a not in blocked and b not in blocked
    if not any(S<nodes[n][0]<N and W<nodes[n][1]<E for n in ns): continue
    nm=t.get('name') or {'footway':'footpath','path':'path','steps':'steps','service':'service road','cycleway':'path','pedestrian':'walkway'}.get(t['highway'],'road')
    if nm not in nameidx: nameidx[nm]=len(names); names.append(nm)
    k=nameidx[nm]; ways+=1
    for a,b in zip(ns,ns[1:]):
        if not segs_ok(a,b): continue
        i,j=ni(a),ni(b); w=round(dist(pts[i],pts[j]),1)
        if t['highway']=='steps': w*=1.5
        adj.setdefault(i,[]).append([j,w,k]); adj.setdefault(j,[]).append([i,w,k])
# keep largest connected component
seen=set();best=[]
for s in range(len(pts)):
    if s in seen or s not in adj: continue
    comp=[s];seen.add(s);st=[s]
    while st:
        u=st.pop()
        for v,_,_ in adj[u]:
            if v not in seen: seen.add(v);comp.append(v);st.append(v)
    if len(comp)>len(best): best=comp
keep=sorted(best); remap={o:n for n,o in enumerate(keep)}
P=[pts[o] for o in keep]; A=[[[remap[v],w,k] for v,w,k in adj[o]] for o in keep]
json.dump({'pts':P,'adj':A,'names':names,'src':'OpenStreetMap contributors (ODbL), extracted 2026-10-03'},open('graph.json','w'),separators=(',',':'))
print(ways,'ways',len(pts),'nodes ->',len(P),'in main component')
