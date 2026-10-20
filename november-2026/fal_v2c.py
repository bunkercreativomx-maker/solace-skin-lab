import os,json,urllib.request,concurrent.futures as cf
K=[l.split('=',1)[1].strip().strip('"\'') for l in open('/opt/data/.env') if l.startswith('FAL_KEY=')][0]
P=json.load(open('artistly_prompts_v2c.json'))
def gen(d,v):
    os.makedirs(f'photos/d{int(d):02d}/fal',exist_ok=True)
    body=json.dumps({"prompt":v['prompt'],"image_size":"portrait_4_3" if v['ar']=='4:5' else "square_hd","quality":"medium","num_images":2,"output_format":"png"}).encode()
    j=json.load(urllib.request.urlopen(urllib.request.Request('https://fal.run/openai/gpt-image-2',body,{'Authorization':'Key '+K,'Content-Type':'application/json'}),timeout=400))
    out=[]
    for i,im in enumerate(j['images'],1):
        f=f'photos/d{int(d):02d}/fal/f{i}.png'; urllib.request.urlretrieve(im['url'],f); out.append(f)
    return d,out
with cf.ThreadPoolExecutor(6) as ex:
    for f in cf.as_completed([ex.submit(gen,d,v) for d,v in P.items()]):
        try: print(f.result())
        except Exception as e: print('ERR',e,getattr(e,'read',lambda:b'')()[:300])
