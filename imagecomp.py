from PIL import Image
import os
from pathlib import Path

prop = 2.5

def comp(path):
    typ = getfiletype(path)
    if typ == None: return path
    img = Image.open(path)
    if img.height <= img.width / prop: return path
    if typ == 'img': return imgcomp(path)
    return gifcomp(path)

def getfiletype(path):
    try: cimg = Image.open(path)
    except: return
    return 'gif' if 'loop' in cimg.info else 'img'

def imgcomp(path):
    cimg = Image.open(path)
    nimg = Image.new('RGBA', (int(cimg.height * prop), cimg.height), (0, 0, 0, 0))
    nimg.paste(cimg, (0, 0))
    if nimg.height > 800: nimg = nimg.resize((2000, 800), Image.LANCZOS)
    hsh = 'ats/%x.png'%hash(nimg.tobytes())
    nimg.save(fp=hsh)
    return hsh

def gifcomp(path):
    cimg = Image.open(path)
    frames = []
    dura = 0
    fn = 0
    while cimg:
        frames.append(cimg.copy())
        fn += 1
        try: cimg.seek(fn)
        except EOFError: break
    hsh = ''
    for i in range(len(frames)):
        dura += frames[i].info['duration']
        nimg = Image.new('RGBA', (int(cimg.height * prop), cimg.height), (255, 255, 255, 0))
        nimg.paste(frames[i], (0, 0))
        if i < 10: hsh += '%x'%hash(nimg.tobytes())
        frames[i] = nimg
    hsh = 'ats/%x.gif'%hash(hsh)
    frames[0].save(hsh, save_all = True, append_images = frames[1:], duration = dura / len(frames), loop = True, transparency = 0)
    if Path(hsh).stat().st_size > 7.9*1024*1024: return path
    return hsh

if __name__ == '__main__':
    pth = comp('tmp.gif')
