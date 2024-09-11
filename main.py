import pyglet
from pyglet.window import key
from pyglet.window import mouse
import data
from cube import cube, sphere

window = pyglet.window.Window()

window.set_size(data.width, data.height)

Batch = pyglet.graphics.Batch()

cube1 = cube(Batch)
#sphere1 = sphere(Batch)

# region toggle
@window.event
def on_key_press(symbol, modifiers):
    pass
# endregion

# region mouse
@window.event
def on_mouse_press(x, y, button, modifiers):
    pass

@window.event
def on_mouse_release(x, y, button, modifiers):
    pass
# endregion

@window.event
def on_draw():
    window.clear()
    Batch.draw()

def update(dt):
    cube1.update()
    #sphere1.update()

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()