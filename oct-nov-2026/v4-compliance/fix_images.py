"""Meta compliance fix (21-oct-2026): remove drug brand names from art (day07 headline, day21 vial label)."""
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
from lama_clean import clean
M='/opt/data/solace-skin-lab/oct-nov-2026-v3/media/'
F='/opt/data/cache/fonts/'
def mask_text(img,box,dil=11,thr=14):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);bg=cv2.GaussianBlur(g,(0,0),8).astype(int);m=np.zeros(g.shape,np.uint8)
    x1,y1,x2,y2=box;m[y1:y2,x1:x2]=((g[y1:y2,x1:x2]>170)&(g[y1:y2,x1:x2].astype(int)-bg[y1:y2,x1:x2]>thr)).astype(np.uint8)*255
    return cv2.dilate(m,np.ones((dil,dil),np.uint8))
# day07: remove "Why botox?" then write new headline
img=cv2.imread(M+'day07.jpg'); m=mask_text(img,(290,225,800,385))
cv2.imwrite('work/d07_mask.png',m); c=clean(img,m); cv2.imwrite('work/d07_clean.png',c)
# sample text color from original
g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); sel=(m>0)&(g>200); col=tuple(int(v) for v in img[sel].mean(0)[::-1])
pil=Image.fromarray(cv2.cvtColor(c,cv2.COLOR_BGR2RGB)); d=ImageDraw.Draw(pil)
up=ImageFont.truetype(F+'CormorantGaramond[wght].ttf',96); up.set_variation_by_axes([500])
it=ImageFont.truetype(F+'CormorantGaramond-Italic[wght].ttf',96); it.set_variation_by_axes([500])
a,b='Why ','wrinkle relaxers?'
wa=d.textlength(a,font=up); wb=d.textlength(b,font=it); x=540-(wa+wb)/2; y=245
d.text((x,y),a,font=up,fill=col); d.text((x+wa,y),b,font=it,fill=col)
pil.save('out/day07.jpg',quality=94); print('d07 color',col,'width',wa+wb)
# day21: blank vial label print
img=cv2.imread(M+'day21.jpg'); g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(int); hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
bg=cv2.GaussianBlur(g.astype(np.uint8),(0,0),10).astype(int); m=np.zeros(g.shape,np.uint8)
x1,y1,x2,y2=300,395,475,540
sub=((bg[y1:y2,x1:x2]-g[y1:y2,x1:x2]>12)|(hsv[y1:y2,x1:x2,1]>70)).astype(np.uint8)*255
m[y1:y2,x1:x2]=sub; m=cv2.dilate(m,np.ones((7,7),np.uint8))
cv2.imwrite('work/d21_mask.png',m); cv2.imwrite('out/day21.jpg',clean(img,m),[cv2.IMWRITE_JPEG_QUALITY,94]); print('d21 ok')
