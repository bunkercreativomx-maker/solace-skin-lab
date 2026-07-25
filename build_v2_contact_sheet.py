from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/opt/data/solace-skin-lab')
SRC = ROOT / 'images' / 'august-2026-v2'
OUT = ROOT / 'v2-contact-sheet.jpg'
files = [SRC / f'day{day:02d}.png' for day in range(1,31)]
missing = [str(p) for p in files if not p.exists()]
if missing:
    raise SystemExit(f'Missing {len(missing)} files')
cols = 5
thumb = 300
label = 34
rows = 6
sheet = Image.new('RGB', (cols*thumb, rows*(thumb+label)), '#f7f1e8')
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
for i,p in enumerate(files):
    im = Image.open(p).convert('RGB').resize((thumb,thumb), Image.Resampling.LANCZOS)
    x=(i%cols)*thumb; y=(i//cols)*(thumb+label)
    sheet.paste(im,(x,y))
    draw.rectangle((x,y+thumb,x+thumb,y+thumb+label), fill='#332c28')
    draw.text((x+10,y+thumb+6),f'DAY {i+1:02d}',fill='white',font=font)
sheet.save(OUT,quality=92)
print(OUT)
