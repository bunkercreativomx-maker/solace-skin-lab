import json,os,urllib.request,time,concurrent.futures as cf
K=[l.split('=',1)[1].strip().strip('"\'') for l in open('/opt/data/.env') if l.startswith('FAL_KEY=')][0]
H={'Authorization':'Key '+K,'Content-Type':'application/json'}
P={'A_chill_rnb':"Warm, inviting chill R&B lounge groove, smooth Rhodes electric piano, soft round bassline, light finger snaps and brushed drums, 92 BPM, feel-good, sensual and classy, luxury spa boutique commercial, positive and welcoming",
   'B_deep_house':"Upbeat elegant deep house, warm plucked synth chords, airy pads, soft four-on-the-floor kick, shimmering hi-hats, 118 BPM, sunny, glamorous and inviting, luxury beauty commercial, makes you want to go",
   'C_acoustic_pop':"Feel-good acoustic pop, bright acoustic guitar strums, soft hand claps, light piano melody, warm bass, 104 BPM, happy, warm and inviting, lifestyle commercial, smile-inducing"}
def run(name,prompt):
    body=json.dumps({'prompt':prompt,'music_length_ms':32000,'force_instrumental':True,'output_format':'mp3_44100_128'}).encode()
    j=json.load(urllib.request.urlopen(urllib.request.Request('https://queue.fal.run/fal-ai/elevenlabs/music',body,H),timeout=60))
    for _ in range(80):
        s=json.load(urllib.request.urlopen(urllib.request.Request(j['status_url'],headers=H),timeout=60))
        if s['status']=='COMPLETED': break
        time.sleep(5)
    r=json.load(urllib.request.urlopen(urllib.request.Request(j['response_url'],headers=H),timeout=60))
    url=r['audio']['url']; urllib.request.urlretrieve(url,f'{name}.mp3'); return name,url
with cf.ThreadPoolExecutor(3) as ex:
    for f in cf.as_completed([ex.submit(run,k,v) for k,v in P.items()]):
        try: print(f.result())
        except Exception as e: print('ERR',e,getattr(e,'read',lambda:b'')()[:300])
