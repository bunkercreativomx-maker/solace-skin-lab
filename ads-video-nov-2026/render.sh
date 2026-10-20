#!/bin/bash
# usage: render.sh "1 2 3" "9x16 4x5"
export PATH=/opt/data/.local/bin:$PATH
cd /opt/data/hyperframes/solace-ads; mkdir -p out qa
for a in $1; do for f in $2; do
  n=$(printf "ad%02d_%s" $a $f)
  python3 gen.py $a $f > /dev/null || { echo "GEN FAIL $n"; continue; }
  (cd $n && timeout 300 npx hyperframes check < /dev/null > ../qa/${n}_check.log 2>&1; grep -E "Check (passed|failed)" ../qa/${n}_check.log | sed "s/^/$n /")
  (cd $n && timeout 1200 npx hyperframes render -o ../out/${n}_raw.mp4 < /dev/null > ../qa/${n}_render.log 2>&1) || echo "RENDER FAIL $n"
  ffmpeg -nostdin -loglevel error -y -i out/${n}_raw.mp4 -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out/${n}.mp4 && rm out/${n}_raw.mp4
  echo "$n done $(ffprobe -v error -show_entries format=duration -of csv=p=0 out/${n}.mp4)"
done; done
echo ALLDONE
