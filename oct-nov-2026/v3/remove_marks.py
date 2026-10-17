"""Remove ONLY the logos/watermarks the client asked to remove. Mask-based inpaint (FAL flux-pro fill);
result is composited back ONLY inside the mask, every other pixel = client's original."""
import os,sys,json,base64,urllib.request,cv2,numpy as np
ROOT=os.path.dirname(os.path.abspath(__file__))
KEY=[l.split('=',1)[1].strip().strip('"') for l in open('/opt/data/.env') if l.startswith('FAL_KEY=')][0]
# boxes measured with connected components of white overlay text (x1,y1,x2,y2); 'solid' = mask whole box
JOBS={
 6:dict(src='src/day06.jpg',text=[(720,1125,965,1272)],solid=[(124,1198,357,1240)],prompt="smooth grayscale studio photo of skin and plain light gray background, no text"),
 18:dict(src='src/day18.jpg',text=[],solid=[(445,1095,612,1290)],prompt="empty plain surface: matte black vinyl on the left half, wrinkled plain white paper sheet on the right half, nothing else, empty"),
 20:dict(src='src/day20.jpg',text=[(528,182,826,362),(532,1108,820,1162)],solid=[(1140,1436,1218,1514),(114,1459,209,1494)],prompt="warm natural photo of skin and white bodysuit fabric, soft sunlight, no text, no logo"),
 7:dict(src='src/day07.jpg',text=[],solid=[(388,1298,692,1366)],prompt="continuation of the same photo, plain skin and background, no text, no logo"),
 30:dict(src='src/day30.jpg',text=[],solid=[(62,740,228,846)],prompt="continuation of the same photo, plain skin, no text, no logo, no frame"),
}
def mask_for(img,cfg):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); bg=cv2.GaussianBlur(g,(0,0),10).astype(int)
    m=np.zeros(g.shape,np.uint8)
    for x1,y1,x2,y2 in cfg['text']:
        sub=((g[y1:y2,x1:x2]>185)&(g[y1:y2,x1:x2].astype(int)-bg[y1:y2,x1:x2]>10)).astype(np.uint8)*255
        m[y1:y2,x1:x2]=sub
    m=cv2.dilate(m,np.ones((11,11),np.uint8))
    for x1,y1,x2,y2 in cfg['solid']: m[y1:y2,x1:x2]=255
    return m
def b64(arr,ext):
    mime='jpeg' if ext=='jpg' else ext
    return f"data:image/{mime};base64,"+base64.b64encode(cv2.imencode('.'+ext,arr,[cv2.IMWRITE_JPEG_QUALITY,95] if ext=='jpg' else [])[1]).decode()
def run(day):
    cfg=JOBS[day]; img=cv2.imread(os.path.join(ROOT,cfg['src'])); m=mask_for(img,cfg)
    cv2.imwrite(f"{ROOT}/work/day{day:02d}_mask.png",m)
    body=json.dumps({"image_url":b64(img,"jpg"),"mask_url":b64(m,'png'),"prompt":cfg['prompt'],"output_format":"png","safety_tolerance":"5"}).encode()
    r=urllib.request.Request("https://fal.run/fal-ai/flux-pro/v1/fill",data=body,method="POST",headers={"Authorization":"Key "+KEY,"Content-Type":"application/json"})
    res=json.load(urllib.request.urlopen(r,timeout=300))
    raw=f"{ROOT}/work/day{day:02d}_fill.png"; urllib.request.urlretrieve(res['images'][0]['url'],raw)
    a=cv2.resize(cv2.imread(raw),(img.shape[1],img.shape[0]),interpolation=cv2.INTER_LANCZOS4)
    soft=cv2.GaussianBlur(cv2.dilate(m,np.ones((7,7),np.uint8)),(0,0),3).astype(float)[...,None]/255
    out=(a*soft+img*(1-soft)).astype(np.uint8)
    cv2.imwrite(f"{ROOT}/work/day{day:02d}_clean.png",out)
    print(day,'changed px outside mask region:',int(((np.abs(out.astype(int)-img).sum(2)>0)&(soft[...,0]==0)).sum()))
if __name__=='__main__':
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(3) as ex: list(ex.map(run,[int(x) for x in sys.argv[1:]] or list(JOBS)))
