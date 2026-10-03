import numpy as np, json, math
cp=[((75,227),(-31.971915,115.786689),'Sheep Shed'),((253,297),(-31.973565,115.786213),'Global Stage'),((495,360),(-31.975567,115.785514),'Main Arena'),
((263,436),(-31.973555,115.78477),'Cattle Lane'),((382,528),(-31.974444,115.783554),'Farmyard Nursery'),((480,547),(-31.975275,115.783618),'Emporium'),
((360,500),(-31.974408,115.784188),'Royal Bazaar'),((267,165),(-31.973483,115.787558),'Dairy Land'),((605,512),(-31.97648,115.784054),'Long Paddock Stage'),
((266,260),(-31.973498,115.78656),'Cat Pavilion'),((662,240),(-31.976863,115.786405),'Station Gate (OSM)'),((274,88),(-31.973683,115.788015),'Gate 10 (OSM)')]
A=np.array([[x,y,1] for (x,y),_,_ in cp]); la=np.array([c[1][0] for c in cp]); lo=np.array([c[1][1] for c in cp])
pa=np.linalg.lstsq(A,la,rcond=None)[0]; po=np.linalg.lstsq(A,lo,rcond=None)[0]
def f(x,y): return float(pa@[x,y,1]), float(po@[x,y,1])
def m(a,b): return math.hypot((a[0]-b[0])*111320,(a[1]-b[1])*111320*math.cos(math.radians(32)))
res=[(n,round(m(f(*p),c))) for p,c,n in cp]; print(res, 'rms',round(math.sqrt(sum(r*r for _,r in res)/len(res))))
est={'Sideshow Alley':(143,452),'AgVenture Hill':(302,215),"Woody's Bar":(230,335),'Cattle Lane Bar':(230,518),'Good Fields':(635,349),
'Long Paddock (food, north)':(642,467),'Long Paddock (food, south)':(629,543),'Sweetie Lane':(351,472),'Bush BBQ':(396,178),'Taste Street (Emporium)':(454,533),
'Kids Luna Park':(378,271),'Arena Surrounds rides':(590,260),'Global Stage Precinct rides':(202,277),'Gate 10 Lawn rides':(314,121),'Smoking area':(439,125)}
out={k:[round(v,6) for v in f(*p)] for k,p in est.items()}
for k,v in out.items(): print(k,v)
json.dump(out,open('raw/georef_est.json','w'),indent=1)
