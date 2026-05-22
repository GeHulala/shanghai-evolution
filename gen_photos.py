"""
Generate simple but recognizable illustrated photos of Shanghai's famous buildings.
These are drawn programmatically with PIL - no internet needed.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos')
os.makedirs(OUT, exist_ok=True)

W, H = 800, 500

def draw_sky(d):
    """Simple sky gradient"""
    for y in range(350):
        t = y / 350
        r = max(80, int(200 - 65*t))
        g = max(150, int(210 - 70*t))
        b = max(180, int(235 - 55*t))
        d.rectangle([(0,y),(W,y)], fill=(r,g,b))

def draw_river(d):
    """River at bottom"""
    for y in range(330, 355):
        t = (y-330)/25
        r = max(40, int(74 - 40*t))
        g = max(80, int(140 - 60*t))
        b = max(140, int(212 - 72*t))
        d.rectangle([(0,y),(W,y)], fill=(r,g,b))

def draw_ground(d, y0=355):
    """Green ground"""
    for y in range(y0, H):
        t = (y-y0)/(H-y0)
        r = max(40, int(90 - 50*t))
        g = max(70, int(138 - 68*t))
        b = max(20, int(58 - 38*t))
        d.rectangle([(0,y),(W,y)], fill=(r,g,b))

def draw_building(d, x1, x2, y1, y2, color, window_color=(255,236,160)):
    """Draw a simple building with windows"""
    d.rectangle([(x1,y1),(x2,y2)], fill=color)
    # Windows
    for x in range(x1+10, x2-5, 22):
        for y in range(y1+15, y2-10, 22):
            d.rectangle([(x,y),(x+12,y+14)], fill=window_color)

# ====== 1. Peace Hotel (1929) ======
def gen_peace_hotel():
    img = Image.new('RGB', (W, H), (135, 206, 235))
    dd = ImageDraw.Draw(img)
    draw_sky(dd); draw_river(dd); draw_ground(dd)
    # Main building - Art Deco style
    draw_building(dd, 250, 480, 160, 355, (200, 176, 136))
    # Roof decoration
    dd.rectangle([(250,155),(480,168)], fill=(80,70,50))
    # Side wings
    dd.rectangle([(170,230),(245,355)], fill=(184,152,120))
    dd.rectangle([(485,200),(580,355)], fill=(184,152,120))
    # Windows details on wings
    for x in range(180, 245, 22):
        for y in range(240, 345, 22):
            dd.rectangle([(x,y),(x+12,y+14)], fill=(255,236,160))
    for x in range(495, 575, 22):
        for y in range(210, 345, 22):
            dd.rectangle([(x,y),(x+12,y+14)], fill=(255,236,160))
    # Base
    dd.rectangle([(245,340),(500,355)], fill=(138,122,90))
    # Sun
    dd.ellipse([(650,30),(730,110)], fill=(255,215,0))
    dd.ellipse([(650,30),(730,110)], fill=(255,200,50,30))
    # Clouds
    dd.ellipse([(100,50),(200,80)], fill=(255,255,255,180))
    dd.ellipse([(120,40),(180,70)], fill=(255,255,255,200))
    dd.ellipse([(500,80),(620,115)], fill=(255,255,255,160))
    dd.ellipse([(530,70),(590,100)], fill=(255,255,255,190))
    path = os.path.join(OUT, '01-peace-hotel.jpg')
    img.save(path, 'JPEG', quality=92)
    print(f'01-peace-hotel.jpg: {os.path.getsize(path)} bytes')

# ====== 2. Oriental Pearl Tower (1995) ======
def gen_oriental_pearl():
    img = Image.new('RGB', (W, H), (10, 10, 46))
    dd = ImageDraw.Draw(img)
    # Night sky
    for y in range(460):
        t = y/460
        dd.rectangle([(0,y),(W,y)], fill=(max(2,int(10+20*t)), max(2,int(10+20*t)), max(8,int(46-30*t))))
    # Stars
    import random
    random.seed(42)
    for _ in range(60):
        x=random.randint(0,W); y=random.randint(0,420)
        s=random.randint(1,2); b=random.randint(100,255)
        dd.ellipse([(x,y),(x+s,y+s)], fill=(b,b,b))
    # Ground
    for y in range(455, H):
        dd.rectangle([(0,y),(W,y)], fill=(26,42,58))
    # Main pole
    dd.rectangle([(395,100),(405,460)], fill=(180,180,180))
    # Three spheres
    dd.ellipse([(370,120),(430,170)], fill=(204,68,119))
    dd.ellipse([(345,220),(455,320)], fill=(204,68,119))
    dd.ellipse([(365,380),(435,440)], fill=(187,51,102))
    # Glow around spheres
    for i in range(3, 0, -1):
        alpha = 15 // i
        c = (255, 100, 150, alpha)
    # Antenna
    dd.rectangle([(398,60),(402,100)], fill=(200,200,200))
    # Reflection on ground
    dd.ellipse([(350,455),(450,470)], fill=(204,68,119,40))
    path = os.path.join(OUT, '02-oriental-pearl.jpg')
    img.save(path, 'JPEG', quality=92)
    print(f'02-oriental-pearl.jpg: {os.path.getsize(path)} bytes')

# ====== 3. Jin Mao Tower (1999) ======
def gen_jinmao():
    img = Image.new('RGB', (W, H), (135, 206, 235))
    dd = ImageDraw.Draw(img)
    draw_sky(dd); draw_river(dd); draw_ground(dd)
    # Main tower - stepped pagoda style
    dd.rectangle([(330,30),(470,355)], fill=(136,152,168))
    # Top crown
    dd.rectangle([(385,22),(415,30)], fill=(212,175,55))
    # Stepped sections
    for y in range(42, 340, 24):
        margin = int(y * 0.04)
        dd.rectangle([(330+margin,y),(470-margin,y+14)], fill=(200,216,239))
    # Base
    dd.rectangle([(310,340),(490,355)], fill=(122,128,138))
    # Side buildings
    dd.rectangle([(220,250),(320,355)], fill=(122,138,154))
    dd.rectangle([(480,230),(580,355)], fill=(122,138,154))
    # Windows on sides
    for x in range(230, 315, 22):
        for y in range(260, 345, 22):
            dd.rectangle([(x,y),(x+12,y+14)], fill=(220,240,255))
    for x in range(490, 575, 22):
        for y in range(240, 345, 22):
            dd.rectangle([(x,y),(x+12,y+14)], fill=(220,240,255))
    # Sun
    dd.ellipse([(30,40),(90,100)], fill=(255,215,0))
    path = os.path.join(OUT, '03-jinmao.jpg')
    img.save(path, 'JPEG', quality=92)
    print(f'03-jinmao.jpg: {os.path.getsize(path)} bytes')

# ====== 4. Shanghai WFC (2008) ======
def gen_swfc():
    img = Image.new('RGB', (W, H), (135, 206, 235))
    dd = ImageDraw.Draw(img)
    draw_sky(dd); draw_river(dd); draw_ground(dd)
    # Main tower - with bottle opener hole
    dd.rectangle([(310,20),(490,355)], fill=(176,192,208))
    # The "hole" at the top
    dd.polygon([(400,80),(370,130),(430,130)], fill=(100,150,220))
    dd.polygon([(400,80),(370,130),(430,130)], fill=(90,140,210,100))
    # Windows
    for y in range(32, 340, 24):
        margin = 8
        dd.rectangle([(315+margin,y),(485-margin,y+14)], fill=(216,228,244))
    # Top crown
    dd.rectangle([(385,12),(415,20)], fill=(200,208,216))
    # Side buildings
    dd.rectangle([(240,260),(305,355)], fill=(138,154,170))
    dd.rectangle([(495,240),(560,355)], fill=(138,154,170))
    # Sun
    dd.ellipse([(680,55),(750,125)], fill=(255,215,0))
    path = os.path.join(OUT, '04-swfc.jpg')
    img.save(path, 'JPEG', quality=92)
    print(f'04-swfc.jpg: {os.path.getsize(path)} bytes')

# ====== 5. China Art Museum (2010) ======
def gen_china_art_museum():
    img = Image.new('RGB', (W, H), (135, 206, 235))
    dd = ImageDraw.Draw(img)
    draw_sky(dd); draw_river(dd); draw_ground(dd)
    # Red crown top
    dd.polygon([(400,15),(240,100),(560,100)], fill=(221,74,74))
    # Main body
    dd.rectangle([(230,100),(570,355)], fill=(204,58,58))
    # Top beam
    dd.rectangle([(330,25),(470,100)], fill=(204,58,58))
    dd.rectangle([(370,15),(430,25)], fill=(170,40,40))
    # Windows
    for x in range(250, 560, 28):
        for y in range(115, 345, 30):
            dd.rectangle([(x,y),(x+18,y+22)], fill=(255,210,110))
    # Base
    dd.rectangle([(230,340),(570,355)], fill=(170,40,40))
    # Side buildings
    dd.rectangle([(180,250),(225,355)], fill=(122,90,58))
    dd.rectangle([(575,240),(620,355)], fill=(122,90,58))
    path = os.path.join(OUT, '05-china-art-museum.jpg')
    img.save(path, 'JPEG', quality=92)
    print(f'05-china-art-museum.jpg: {os.path.getsize(path)} bytes')

# ====== 6. Shanghai Tower (2015) ======
def gen_shanghai_tower():
    img = Image.new('RGB', (W, H), (135, 206, 235))
    dd = ImageDraw.Draw(img)
    draw_sky(dd); draw_river(dd); draw_ground(dd)
    # Main tower - twisted spiral
    dd.rectangle([(345,8),(455,355)], fill=(184,196,208))
    # Top crown
    dd.rectangle([(380,4),(420,8)], fill=(192,200,208))
    # Spiral lines
    for y in range(18, 345, 20):
        offset = int(10 * (1 - y/345))
        dd.rectangle([(345+offset,y),(455-offset,y+14)], fill=(216,234,248))
    # Side buildings
    dd.rectangle([(230,280),(340,355)], fill=(122,138,154))
    dd.rectangle([(460,260),(570,355)], fill=(122,138,154))
    # Windows on sides
    for x in range(240, 335, 20):
        for y in range(290, 350, 20):
            dd.rectangle([(x,y),(x+12,y+12)], fill=(200,220,240))
    for x in range(470, 565, 20):
        for y in range(270, 350, 20):
            dd.rectangle([(x,y),(x+12,y+12)], fill=(200,220,240))
    path = os.path.join(OUT, '06-shanghai-tower.jpg')
    img.save(path, 'JPEG', quality=92)
    print(f'06-shanghai-tower.jpg: {os.path.getsize(path)} bytes')


# Generate all 6 photos
print('Generating building photos...\n')
gen_peace_hotel()
gen_oriental_pearl()
gen_jinmao()
gen_swfc()
gen_china_art_museum()
gen_shanghai_tower()
print('\nAll 6 photos generated successfully!')