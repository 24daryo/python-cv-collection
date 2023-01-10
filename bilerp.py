import taichi as ti

ti.init(arch=ti.gpu)

width = 480
height = 360
gui = ti.GUI("Bileap", res=(width, height), fast_gui=True)
colors = ti.Vector.field(3, dtype=float, shape=(width, height))

@ti.kernel
def render(frame: int):
    red = ti.Vector([1.0, 0.0, 0.0])
    green = ti.Vector([0.0, 1.0, 0.0])
    yellow = ti.Vector([1.0, 1.0, 0.0])
    blue = ti.Vector([0.0, 0.0, 1.0])
    
    for i, j in colors:
        top = ti.math.mix(red, yellow, i/width)
        bottom = ti.math.mix(blue, green, i/width)
        colors[i, j] = ti.math.mix(bottom, top, j/height)

frame = 0
while gui.running:
    render(frame)
    gui.set_image(colors)
    gui.show()
    frame += 1