
import pygame
from pygame import *
from pygame import Color
from random import *
from math import *
from tkinter import *
from tkinter import filedialog
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
                  
def draw_back():
    global offset
    
    # Current color 
    draw.rect(screen, color, curcolorRect)
    draw.rect(screen, OUTLINE, curcolorRect,1)

    draw_color_tab()

    # Draws color tabs
    if cTab == "colorTab":
        draw_color()
    elif cTab == "paletteTab":
        draw_palette()
    elif cTab == "codeTab":
        draw_code_tab()
    
    for i in range(len(tools)):
        # draws outline 
        if tool == tools[i]:
            draw.rect(screen, N25COLOR,tool_Rects[i],2) 
        else:
            draw.rect(screen, GREY,tool_Rects[i],2)

    if grid_on == True:
         draw.rect(screen, N25COLOR,tool_Rects[8],2) 

    draw_stamp()
    draw_size()

def draw_canvas():
    global canvas,color,clickCanvas

    if canvasRect.collidepoint(mx,my):
        if mb[0]:
            # tools
            
            if tool == "pencil":
                draw.line(canvas, color, (omx,omy), (mx,my), size)
                
            elif tool == "brush" or tool == "eraser":
                d = dist((omx,omy),(mx,my))
                for i in range(int(d)):
                    # connect the dots and draws circles
                    if d >0:
                        sx = (mx-omx)/d
                        sy = (my-omy)/d
                        if tool == "brush":
                            draw.circle(canvas, color, (omx+i*sx,omy+i*sy), size)
                        elif tool == "eraser":
                            draw.circle(canvas, WHITE, (omx+i*sx,omy+i*sy), size) # don't know how to overlay transperent sorry
            elif tool == "spray":
                for i in range(size):
                    # randomly draws spray specs
                    x = randint(mx-size, mx+size)  
                    y = randint(my-size, my+size)
                    draw.circle(canvas, color, (x,y), size**(1/6))

            elif tool == "dropper" and clickCanvas == True:
                
                canvas.fill((0,0,0,0))
                canvas.blit(back,(0,0))
                dropColor = canvas.get_at((mx,my)) # gets color

                # draw color preview cirlce
                draw.circle(canvas, dropColor, (mx,my), 20)
                draw.circle(canvas, DARKGREY, (mx,my), 20, 2)      
                draw.line(canvas, DARKGREY, (mx-5,my), (mx+5,my))  
                draw.line(canvas, DARKGREY, (mx,my+5), (mx,my-5))

            for i in range(1,len(stamps)):
                if tool == stamps[i] and clickCanvas == True:
                    # scales and blits image
                    img = aspect_scale(stamp_img[i],(size**2, size**2))
                    x = img.get_width() // 2
                    y = img.get_height() // 2
                    canvas.blit(img,(mx-x,my-y))
                    clickCanvas = False

            if tool == "shapes" and clickCanvas == True:

                canvas.fill((0,0,0,0))
                canvas.blit(back,(0,0))
                r = Rect(start[0],start[1],mx-start[0],my-start[1])
                r.normalize()

                if shapeType == "rectangle":
                    if shapeStyle == "Filled":
                        draw.rect(canvas, fillColor,r)
                    draw.rect(canvas, color,r,size)

                elif shapeType == "ellipse":
                    if shapeStyle == "Filled":
                        draw.ellipse(canvas, fillColor,r)
                    draw.ellipse(canvas,color,r,size)

                elif shapeType == "triangle":
                    # draws isoceles triangle with first click as mirror center
                    dx = start[0]-mx
                    point1 = (start[0]+dx,my)
                    point2 = (start[0]-dx,my)
                    if shapeStyle == "Filled":
                        draw.polygon(canvas,fillColor,(start,point1,point2))
                    draw.polygon(canvas,color,(start,point1,point2),size)

                elif shapeType == "polygon":
                    pass

            if tool == "line" and clickCanvas == True:

                canvas.fill((0,0,0,0))
                canvas.blit(back,(0,0))
                d = dist(start,(mx,my))
                
                if lineType == "dotted":
                    for i in range(int(d/(size*3))+1):
                        if d >0:
                            # draws evenly spaced out circles
                            sx = size * 3 * (mx-start[0])/d
                            sy = size * 3 * (my-start[1])/d
                            draw.circle(canvas, color, (start[0]+i*sx,start[1]+i*sy), size**1/2)
                else: 
                    draw.line(canvas, color, start, (mx,my),size)

def draw_popUp(page):
    ''' draws an empty pop-up window on current screen, can then be used for different windows
    '''
    screen.fill((30,30,30),special_flags=BLEND_SUB)     # special flag makes background darker by subtracting rgb values
    window = Rect(400,250,450,300)
    exitRect = Rect(820,265,15,15)
        
    action = None
    screen.set_clip(window)
    
    running = True
    while running:

        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        mouse_down = False
        
        for evt in event.get():          
            if evt.type == QUIT:
                screen.set_clip()
                quit()
            if evt.type == MOUSEBUTTONDOWN:
                mouse_down = True
            if evt.type == MOUSEBUTTONUP:
                if exitRect.collidepoint(mx,my):
                    screen.set_clip()
                    return
                
        # window
        draw.rect(screen,LIGHTGREY,window)
        draw.rect(screen,DARKERGREY,window,3)

        # exit button
        if exitRect.collidepoint(mx,my):
            drawExit(exitRect,True)
        else:
            drawExit(exitRect,False)

        if page == "save":
            action = save_window(mouse_down)

        if action != None:
            screen.set_clip()
            return action

        myClock.tick(60)
        display.flip()

def save_window(mouse_down):
    '''options for user to save canvas or entire screen
    '''

    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    
    options = ["Save Canvas","Save Screen"]
    action = None
    
    for i in range(len(options)):
        rect = Rect(475,310+110*i,300,70)
        draw.rect(screen,GREY,rect,2)
        pic = headFont.render(options[i], True, OUTLINE)
        blit_center(screen,rect,pic)
        
        if rect.collidepoint(mx,my):
            draw.rect(screen,WHITE,rect,2)
            if mouse_down == True:
                return options[i]

def shape_window():

    global shapeStyle, shapeType, fillColor
    
    draw.rect(screen, GREY, shapeRect)
    draw.rect(screen, N25COLOR, tool_Rects[6], 2)

    # filled/unfilled options
    for i in range (len(shapeStyles)):
        draw.rect(screen, LIGHTGREY,shapeStyleRects[i])
        styleName = shapeStyles[i]
        stylePic = sysFont.render(styleName, True, OUTLINE)
        blit_center(screen,shapeStyleRects[i],stylePic)

    # shape types
    for i in range (len(shapeTypes)):
        draw.rect(screen, LIGHTGREY,shapeTypeRects[i])
        blit_center(screen,shapeTypeRects[i],shape_img[i])

    running = True
    while running:

        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        
        for evt in event.get():
            if evt.type == QUIT:
                quit()
            if evt.type == MOUSEBUTTONDOWN:
                if not shapeRect.collidepoint(mx,my):
                    # exits window
                    return
                
                for i in range (len(shapeStyleRects)):
                    # if click on style, change
                    if shapeStyleRects[i].collidepoint(mx,my):
                        shapeStyle = shapeStyles[i]
                        
                for i in range (len(shapeTypeRects)):
                    if shapeTypeRects[i].collidepoint(mx,my):
                        shapeType = shapeTypes[i]
                        
        if fillRect.collidepoint(mx,my) and mb[0]:       
            fillColor = color[:]
            
        # outlines
        for i in range (len(shapeStyles)):
            if shapeStyle == shapeStyles[i]:
                draw.rect(screen, N25COLOR,shapeStyleRects[i],1)
            else:
                draw.rect(screen, OUTLINE,shapeStyleRects[i],1)

        for i in range (len(shapeTypes)):
            if shapeType == shapeTypes[i]:
                draw.rect(screen, N25COLOR,shapeTypeRects[i],1)
            else:
                draw.rect(screen, OUTLINE,shapeTypeRects[i],1)

        # color previews
        draw.rect(screen, color, outlineRect)
        draw.rect(screen, fillColor, fillRect)
        draw.rect(screen, OUTLINE, (outlineRect.x,fillRect.y,outlineRect.w+fillRect.w,fillRect.h),1)
        draw.line(screen, OUTLINE, (fillRect.x,fillRect.y),(fillRect.x,fillRect.bottom-1),1)
            
        myClock.tick(60)
        display.flip()

def line_window():

    global lineType
    
    draw.rect(screen, GREY, lineRect)
    draw.rect(screen, N25COLOR, tool_Rects[7], 2)

    for i in range (len(lineTypes)):
        draw.rect(screen, LIGHTGREY,lineTypeRects[i])
        blit_center(screen,lineTypeRects[i],line_img[i])

    running = True
    while running:

        mx, my = mouse.get_pos()
        mb = mouse.get_pressed()
        
        for evt in event.get():
            if evt.type == QUIT:
                quit()
            if evt.type == MOUSEBUTTONDOWN:
                if not lineRect.collidepoint(mx,my):
                    return
                
                for i in range (len(lineTypeRects)):
                    # if click on type, change
                    if lineTypeRects[i].collidepoint(mx,my):
                        lineType = lineTypes[i]

        for i in range (len(lineTypes)):
            if lineType == lineTypes[i]:
                draw.rect(screen, N25COLOR,lineTypeRects[i],1)
            else:
                draw.rect(screen, OUTLINE,lineTypeRects[i],1)
            
        myClock.tick(60)
        display.flip()
        
def draw_color_tab():
    ''' draws the top tab part of the color window
    '''
    draw.rect(screen, GREY,colorBarRect)
    draw.rect(screen, OUTLINE,colorBarRect,1)
    
    for i in range (len(cTabs)):
        draw.line(screen, OUTLINE,(tabRects[i].left,tabRects[i].top),(tabRects[i].left,tabRects[i].bottom),1)

        # tab labels
        tabName = cTabs[i][:-3]
        tabPic = sysFont.render(tabName, True, WHITE)
        blit_center(screen,tabRects[i],tabPic)

        if cTab == cTabs[i]:
            draw.rect(screen, OUTLINE,tabRects[i],3) # bolds outline
            
def draw_color():
    ''' draws the color selection plates
    '''
    # hue selection rect
    for i in range (0,360): 
        h = pygame.Color(0)
        h.hsla = i,100,50,100
        draw.rect(screen, h, (1200, 100+(i*150/361), 30, 1))

    # saturation and lightness of hue rect
    for s in range (0,100):
        for l in range (0,100):
            c = pygame.Color(0) 
            c.hsla = hue, s, l, 100
            draw.rect(screen, c, (1000+(s*200/100), 100+(l*150/100), 2, 2))
            
    # indicators
    screen.set_clip(colorRect)  # make not draw out of area
    draw.rect(screen, OUTLINE, (1200, 100+(hue*150/361)-2,30,4), 1)               # current hue
    draw.circle(screen, OUTLINE, (1000+(sat*200/100),100+(lum*150/100)), 4, 1)    # current saturation and luminocity
    screen.set_clip(None)

    # outlines
    draw.line(screen, OUTLINE, (1200,100), (1200,249), 1)
    draw.rect(screen, OUTLINE, (1000,100,230,150), 1)

def draw_palette():
    '''draws color palette saver tab
    '''
    draw.rect(screen, GREY, colorRect)
    # draws rects with saved colors
    for i in range (len(palColors)):
        draw.rect(screen, palColors[i], palRects[i])
        draw.rect(screen, OUTLINE, palRects[i],1)

def draw_code_tab():

    draw.rect(screen, GREY, colorRect)
    hue,sat,lum,a = color.hsla

    labels = ["hexadecimal","","H","S","L","","R","G","B"]
    hexd = rgb_to_hex(color)
    values = [hexd,"",int(hue),int(sat),int(lum),"",int(color.r),int(color.g),int(color.b)]

    for i in range(len(labels)):
        if labels[i] != "":

            label = sysFont.render(labels[i], True, WHITE)
            if type(values[i]) != str:
                val = sysFont.render(str(int(values[i])), True, WHITE)
            else:
                val = sysFont.render(values[i], True, WHITE)

            y = 108+i*15
            rect = Rect(1150,y,60,13)

            draw.rect(screen,DARKGREY,rect)
            screen.blit(label,(1030,y))
            blit_center(screen,rect,val)
    
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def draw_stamp():
    '''draws the stamp rects with offsets
    '''
    global stampRects                   # variable can be used outside of function
    screen.set_clip(stampRect)          # only shows stamps in rect area
    draw.rect(screen, GREY, stampRect)
    stampRects = []
    for i in range(len(stamps)//2):
        # creates rect areas with offset
        y = 335 + i*105 - offset
        stampRects.append (Rect(1015, y, 95,95))
        stampRects.append (Rect(1120, y, 95,95))
    for i in range (len(stampRects)):
        # displays images
        draw.rect(screen, DARKGREY, stampRects[i],2) # outline
        img = aspect_scale(stamp_img[i], (85,85))
        blit_center(screen,stampRects[i],img)
        if tool == stamps[i]:
            draw.rect(screen, N25COLOR,stampRects[i],2)
    screen.set_clip(None)

def draw_size():
    # size slider
    draw.polygon(screen, GREY, ((82,710-5),(82,710+5),(300,710+15),(300,710-15))) # back
    draw.circle(screen, DARKGREY, (82,710),5) 
    draw.circle(screen, DARKGREY, (300,710),15)
    # draws indicator for current size; ranging from 1-30 pixels
    x = 80 + (size*235/30)
    draw.circle(screen,LIGHTGREY,(x,710),3)

def drawExit(square,mouseover):
    ''' draws an x button
        if mouseover the button, change color and bold
    '''
    rect = Rect(square)
    color = (255,0,0)
    size = 3
    
    if mouseover == True:
        color = WHITE
        size = 4
        
    draw.line(screen,color,(rect.x,rect.y),(rect.x+rect.w, rect.y+rect.h),size)
    draw.line(screen,color,(rect.x+rect.w,rect.y),(rect.x, rect.y+rect.h),size)
    
    
def blit_center(surface,rect,img):
    ''' returns the x y position to blit image in center of rect
    '''
    x = rect.x + (rect.w - img.get_width()) // 2
    y = rect.y + (rect.h - img.get_height()) // 2

    surface.blit(img,(x,y))

def aspect_scale(img,box):
    # Scales img while keeping aspect ratio
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = box[0]/float(ix)
        sy = scale_factor * iy
        if sy > box[1]:
            scale_factor = box[1]/float(iy)
            sx = scale_factor * ix
            sy = box[1]
        else:
            sx = box[0]
    else:
        # fit to height
        scale_factor = box[1]/float(iy)
        sx = scale_factor * ix
        if sx > box[0]:
            scale_factor = box[0]/float(ix)
            sx = box[0]
            sy = scale_factor * iy
        else:
            sy = box[1]
    return transform.scale(img, (sx,sy))

def blit_text_outline(text,color,outcolor,pos):
    ''' blits text on screen with an outline of chosen color'''

    outlinePic = sysFont.render(text, True, outcolor)
    for x in -1,1:
        for y in -1,1:
            screen.blit(outlinePic,(pos[0]+x,pos[1]+y))
    
    txtPic = sysFont.render(text, True, color)
    screen.blit(txtPic,pos)
    
root = Tk()
root.withdraw()
files = [(".png", "*.png"),  # file types can save/load as
            (".jpg", "*.jpg"), 
            (".jpeg", "*.jpeg")]

screen = display.set_mode((1250,800))
WHITE = (255,255,255)
BLACK = (0)
N25COLOR = (136,68,153) # used as box highlights as well
KNDCOLOR = (187,101,136)
MFYCOLOR = (136,137,204)
ENCOLOR = (204,170,135)
MZKCOLOR = (228,168,202)

GREY = Color("#68617E")
LIGHTGREY = Color("#B9B7C9")
DARKGREY = Color("#4F4869")
DARKERGREY = Color("#3E365A")
OUTLINE = Color("#322C4B")

color = Color(0,0,0,100) # selected color
hue,sat,lum,a = color.hsla

font.init()
sysFont = font.SysFont('couriernew',13) #font used for formatting
headFont = font.SysFont('couriernew',20)

tool = "pencil"
size = 5
a = 100
clickCanvas = False

background = image.load(resource_path("img/bg.jpg"))
screen.blit(background,(0,0))

canvasRect = Rect(80,60,900,610)
canvas = Surface((1250,800),SRCALPHA)
layer = Surface((1250,800),SRCALPHA)
canvas.set_clip(canvasRect)
canvas.fill(WHITE)
back = Surface((0,0))

grid = Surface((900,610),SRCALPHA)
for x in range(0,901,40):
    for y in range(0,610,40):
        draw.line(grid, DARKGREY,(x,0),(x,610))
        draw.line(grid, DARKGREY,(0,y),(900,y))
grid.set_alpha(100)
grid_on = False

draw.rect(screen, WHITE, canvasRect)
draw.rect(screen, OUTLINE, (78,58,904,614),2) #border

leftBar = Rect(0,0,60,800)
draw.rect(screen, DARKGREY, leftBar)
draw.line(screen,OUTLINE,(60,0),(60,800))

icon = image.load(resource_path(f"img/icon.png"))
icon = transform.scale(icon,(30,30))
screen.blit(icon,(310,15))
header = headFont.render("25-ji, Nightcord de. Themed Paint Program", True, OUTLINE)
screen.blit(header,(350, (60-header.get_height())//2))

text = sysFont.render("Made by @Eternalstar", True, OUTLINE)
text2 = sysFont.render("Contact: eternalstar1232@gmail.com", True, OUTLINE)
screen.blit(text,(screen.get_width()-text.get_width()-30,730))
screen.blit(text2,(screen.get_width()-text2.get_width()-30,755))


tools = ["pencil","brush","eraser","spray","dropper","text","shapes","line","grid"]     # relative lists of tools 
tool_Rects = []                                                                         # and their respective rects
for i in range (len(tools)):
    # creates evenly spaced rect areas
    rect = Rect(10,30+i*50,40,40)
    tool_Rects.append(rect)
    draw.rect(screen, GREY, rect)
    # load icons
    img = image.load(resource_path(f"img/{tools[i]}.png"))
    img = transform.scale(img, (30,30))
    blit_center(screen,rect,img)


# shape tool
shapeRect = Rect(60,360,170,110)
shapeStyles = ["Filled","Unfilled"]
shapeStyle = shapeStyles[0]
shapeStyleRects = []
for i in range (len(shapeStyles)):
    shapeStyleRects.append(Rect(70+i*75,370,75,20))
shapeTypes = ["rectangle","ellipse","triangle"]
shape_images = ["img/shape_r.png","img/shape_e.png","img/shape_t.png","img/shape_p.png"]
shapeType = shapeTypes[0]
shape_img = []
shapeTypeRects = []
for i in range (len(shapeTypes)):
    shapeTypeRects.append(Rect(70+i*40,400,30,30))
    img = image.load(resource_path(shape_images[i]))
    img = transform.scale(img, (25,25))
    shape_img.append(img)

fillColor = pygame.Color(WHITE)         # color used to fill shape
outlineRect = Rect(70,440,20,20)        # color used to outline shape
fillRect = Rect(90,440,130,20)


# line tool
lineRect = Rect(60,420,90,50)
lineTypes = ["solid","dotted"]
line_images = ["img/lineSolid.png","img/lineDotted.png"]
lineType = lineTypes[0]
line_img = []
lineTypeRects = []
for i in range (len(lineTypes)):
    lineTypeRects.append(Rect(70+i*40,430,30,30))
    img = image.load(resource_path(line_images[i]))
    img = transform.scale(img, (25,25))
    line_img.append(img)

        
functions = ["undo","restart","redo",
             "load","save"]
function_Rects = []
for i in range (3):
    rect = Rect(10,530+i*50,40,40)
    function_Rects.append(rect)
    draw.rect(screen, GREY, rect)
    img = image.load(resource_path(f"img/{functions[i]}.png"))
    img = transform.scale(img, (30,30))
    blit_center(screen,rect,img)
    
for i in range (2):
    rect = Rect(10,690+i*50,40,40)
    function_Rects.append(rect)
    draw.rect(screen, GREY, rect)
    img = image.load(resource_path(f"img/{functions[3+i]}.png"))
    img = transform.scale(img, (30,30))
    blit_center(screen,rect,img)

laststeps = []  # used to save images for undo
nextsteps = []  # used to save images for redo

# color picker
colorBarRect = Rect(1000,80,230,20) # top part
colorRect = Rect(1000,100,230,150)


cTabs = ["colorTab","paletteTab","codeTab"]
tabRects = []
for i in range (len(cTabs)):        # appends evenly spaced rects 
    tabRects.append(Rect(1000+i*230/3,80,230/3,20))
    
cTab = cTabs[0]                     # default set tab for color

# Color picker tab
curcolorRect = (1156,60,73,15)      # current color preview
shadeRect = Rect(1000,100,200,150)  # shade
hueRect = Rect(1200,100,30,150)     # hue

# Palette tab
palColors = []                      # saved colors
for i in range(24):
    palColors.append(Color(WHITE))
palRects = []                       # their rects
for x in range (6):
    for y in range (4):
        palRects.append(Rect(1000+25/2+x*35,100+15/2+y*35,30,30))
    
# default colors
dfcolors = [WHITE, BLACK, GREY, DARKGREY, N25COLOR, KNDCOLOR, MFYCOLOR, ENCOLOR, MZKCOLOR]
dfcRect = []
for i in range(len(dfcolors)):
    # displays
    dfcRect.append(Rect(1000+i*26,260,21,21))
    draw.rect(screen, dfcolors[i], dfcRect[i])
    draw.rect(screen, OUTLINE, dfcRect[i],1)

drop = False

# stamps
offset = 0      # scroll up and down of area
stampRect = Rect(1000,320,230,350)
draw.rect(screen, GREY, stampRect)
stampBarRect = (1000,290,230,30)
draw.rect(screen, DARKGREY, stampBarRect)

stamps = ["add","empty","stampMk1","stampMk2","stampKnd1","stampKnd2","stampMfy1","stampMfy2","stampEna1","stampEna2","stampMzk1","stampMzk2"]
stamp_img = []
for i in range (len(stamps)):
    img = image.load(resource_path(f"img/{stamps[i]}.png"))
    stamp_img.append(img)

sizeRect = Rect (80,690,235,40)

running = True
myClock = time.Clock()
omx,omy = 0,0

running = True
while running:
                        
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    for evt in event.get():
        if evt.type == QUIT:
            running = False
            
        if evt.type == pygame.MOUSEWHEEL:
            # calculates offset
            if stampRect.collidepoint(mx,my):
                offset -= evt.y*10
            
        if evt.type == MOUSEBUTTONDOWN: 
            
            if canvasRect.collidepoint(mx,my):
                clickCanvas = True
                start = mx,my
                # saves canvas before anything is drawn
                back = canvas.copy()

                if tool == "text":
                    
                    try: # does not crash if user ignores
                        fontt = font.SysFont(None, size*5)      # default font
                        txt = input("Input text:")
                        txtPic = fontt.render(txt, True, size)

                        # Adjust position and blits
                        x = max(0, mx - txtPic.get_width()/2)  
                        y = max(0, my - txtPic.get_height()/2)
                        canvas.blit(txtPic, (x, y))
                        
                    except:
                        pass
                    
            else:
                clickCanvas = False

                # change color tab
                for i in range(len(cTabs)):
                    if tabRects[i].collidepoint(mx,my):
                        cTab = cTabs[i]

                # use default colors
                for i in range (len(dfcolors)):
                    if dfcRect[i].collidepoint(mx,my):
                        color = Color(dfcolors[i])          # saves as independent variable
                        hue,sat,lum,a = color.hsla

                # change tools
                for i in range (8): 
                    if tool_Rects[i].collidepoint(mx,my):
                        tool = tools[i]

                # grid tool
                if tool_Rects[8].collidepoint(mx,my):
                    grid_on = not grid_on                   # toggles True/False

                # stamp tool
                if stampRect.collidepoint(mx,my):           # if click inside displayed rect
                    if stampRects[0].collidepoint(mx,my):
                        # upload own stamp
                        file = filedialog.askopenfilename(filetypes = [("Picture files", "*.png;*.jpg;*.jpeg")])
                        if file != '':                      # does not try to do it if no file
                            print (f"Imported file {file}")
                            img = image.load(file)
                            # replaces original img in stamp_img[1]
                            stamp_img.insert(1,img) 
                            del stamp_img[2]
                            
                    for i in range(1,len(stamps)):
                        # use stamps
                        if stampRects[i].collidepoint(mx,my):
                            tool = stamps[i]

                # shape/line windows
                for i in range (6,8):
                    if tool_Rects[i].collidepoint(mx,my):
                        windowBack = screen.copy()          # stores screen of before window was opened
                        if i == 6:
                            shape_window()                  # opens shape selection window
                        elif i == 7:
                            line_window()
                        screen.blit(windowBack,(0,0))       # returns to original state
                        continue

                # use functions: ["undo","restart","redo","load","save"]

                # undo
                if function_Rects[0].collidepoint(mx,my):
                    if len(laststeps) > 0:
                        giveback = len(laststeps) - 2
                        canvas.fill((0,0,0,0))
                        canvas.blit(laststeps[giveback],(0,0))
                        nextsteps.append (laststeps[len(laststeps)-1])  # adds to redo list if want to go back
                        del laststeps[len(laststeps)-1]                 # prevents from using current screen

                # restart
                if function_Rects[1].collidepoint(mx,my):
                    canvas.fill(WHITE)          # clears canvas

                # redo
                if function_Rects[2].collidepoint(mx,my):
                    if len(nextsteps) > 0:
                        giveback = len(nextsteps) - 2
                        canvas.fill((0,0,0,0))
                        canvas.blit(nextsteps[giveback],(0,0))
                        laststeps.append (nextsteps[len(nextsteps)-1]) # re-adds to undo list to use again
                        del nextsteps[len(nextsteps)-1] 
                    
                # load
                if function_Rects[3].collidepoint(mx,my):
                    file = filedialog.askopenfilename(filetypes = [("Picture files", "*.png;*.jpg;*.jpeg")])
                    if file != '':                              #does not try to load if user exits
                        # load to canvas
                        img = image.load(file)
                        img = aspect_scale(img,(900,610))       # fit to canvas
                        canvas.blit(img,(80,60))                # blits to canvas
                        print (f"Loaded {file} to canvas")

                # save
                if function_Rects[4].collidepoint(mx,my):
                    back = screen.copy()
                    action = draw_popUp("save")
                    screen.blit(back,(0,0))
                    print(True)
                    name = filedialog.asksaveasfilename(filetypes = files, defaultextension = files) ###(filetypes = files, defaultextension = files)
                    if name != '':
                        if action == "Save Canvas":
                            image = Surface((900,610))
                            image.blit(screen,(0,0),((80,60),(900,610)))
                        elif action == "Save Screen":
                            image = screen
                        pygame.image.save(image,name)
                        print (f"Saved to {name}")
                    action = None
                    
        if evt.type == MOUSEBUTTONUP:
            
            if clickCanvas == True:
                
                if tool == "dropper":
                    canvas.fill((0,0,0,0))
                    canvas.blit(back,(0,0))
                    
                    dropColor = canvas.get_at((mx,my))
                    color = Color(dropColor[:])
                    hue,sat,lum,a = color.hsla
                    
                s = canvas.copy()
                laststeps.append(s)
                
                clickCanvas = False

                    

    # check interactions-----

    if clickCanvas != True:
        
        if mb[0]:

            # use size slider
            if sizeRect.collidepoint(mx,my):
                size = int((mx-80)/235 * 30)
                if size <= 0:
                    size = 1
                        
        if cTab == "colorTab":
            if mb[0]:
                if hueRect.collidepoint(mx,my):
                    # changes hue
                    hue = (my-100)/150*360
                if shadeRect.collidepoint(mx,my):
                    # changes shade
                    sat = (mx - 1000) / 200 * 100 
                    lum = (my - 100) / 150 * 100
                color.hsla = hue,sat,lum,a

        if cTab == "paletteTab":
            # uses palette
            for i in range(len(palRects)):
                if palRects[i].collidepoint(mx,my):
                    if mb[0]:                               # saves color
                        palColors[i] = Color(color[:])      # replaces original color with new color
                    if mb[2]:                               # uses color
                        color = Color(palColors[i][:])
                        hue,sat,lum,a = color.hsla

    # Limit offset
    if offset < 0:       # min offset
        offset = 0
    elif offset > 300:   # max offset
        offset = 300
                    
    draw_back()
    draw_canvas()
    screen.blit(canvas,(0,0))
    
    if grid_on == True:
        screen.blit(grid,(80,60))
    
    omx,omy = mx,my
    myClock.tick(60)
    
    display.flip()
    
quit()






