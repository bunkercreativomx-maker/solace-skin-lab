"""Non-generative cleanup with LaMa (local, big-lama). Only masked pixels change."""
import sys,cv2,numpy as np,torch
from simple_lama_inpainting import SimpleLama
from PIL import Image
lama=SimpleLama()
def text_mask(img,box,thr=12,dil=9):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); bg=cv2.GaussianBlur(g,(0,0),8).astype(int); m=np.zeros(g.shape,np.uint8)
    x1,y1,x2,y2=box; m[y1:y2,x1:x2]=(np.abs(g[y1:y2,x1:x2].astype(int)-bg[y1:y2,x1:x2])>thr).astype(np.uint8)*255
    return cv2.dilate(m,np.ones((dil,dil),np.uint8))
def clean(img,m):
    out=np.array(lama(Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB)),Image.fromarray(m)))
    out=cv2.cvtColor(out,cv2.COLOR_RGB2BGR)[:img.shape[0],:img.shape[1]]
    soft=cv2.GaussianBlur(m,(0,0),2).astype(float)[...,None]/255
    return (out*soft+img*(1-soft)).astype(np.uint8)
if __name__=='__main__':
    for d,box,solid in [(7,(388,1298,692,1366),False),(30,(62,740,228,846),True)]:
        img=cv2.imread(f'src/day{d:02d}.jpg')
        if solid:
            m=np.zeros(img.shape[:2],np.uint8); x1,y1,x2,y2=box; m[y1:y2,x1:x2]=255
        else: m=text_mask(img,box)
        cv2.imwrite(f'work/day{d:02d}_clean.png',clean(img,m)); print('ok',d)
