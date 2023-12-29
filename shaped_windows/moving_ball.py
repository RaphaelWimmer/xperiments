# (C) 2023 Raphael Wimmer <raphael@winterwind.org>
# licensed under CC-0 - do what you want with it

from Xlib import X, display
from Xlib.ext import shape
import time

# Initialize display and screen
d = display.Display()
s = d.screen()

# Create a window
win = s.root.create_window(300, 300, 100, 100, 1, s.root_depth)

# Set window properties
win.set_wm_name('Ball')
win.map()

# Shape the window as a circle
shape_mask = win.create_pixmap(100, 100, 1)
gc = shape_mask.create_gc(foreground=0, background=0)
shape_mask.fill_rectangle(gc, 0, 0, 100, 100, 0)
gc.change(foreground=1)
shape_mask.fill_arc(gc, 0, 0, 100, 100, 0, 360*64)
win.shape_mask(shape.SO.Set, shape.SK.Bounding, 0, 0, shape_mask)
wgc = win.create_gc(foreground=s.white_pixel)
win.fill_rectangle(wgc, 0, 0, 100, 100)

# Move the window
x_speed = y_speed = 2
while True:
    geometry = win.get_geometry()
    x, y = geometry.x, geometry.y

    # Check for screen borders and bounce
    if x + geometry.width >= s.width_in_pixels or x <= 0:
        x_speed = -x_speed
    if y + geometry.height >= s.height_in_pixels or y <= 0:
        y_speed = -y_speed

    win.configure(x=x+x_speed, y=y+y_speed)
    win.fill_rectangle(wgc, 0, 0, 100, 100)
    d.sync()
    time.sleep(0.01)
