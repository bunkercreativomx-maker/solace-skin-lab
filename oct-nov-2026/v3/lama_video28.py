"""Day 28: remove only the 'DUNEDINMEDICAL.CO.NZ' line, frame by frame with LaMa (non-generative)."""
import cv2, numpy as np, subprocess, os
from lama_clean import clean
cap = cv2.VideoCapture('src/day28.mp4'); fps = cap.get(5); W = int(cap.get(3))
os.makedirs('work/f28', exist_ok=True)
y0, y1 = 1072, 1192  # crop band for speed
m = np.zeros((y1 - y0, W), np.uint8); m[1112 - y0:1150 - y0, 186:552] = 255
i = 0
while True:
    ok, fr = cap.read()
    if not ok:
        break
    band = fr[y0:y1].copy(); fr[y0:y1] = clean(band, m)
    cv2.imwrite(f'work/f28/{i:05d}.png', fr); i += 1
print('frames', i, fps, flush=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(fps), '-i', 'work/f28/%05d.png', '-i', 'src/day28.mp4',
                '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', 'out/day28.mp4'], check=True)
print('done', flush=True)
