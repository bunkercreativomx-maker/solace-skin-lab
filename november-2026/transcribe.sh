export PATH=/opt/data/.local/bin:$PATH
cd /opt/data/hyperframes
for d in $(seq -w 3 30); do
  A=/opt/data/solace-skin-lab/november-2026/audio
  while [ ! -f $A/d$d.wav ]; do sleep 10; done
  [ -f $A/tr_d$d/transcript.json ] || timeout 300 npx hyperframes transcribe $A/d$d.wav -d $A/tr_d$d --language en < /dev/null > /dev/null 2>&1
  echo "tr d$d $(ls $A/tr_d$d 2>/dev/null)"
done
echo TRDONE
