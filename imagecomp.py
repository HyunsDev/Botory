from PIL import Image
import os

prop = 2.5

def comp(path):
    typ = getfiletype(path)
    if typ == 'img':
        cimg = Image.open(path)
        md = False
        if cimg.height >= cimg.width / prop:
            md = True
            nimg = Image.new('RGBA', (int(cimg.height * prop), cimg.height), (0, 0, 0, 0))
            luc = int((cimg.height * prop - cimg.width) / 2)
            nimg.paste(cimg, (luc, 0))
            cimg = nimg
        if not md: return path
        hsh = 'ats/%x.png'%hash(cimg.tobytes())
        cimg.save(fp=hsh)
        return hsh
    else: return path

def getfiletype(path):
    try: cimg = Image.open(path)
    except: return
    return 'gif' if 'loop' in cimg.info else 'img'

if __name__ == '__main__':
    pth = comp('2021.png')
    Img(fp=pth).show()
