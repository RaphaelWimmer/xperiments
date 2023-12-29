# (C) 2023 Raphael Wimmer <raphael@winterwind.org>
# licensed under CC-0 - do what you want with it

from Xlib import X, display
from Xlib.ext import shape
from PIL import Image
import time

def next_color(s):
    #colors = [s.white_pixel, s.black_pixel]
    cm = s.default_colormap
    color_names = "red green blue white turquoise magenta orange yellow".split(" ")
    colors = [cm.alloc_named_color(c).pixel for c in color_names]
    idx = 0
    while True:
        yield colors[idx]
        idx = (idx + 1) % len(colors)


# Initialize display and screen
d = display.Display()
s = d.screen()

logo = Image.open("./dvd_video_logo.bmp")
w,h = logo.width, logo.height
# Create a window
win = s.root.create_window(300, 300, w, h, 1, s.root_depth)

# Set window properties
win.set_wm_name('Bouncing Logo')
win.map()

# Shape the window as a circle
shape_mask = win.create_pixmap(w, h, 1)
gc = shape_mask.create_gc(foreground=1, background=0)
shape_mask.fill_rectangle(gc, 0, 0, w, h, 0)
#gc.change(foreground=1)
#shape_mask.fill_arc(gc, 0, 0, 100, 100, 0, 360*64)
shape_mask.put_pil_image(gc, 0, 0, logo)
win.shape_mask(shape.SO.Set, shape.SK.Bounding, 0, 0, shape_mask)
wgc = win.create_gc(foreground=s.white_pixel)
win.fill_rectangle(wgc, 0, 0, w, h)

# Move the window
x_speed = y_speed = 2
colors = next_color(s)
color = next(colors)
while True:
    geometry = win.get_geometry()
    x, y = geometry.x, geometry.y

    # Check for screen borders and bounce
    if x + geometry.width >= s.width_in_pixels or x <= 0:
        x_speed = -x_speed
        color = next(colors)
        wgc.change(foreground=color)
    if y + geometry.height >= s.height_in_pixels or y <= 0:
        y_speed = -y_speed
        color = next(colors)
        wgc.change(foreground=color)
    x = x + x_speed
    y = y + y_speed
    # make sure that we stay within the screen even if there are X11 hickups with updating the position
    x = max(min(x, s.width_in_pixels - geometry.width), 0)
    y = max(min(y, s.height_in_pixels - geometry.height), 0)

    win.configure(x=x, y=y)
    win.fill_rectangle(wgc, 0, 0, w, h)
    d.sync()
    time.sleep(1/60)
