import os
import glob
from PIL import Image

dst_dir = './static/images_after'
os.makedirs(dst_dir, exist_ok=True)

files = glob.glob('./static/images/*')

for f in files:
    root, ext = os.path.splitext(f)
    if ext in ['.jpg', '.png']:
        img = Image.open(f)
        img_resize = img.resize((img.width // 4*3, img.height // 4*3))
        basename = os.path.basename(root)
        img_resize.save(os.path.join(dst_dir, basename + ext))