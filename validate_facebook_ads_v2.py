import json
import re
from pathlib import Path

ROOT=Path('/opt/data/solace-skin-lab')
p=ROOT/'facebook_ads_v2_2026-07-24_to_2026-08-22.json'
data=json.loads(p.read_text())
errors=[]
ads=data.get('ads',[])
if len(ads)!=8: errors.append(f'Expected 8 ads, got {len(ads)}')
if sum(x['percent'] for x in data['monthlyStrategy']['budgetAllocation'])!=100: errors.append('Budget allocation does not total 100%')
blob=json.dumps(data,ensure_ascii=False)
if '(915) 995-9524' not in blob: errors.append('Official phone missing')
for retired in ('2060','(915) 995-2060','149.99'):
    if retired in blob: errors.append(f'Retired/conflicting value found: {retired}')
ids=[a['id'] for a in ads]
if len(set(ids))!=len(ids): errors.append('Duplicate ad IDs')
for a in ads:
    for k in ('primaryTextA','primaryTextB','headlineA','headlineB','description','cta','audience','optimization','compliance'):
        if not a.get(k): errors.append(f"{a.get('id')}: missing {k}")
    days=[a.get('creativeDay'),a.get('alternateCreativeDay'),*(a.get('creativeDays') or []),*(a.get('alternateCreativeDays') or [])]
    for d in filter(None,days):
        if not (ROOT/f'images/august-2026-v2/day{d:02d}.png').is_file(): errors.append(f"{a['id']}: missing creative day {d}")
for variant in ('primaryTextA','primaryTextB'):
    offer=next(a for a in ads if a['id']=='META-03')[variant]
    if 'GET A FREE FACIAL' not in offer or 'WITH THE PURCHASE OF ANY LUXURY SKINCARE PRODUCT • ONLY $64.99' not in offer: errors.append(f'META-03 {variant}: offer changed')
    tue=next(a for a in ads if a['id']=='META-04')[variant]
    for phrase in ('TUESDAY 2×1 + WINE + 2 FREE FACIALS','age 21+'):
        if phrase not in tue: errors.append(f'META-04 {variant}: missing {phrase}')
    for ad_id in ('META-05','META-07'):
        text=next(a for a in ads if a['id']==ad_id)[variant].lower()
        for phrase in ('suitability','potential risks','individual results vary'):
            if phrase not in text: errors.append(f'{ad_id} {variant}: missing {phrase}')
texts=[re.sub(r'\W+',' ',a[k].lower()).strip() for a in ads for k in ('primaryTextA','primaryTextB')]
if len(texts)!=len(set(texts)): errors.append('Duplicate primary copy variants')
print(json.dumps({'ok':not errors,'ads':len(ads),'copyVariants':len(texts),'budgetPercent':sum(x['percent'] for x in data['monthlyStrategy']['budgetAllocation']),'errors':errors},indent=2))
raise SystemExit(bool(errors))
