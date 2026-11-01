"""Export uploadable article diagrams; requires Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent / 'assets'
ROOT.mkdir(exist_ok=True)
W, H = 1600, 900
BG, INK, MUTED = '#101c30', '#eef4ff', '#a8bad4'
TEAL, BLUE, GOLD = '#55dcc1', '#83b5ff', '#ffcc7a'
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(size, bold=False): return ImageFont.truetype(BOLD if bold else FONT, size)
def canvas(title, sub):
    im = Image.new('RGB', (W,H), BG)
    d = ImageDraw.Draw(im)
    d.text((80,55), title, font=font(49,True), fill=INK)
    d.text((80,125), sub, font=font(27), fill=MUTED)
    return im,d

def box(d, xy, title, lines, color=TEAL):
    x,y,x2,y2=xy
    d.rounded_rectangle(xy,radius=22,fill='#1c2c45',outline=color,width=3)
    d.text((x+25,y+22),title,font=font(31,True),fill=color)
    for i,line in enumerate(lines): d.text((x+25,y+78+i*39),line,font=font(26),fill=INK)

def arrow(d, a,b, color=MUTED):
    d.line([a,b],fill=color,width=5)
    import math
    angle=math.atan2(b[1]-a[1],b[0]-a[0])
    pts=[b,(b[0]-20*math.cos(angle-.5),b[1]-20*math.sin(angle-.5)),(b[0]-20*math.cos(angle+.5),b[1]-20*math.sin(angle+.5))]
    d.polygon(pts,fill=color)

def save(im,name): im.save(ROOT / name)

im,d=canvas('Stop paying twice for the same vector', 'Apache Spark + real embeddings + a bounded LRU cache')
box(d,(65,355,380,535),'Ticket text',['Model + exact text'],BLUE)
box(d,(470,355,800,535),'Check LRU',['Already stored?'],BLUE)
box(d,(930,215,1530,410),'HIT: vector found',['Read cached vector; skip Ollama','Move this entry to most recent'],TEAL)
box(d,(930,510,1530,745),'MISS: no vector',['Call Ollama to generate embedding','Store vector as most recent','If full, evict least recently used'],GOLD)
arrow(d,(380,445),(470,445))
arrow(d,(800,405),(930,315),TEAL)
arrow(d,(800,485),(930,610),GOLD)
d.text((65,800),'Both paths return the ticket with its embedding.',font=font(35,True),fill=INK)
save(im,'01-cover.png')

im,d=canvas('One partition invocation. One independent cache.', 'Model calls are skipped on hits; caches are not shared between partitions.')
box(d,(80,230,430,420),'Driver',['Partitioned ticket RDD'],BLUE)
box(d,(575,230,1040,420),'Partition 0',['Tickets 101–105','Own LRU: capacity 2'])
box(d,(575,520,1040,710),'Partition 1',['Tickets 106–110','Own LRU: capacity 2'])
box(d,(1190,370,1520,600),'Ollama',['/api/embed','Misses only'],GOLD)
arrow(d,(430,315),(575,315));arrow(d,(430,345),(575,615))
arrow(d,(1040,325),(1190,430));arrow(d,(1040,615),(1190,530))
d.text((80,800),'A repeat in another partition can still be a miss.',font=font(32,True),fill=INK)
save(im,'02-partition-flow.png')

im,d=canvas('Cache hit or miss: what happens next?', 'Capacity = 2 entries. Cache state is shown AFTER each ticket is processed.')
rows=[('1','Return','MISS',['Return']),('2','Payment','MISS',['Payment','Return']),('3','Return','HIT',['Return','Payment']),('4','Order','MISS',['Order','Return']),('5','Payment','MISS',['Payment','Order'])]
actions=[('Call model; store Return','No eviction: space available'),
         ('Call model; store Payment','No eviction: space available'),
         ('Reuse stored Return vector','No model call; move Return first'),
         ('Call model; store Order','Evict Payment: least recently used'),
         ('Call model; store Payment','Evict Return: least recently used')]
d.text((65,190),'INPUT / LOOKUP',font=font(22,True),fill=MUTED)
d.text((350,190),'ACTION',font=font(22,True),fill=MUTED)
d.text((985,190),'CACHE: MOST → LEAST RECENT',font=font(22,True),fill=MUTED)
for n,(step,text,status,state) in enumerate(rows):
 y=245+n*105
 color=TEAL if status=='HIT' else GOLD
 d.line((65,y-12,1530,y-12),fill='#2c405b',width=1)
 d.text((65,y),f'{step}. {text}',font=font(29,True),fill=INK)
 d.text((65,y+39),status,font=font(23,True),fill=color)
 d.text((350,y),actions[n][0],font=font(27,True),fill=color)
 d.text((350,y+39),actions[n][1],font=font(23),fill=MUTED)
 for j,item in enumerate(state):
  x=985+j*280
  d.rounded_rectangle((x,y,x+245,y+72),radius=14,fill='#1c2c45',outline=TEAL if j==0 else BLUE,width=3)
  d.text((x+20,y+21),item,font=font(27),fill=INK)
 if len(state)==2: arrow(d,(1235,y+36),(1260,y+36))
d.text((65,820),'5 tickets  •  4 model calls  •  1 reused vector',font=font(33,True),fill=TEAL)
save(im,'03-lru-sequence.png')

im,d=canvas('An embedding cache is one piece of the RAG pipeline', 'This project implements enrichment. Indexing and retrieval are extensions.')
box(d,(80,230,1520,430),'IMPLEMENTED: Spark embedding enrichment', ['Tickets → partition-local cache → model on misses → ticket + embedding'],TEAL)
arrow(d,(800,430),(800,510))
box(d,(80,510,1520,710),'EXTENSION: indexing and question answering', ['Write vectors + text → embed question → retrieve evidence → generate answer'],BLUE)
d.text((80,800),'Fewer embedding calls ≠ a faster similarity-search algorithm.',font=font(34,True),fill=GOLD)
save(im,'04-rag-boundary.png')

# Optional animation for preview/sharing, with a static PNG fallback for Medium.
frames=[]
for n,(step,text,status,state) in enumerate(rows):
 im,d=canvas('Watch a capacity-two LRU cache',f'Step {step} of 5  |  Input: {text}  |  {status}')
 for j,item in enumerate(state):
  x=260+j*580
  box(d,(x,320,x+490,550),item,['Stored embedding', 'Most recent' if j==0 else 'Least recent'],TEAL if j==0 else BLUE)
 d.text((80,670),actions[n][0],font=font(35,True),fill=TEAL if status=='HIT' else GOLD)
 d.text((80,730),actions[n][1],font=font(30),fill=INK)
 frames.append(im.resize((960,540)))
frames[0].save(ROOT/'05-lru-animation.gif',save_all=True,append_images=frames[1:],duration=1600,loop=0)
print('Exported four PNG diagrams and one GIF.')
