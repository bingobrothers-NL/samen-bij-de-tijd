#!/usr/bin/env python3
"""Twice-daily source-linked RSS digest, no AI or fabricated explanations."""
import datetime as dt, email.utils, html, json, os, re, urllib.request, xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
from zoneinfo import ZoneInfo
from pathlib import Path
ROOT=Path(__file__).parent
FEEDS=[('Nederland','https://feeds.nos.nl/nosnieuwsbinnenland'),('Wereld','https://feeds.nos.nl/nosnieuwsbuitenland'),('Politiek','https://feeds.nos.nl/nosnieuwspolitiek'),('Economie','https://feeds.nos.nl/nosnieuwseconomie'),('Technologie','https://feeds.nos.nl/nosnieuwstech')]
now=dt.datetime.now(ZoneInfo('Europe/Amsterdam'))
edition=os.environ.get('EDITION') or ('ochtend' if now.hour<18 else 'avond')
def clean(value):
    return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>',' ',value or ''))).strip()
def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'SamenBijDeTijd/1.0 (+RSS digest; personal project)'})
    with urllib.request.urlopen(req,timeout=15) as r: return r.read()
def article_photo(link):
    """Try the article's own Open Graph/Twitter photo when RSS has none."""
    try:
        host=urlparse(link).hostname or ''
        if host not in ('nos.nl','www.nos.nl'):
            return ''
        req=urllib.request.Request(link,headers={'User-Agent':'Mozilla/5.0 (compatible; SamenBijDeTijd/1.0)'})
        with urllib.request.urlopen(req,timeout=7) as response:
            if 'text/html' not in response.headers.get('Content-Type',''):return ''
            page=response.read(350000).decode('utf-8','ignore')
        for tag in re.findall(r'<meta\b[^>]*>',page,re.I):
            if re.search(r'(?:og:image|twitter:image)',tag,re.I):
                m=re.search(r'\bcontent\s*=\s*["\']([^"\']+)',tag,re.I)
                if m:
                    candidate=urljoin(link,html.unescape(m.group(1)))
                    if candidate.startswith('https://') and urlparse(candidate).hostname:return candidate
    except Exception as exc:
        print('Article photo unavailable:',str(exc)[:100])
    return ''

def entries(category,url):
    root=ET.fromstring(fetch(url)); out=[]
    for item in root.findall('.//item')[:18]:
        title=clean(item.findtext('title')); link=(item.findtext('link') or '').strip()
        summary=clean(item.findtext('description'))
        image=''
        # Prefer editorial photos supplied by the publisher's RSS feed.
        # Never guess an unrelated stock photo for an article.
        for child in item:
            tag=child.tag.rsplit('}',1)[-1]
            if tag in ('thumbnail','content','enclosure','image'):
                candidate=child.attrib.get('url','')
                typ=child.attrib.get('type','')
                if candidate.startswith('https://') and (tag!='enclosure' or typ.startswith('image/')):
                    image=candidate;break
        if not image:
            # Some feeds include the photo only inside the HTML description.
            description_html=item.findtext('description') or ''
            match=re.search(r'<img[^>]+src=[\"\'](https://[^\"\']+)[\"\']',description_html,re.I)
            if match:image=html.unescape(match.group(1))
        if not image:image=article_photo(link)
        if not image and re.search(r'\bmicrosoft\b',title,re.I):
            image='microsoft-logo.svg'
        if not image:
            topic=(title+' '+summary).lower()
            image=('onderwerp-oekraine.svg' if any(w in topic for w in ('oekra','zelensky','rusland')) else
                   'onderwerp-zorg.svg' if any(w in topic for w in ('zorgpremie','ziekenhuis','zorgverzeker')) else
                   'onderwerp-cyber.svg' if any(w in topic for w in ('hack','cyber','deepfake','noord-korea')) else
                   'onderwerp-politiek.svg' if category=='Politiek' else '')
        stamp=item.findtext('pubDate') or ''
        try: published=email.utils.parsedate_to_datetime(stamp).astimezone(ZoneInfo('Europe/Amsterdam'))
        except Exception: published=now-dt.timedelta(days=2)
        if not title or not link.startswith('https://') or published<now-dt.timedelta(hours=30):continue
        out.append({'category':category,'title':title,'summary':summary[:380] or 'Lees het artikel bij de bron voor meer informatie.', 'explanation':'Dit is een samenvatting uit de RSS-feed van de bron. Voor meer achtergrond en controle van de feiten: open het originele artikel.', 'details':[summary[:380]] if summary else [],'context':'De beschikbare nieuwsfeed bevat alleen een korte omschrijving. Zodra er meer betrouwbare broninformatie beschikbaar is, kan hier extra context worden toegevoegd.','source':'NOS','url':link,'image':image,'published':published.isoformat()})
    return out
# A separate sports edition, using the public NOS sport RSS feed.
SPORT_FEED='https://feeds.nos.nl/nossportalgemeen'
try:
    sport_items=entries('Sport',SPORT_FEED)
    if sport_items:
        for item in sport_items:
            title=item['title'].lower()
            item['category']=('Formule 1' if any(t in title for t in ('formule 1','verstappen','grand prix','f1 ')) else 'Wielrennen' if any(t in title for t in ('wielren','tour de','vuelta','giro d','koers')) else 'Tennis' if any(t in title for t in ('tennis','wimbledon','atp ','wta ','sinner','alcaraz')) else 'Voetbal' if any(t in title for t in ('voetbal','eredivisie','champions league','oranje','ajax','psv','feyenoord')) else 'Overig')
        sports={'updated':now.strftime('%d-%m-%Y %H:%M Europe/Amsterdam'),'items':sport_items[:15]}
        (ROOT/'sport.json').write_text(json.dumps(sports,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f'Updated sport: {len(sport_items[:15])} stories')
except Exception as exc:
    print('Sports feed unavailable; preserving previous sport edition:',exc)
all_items=[]
for cat,url in FEEDS:
    try: all_items+=entries(cat,url)
    except Exception as e: print('Feed unavailable:',cat,str(e))
if not all_items: raise SystemExit('No valid RSS news: retaining previous editions')
seen=set();unique=[]
for item in sorted(all_items,key=lambda x:x['published'],reverse=True):
    key=re.sub('[^a-z0-9]','',item['title'].lower())[:75]
    if key not in seen: seen.add(key);unique.append(item)
selected=[]
for cat,_ in FEEDS:
    match=next((i for i in unique if i['category']==cat),None)
    if match:selected.append(match)
for item in unique:
    if len(selected)>=7:break
    if item not in selected:selected.append(item)
if len(selected)<3:raise SystemExit('Too few stories: retaining previous editions')
for item in selected:item.pop('published',None)
selected[0]['question']='Welk onderwerp uit deze editie raakt jullie het meest, en waarom?'
payload={'updated':now.strftime('%d-%m-%Y %H:%M Europe/Amsterdam'),'edition':edition,'items':selected}
(ROOT/f'{edition}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'daily.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Updated {edition}: {len(selected)} articles')
