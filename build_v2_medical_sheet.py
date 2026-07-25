from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path('/opt/data/solace-skin-lab')
days=[6,8,11,13,14,18,20,21,27,28]
thumb=500; label=42; cols=2; rows=5
sheet=Image.new('RGB',(cols*thumb,rows*(thumb+label)),'white')
d=ImageDraw.Draw(sheet); f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
for i,day in enumerate(days):
    im=Image.open(ROOT/f'images/august-2026-v2/day{day:02d}.png').convert('RGB').resize((thumb,thumb),Image.Resampling.LANCZOS)
    x=(i%cols)*thumb; y=(i//cols)*(thumb+label); sheet.paste(im,(x,y)); d.rectangle((x,y+thumb,x+thumb,y+thumb+label),fill='#332c28'); d.text((x+10,y+thumb+7),f'DAY {day:02d}',fill='white',font=f)
out=ROOT/'v2-medical-contact-sheet.jpg'; sheet.save(out,quality=95); print(out)
