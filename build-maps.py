#!/usr/bin/env python3
"""Rebuild the two inline SVG maps from Natural Earth data and inject them into the pages.

  python3 build-maps.py /path/to/geodata

geodata needs ne_50m_land.geojson (trade map), ne_10m_land.geojson, ne_10m_lakes.geojson and
ne_10m_rivers_lake_centerlines.geojson (ARA port map), from
https://github.com/nvkelso/natural-earth-vector/tree/master/geojson (not kept in the repo).
Replaces the <div class="trademap"> block in chartering(.-nl).html and the
<div class="portmap"> block in agency(-nl).html. Styling lives in styles.css.
"""
import json, math, pathlib, re, sys
GEO = pathlib.Path(sys.argv[1]); ROOT = pathlib.Path(__file__).parent

def merc(lat): return math.log(math.tan(math.pi/4 + math.radians(max(-85.0, min(85.0, lat)))/2))

class Frame:
    def __init__(s, W, H, lon0, lon1, lat0, lat1, margin=40):
        s.W, s.H, s.lon0, s.lon1, s.lat0, s.lat1, s.M = W, H, lon0, lon1, lat0, lat1, margin
        s.kx = W/(lon1-lon0); s.ky = H/(merc(lat1)-merc(lat0))
    def px(s, lon, lat): return ((lon-s.lon0)*s.kx, (merc(s.lat1)-merc(lat))*s.ky)
    def clip(s, pts):
        W, H, M = s.W, s.H, s.M
        def edge(pts, inside, inter):
            out=[]
            for i,p in enumerate(pts):
                q=pts[i-1]
                if inside(p):
                    if not inside(q): out.append(inter(q,p))
                    out.append(p)
                elif inside(q): out.append(inter(q,p))
            return out
        def ix(a,b,x): t=(x-a[0])/(b[0]-a[0]); return (x, a[1]+t*(b[1]-a[1]))
        def iy(a,b,y): t=(y-a[1])/(b[1]-a[1]); return (a[0]+t*(b[0]-a[0]), y)
        for inside,inter in [(lambda p:p[0]>=-M, lambda a,b:ix(a,b,-M)),(lambda p:p[0]<=W+M, lambda a,b:ix(a,b,W+M)),
                             (lambda p:p[1]>=-M, lambda a,b:iy(a,b,-M)),(lambda p:p[1]<=H+M, lambda a,b:iy(a,b,H+M))]:
            if not pts: return []
            pts=edge(pts,inside,inter)
        return pts
    def d(s, pts, closed=True, tol=0.9, minsize=3):
        out=[]; last=None
        for x,y in pts:
            if last and abs(x-last[0])<tol and abs(y-last[1])<tol: continue
            out.append((x,y)); last=(x,y)
        if len(out)<(3 if closed else 2): return ""
        xs=[x for x,_ in out]; ys=[y for _,y in out]
        if closed and max(xs)-min(xs)<minsize and max(ys)-min(ys)<minsize: return ""
        return "M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in out)+("Z" if closed else "")
    def land(s, geojson, tol=0.9):
        paths=[]
        for f in json.load(open(GEO/geojson))["features"]:
            g=f["geometry"]; polys=[g["coordinates"]] if g["type"]=="Polygon" else g["coordinates"]
            for poly in polys:
                for ring in poly:
                    d=s.d(s.clip([s.px(lo,la) for lo,la in ring]), tol=tol)
                    if d: paths.append(d)
        return '<path class="land" fill-rule="evenodd" d="'+" ".join(paths)+'"/>'
    def poly(s, ll): return "M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in (s.px(lo,la) for lo,la in ll))+"Z"
    def grid(s, step, pid):
        # dotted graticule, one line per `step` degrees
        d=[]
        lo=math.ceil(s.lon0/step)*step
        while lo<=s.lon1:
            x,_=s.px(lo,s.lat0); d.append(f"M{x:.1f},0V{s.H}"); lo+=step
        la=math.ceil(s.lat0/step)*step
        while la<=s.lat1:
            _,y=s.px(s.lon0,la); d.append(f"M0,{y:.1f}H{s.W}"); la+=step
        return f'<path class="grat" d="{" ".join(d)}"/>'

HATCH='<pattern id="{id}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line class="hl" x1="0" y1="0" x2="0" y2="7"/></pattern>'
def fades(F, prefix, r=140, l=120, t=70, b=90):
    g=lambda id,x1,y1,x2,y2: f'<linearGradient id="{prefix}{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="#EDF2EF" stop-opacity="0"/><stop offset="1" stop-color="#EDF2EF"/></linearGradient>'
    defs=g("R",0,0,1,0)+g("L",1,0,0,0)+g("T",0,1,0,0)+g("B",0,0,0,1)
    rects=(f'<rect x="{F.W-r}" y="0" width="{r}" height="{F.H}" fill="url(#{prefix}R)"/><rect x="0" y="0" width="{l}" height="{F.H}" fill="url(#{prefix}L)"/>'
           f'<rect x="0" y="0" width="{F.W}" height="{t}" fill="url(#{prefix}T)"/><rect x="0" y="{F.H-b}" width="{F.W}" height="{b}" fill="url(#{prefix}B)"/>')
    return defs, rects

# ---------------- trade map (chartering) ----------------
T = Frame(1080, 680, -38.0, 44.0, 29.0, 63.0)
AREAS = {  # lon/lat polygons that abut; land drawn on top clips them to water
 "north": ([(1.4,50.9),(-2.2,56),(-2.5,59),(-1.8,61.6),(5.6,62.6),(7.6,58.2),(8.5,59.3),(10.8,59.9),(11.8,58.8),(11.8,57.6),(10.6,57.7),(9.4,55.2),(8.6,53.6),(5.2,53.1),(4.2,51.9),(1.9,50.9)], (3.3,56.6)),
 "baltic": ([(10.6,57.7),(11.8,57.6),(12.5,58.4),(13.5,60.4),(17,63.5),(24,66.5),(31.5,62),(30.5,59.2),(25,57.2),(21.5,54.3),(14,53.6),(10.4,54.1),(9.8,55.5)], (19.5,58.4)),
 "atlantic": ([(-45,66),(-1.8,66),(-1.8,61.6),(-2.5,59),(-2.2,56),(1.4,50.9),(1.9,50.9),(0,49.3),(-2,49),(-4.8,48.3),(-1.2,46.5),(-1.5,43.4),(-8.2,43.6),(-8.2,37.0),(-6.3,36.0),(-5.6,35.95),(-5.4,35.2),(-6.3,34.0),(-7.4,33.2),(-10.0,32.2),(-45,32.2)], (-21,48.5)),
 "westafrica": ([(-45,32.2),(-10.0,32.2),(-9.6,30.2),(-13.2,27.2),(-17.2,21),(-45,21)], (-23,30.6)),
 "med": ([(-5.6,35.95),(-6.3,36.0),(-5.8,36.6),(-1.5,38.2),(0.6,41.2),(2.6,43.6),(9,44.8),(13,46.2),(19.5,41.5),(23.5,40.2),(26.6,41.2),(26.2,40.1),(29.0,41.0),(29.4,40.6),(36.5,37.2),(36.5,31),(30,30.4),(10,33.2),(-2,34.8),(-5.2,35.3)], (17.5,35.6)),
 "black": ([(29.0,41.0),(26.2,40.1),(27.5,41.6),(28.2,42.6),(27.6,43.6),(30.2,47.2),(35.5,46.4),(39.5,47.8),(42.5,43.5),(42.5,40.9),(36,41),(29.4,40.6)], (34.5,43.6)),
}
NAMES = {"en": {"north":"North Sea","baltic":"Baltic","atlantic":"Atlantic","westafrica":"West Africa","med":"Mediterranean","black":"Black Sea","rtm":"Rotterdam","ant":"Antwerp"},
         "nl": {"north":"Noordzee","baltic":"Oostzee","atlantic":"Atlantische Oceaan","westafrica":"West-Afrika","med":"Middellandse Zee","black":"Zwarte Zee","rtm":"Rotterdam","ant":"Antwerpen"}}
RTM=(4.48,51.92); ANT=(4.40,51.22)

def trade_svg(lang):
    n=NAMES[lang]; defs,rects=fades(T,"tf")
    out=[f'<svg viewBox="0 0 {T.W} {T.H}" xmlns="http://www.w3.org/2000/svg">',
         '<defs>'+defs+HATCH.format(id="thatch")+'</defs>',
         f'<rect width="{T.W}" height="{T.H}" fill="#EDF2EF"/>', T.grid(10,"tg"),
         '<g class="seas">'+"".join(f'<path class="ta" d="{T.poly(ll)}"/>' for k,(ll,lp) in AREAS.items())+'</g>',
         T.land("ne_50m_land.geojson"), rects]
    for k,(ll,lp) in AREAS.items():
        x,y=T.px(*lp); out.append(f'<text class="lab" x="{x:.0f}" y="{y:.0f}" text-anchor="middle">{n[k]}</text>')
    xr,yr=T.px(*RTM); xa,ya=T.px(*ANT)
    out.append(f'<g class="home"><circle cx="{xr:.1f}" cy="{yr:.1f}" r="5.5"/><text x="{xr+12:.0f}" y="{yr-4:.0f}">{n["rtm"]}</text>'
               f'<circle cx="{xa:.1f}" cy="{ya:.1f}" r="5.5"/><text x="{xa+12:.0f}" y="{ya+15:.0f}">{n["ant"]}</text></g>')
    out.append('</svg>'); return "\n".join(out)

# ---------------- ARA port map (agency) ----------------
P = Frame(1080, 460, 1.2, 7.8, 50.85, 52.6, margin=30)
ARA = [(0,50),(0,54),(9,54),(9,50)]  # all water in the frame, clipped by land
PORTS = [  # key, office, lon, lat, label anchor, dx, dy
 ("rtm","Amsterdam",4.90,52.375,"start",12,5),
 ("rtm","Rotterdam",4.48,51.92,"start",12,-6),
 ("rtm","Moerdijk",4.60,51.69,"start",12,14),
 ("rtm","Flushing",3.57,51.45,"end",-12,-6),
 ("rtm","Terneuzen",3.83,51.335,"middle",0,23),
 ("ant","Zeebrugge",3.20,51.33,"end",-12,4),
 ("ant","Ghent",3.72,51.05,"end",-12,12),
 ("ant","Antwerp",4.40,51.23,"start",12,-6),
 ("ant","Hemiksem &amp; upper Scheldt",4.34,51.14,"start",12,15),
]
PORT_NL={"Flushing":"Vlissingen","Ghent":"Gent","Antwerp":"Antwerpen","Hemiksem &amp; upper Scheldt":"Hemiksem &amp; Boven-Schelde"}
LEG={"en":("Agency, all ARA ports","Rotterdam office &middot; NL","Antwerp office &middot; BE","North Sea"),
     "nl":("Agentuur, alle ARA-havens","Kantoor Rotterdam &middot; NL","Kantoor Antwerpen &middot; BE","Noordzee")}
RIVERS={"Schelde","Waal","Lek"}
RIVER_LON_MAX=5.1

def rivers():
    d=[]
    for f in json.load(open(GEO/"ne_10m_rivers_lake_centerlines.geojson"))["features"]:
        if f["properties"].get("name") not in RIVERS: continue
        g=f["geometry"]; lines=[g["coordinates"]] if g["type"]=="LineString" else g["coordinates"]
        for l in lines:
            pts=[P.px(lo,la) for lo,la in l if lo<=RIVER_LON_MAX]
            # keep only the stretch inside the frame (+margin)
            seg=[]
            for p in pts:
                if -P.M<=p[0]<=P.W+P.M and -P.M<=p[1]<=P.H+P.M: seg.append(p)
                else:
                    s=P.d(seg,closed=False,tol=0.5); d.append(s) if s else None; seg=[]
            s=P.d(seg,closed=False,tol=0.5); d.append(s) if s else None
    return '<path class="river" d="'+" ".join(x for x in d if x)+'"/>'

def lakes():
    # inland water drawn as plain mist on top of the land (IJsselmeer/Markermeer): shape only, not a working area
    paths=[]
    for f in json.load(open(GEO/"ne_10m_lakes.geojson"))["features"]:
        g=f["geometry"]; polys=[g["coordinates"]] if g["type"]=="Polygon" else g["coordinates"]
        for poly in polys:
            pts=[P.px(lo,la) for lo,la in poly[0]]
            if not any(0<=x<=P.W and 0<=y<=P.H for x,y in pts): continue
            d=P.d(P.clip(pts), tol=0.6)
            if d: paths.append(d)
    return '<path class="lake" d="'+" ".join(paths)+'"/>' if paths else ""

def port_svg(lang):
    head,l1,l2,sea=LEG[lang]; defs,rects=fades(P,"pf",r=200,l=110,t=50,b=60)
    out=[f'<svg viewBox="0 0 {P.W} {P.H}" xmlns="http://www.w3.org/2000/svg">',
         '<defs>'+defs+HATCH.format(id="phatch")+'</defs>',
         f'<rect width="{P.W}" height="{P.H}" fill="#EDF2EF"/>', P.grid(1,"pg"),
         f'<path class="ta" d="{P.poly(ARA)}"/>', P.land("ne_10m_land.geojson", tol=0.6), lakes(), rivers(), rects]
    x,y=P.px(2.4,52.05); out.append(f'<text class="sealab" x="{x:.0f}" y="{y:.0f}">{sea}</text>')
    for off,name,lo,la,anc,dx,dy in PORTS:
        x,y=P.px(lo,la); lab=PORT_NL.get(name,name) if lang=="nl" else name
        out.append(f'<g class="port {off}"><circle cx="{x:.1f}" cy="{y:.1f}" r="6"/><circle class="ring" cx="{x:.1f}" cy="{y:.1f}" r="11"/><text x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{anc}">{lab}</text></g>')
    out.append(f'<g class="legend" transform="translate(790 60)"><text class="leghead" x="0" y="0">{head}</text>'
               f'<g class="port rtm" transform="translate(0 28)"><circle cx="6" cy="-4" r="6"/><text x="20" y="0">{l1}</text></g>'
               f'<g class="port ant" transform="translate(0 56)"><circle cx="6" cy="-4" r="6"/><text x="20" y="0">{l2}</text></g></g>')
    out.append('</svg>'); return "\n".join(out)

def inject(fname, cls, svg):
    p=ROOT/fname; s=p.read_text()
    s2,n=re.subn(r'(<div class="'+cls+r'"[^>]*>)\n.*?</svg>\n(\s*</div>)', lambda m: m.group(1)+"\n"+svg+"\n"+m.group(2), s, count=1, flags=re.S)
    assert n==1, fname
    p.write_text(s2); print(f"{fname}: {cls} = {len(svg)//1024} KB")

inject("chartering.html","trademap",trade_svg("en")); inject("chartering-nl.html","trademap",trade_svg("nl"))
inject("agency.html","portmap",port_svg("en")); inject("agency-nl.html","portmap",port_svg("nl"))
