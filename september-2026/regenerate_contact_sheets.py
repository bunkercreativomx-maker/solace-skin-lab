#!/usr/bin/env python3
# Regenera los 3 contact sheets de septiembre-2026 (days01-10, 11-20, 21-30)
# usando las imagenes images/dayNN.png actuales.
import os
from PIL import Image

BASE='/opt/data/solace-skin-lab/september-2026'
IMG=os.path.join(BASE,'images')
OUT=os.path.join(BASE,'contact-sheets')
os.makedirs(OUT, exist_ok=True)

def contact_sheet(start, end, outfile):
    cols=5
    cell=340
    pad=12
    rows=( (end-start+1) + cols -1 )//cols
    W=cols*cell+(cols+1)*pad
    H=rows*cell+(rows+1)*pad
    sheet=Image.new('RGB',(W,H),(18,18,20))
    for i,day in enumerate(range(start,end+1)):
        p=os.path.join(IMG,f'day{day:02d}.png')
        if not os.path.exists(p):
            print('  missing', p); continue
        im=Image.open(p).convert('RGB')
        im=im.resize((cell,cell), Image.LANCZOS)
        r,c=divmod(i,cols)
        x=pad+c*(cell+pad); y=pad+r*(cell+pad)
        sheet.paste(im,(x,y))
    sheet.save(outfile)
    print(f'{outfile}: {os.path.getsize(outfile)} bytes')

contact_sheet(1,10, os.path.join(OUT,'days01-10.png'))
contact_sheet(11,20, os.path.join(OUT,'days11-20.png'))
contact_sheet(21,30, os.path.join(OUT,'days21-30.png'))
print('DONE')
