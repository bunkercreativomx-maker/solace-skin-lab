from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

srcs = sorted(Path('/opt/data/images').glob('upload_20260723_16282*'))
thumb_w, thumb_h = 420, 420
label_h = 46
cols = 2
rows = (len(srcs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * thumb_w, rows * (thumb_h + label_h)), 'white')
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
for i, p in enumerate(srcs):
    im = Image.open(p).convert('RGB')
    im.thumbnail((thumb_w - 20, thumb_h - 20), Image.Resampling.LANCZOS)
    x = (i % cols) * thumb_w + (thumb_w - im.width) // 2
    y0 = (i // cols) * (thumb_h + label_h)
    y = y0 + (thumb_h - im.height) // 2
    sheet.paste(im, (x, y))
    draw.text(((i % cols) * thumb_w + 10, y0 + thumb_h + 8), p.name, fill='black', font=font)
out = Path('/opt/data/solace-skin-lab/real-assets-contact-sheet.jpg')
sheet.save(out, quality=90)
print(out)
