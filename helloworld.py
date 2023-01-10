import taichi as ti

ti.init(arch=ti.gpu)

width = 480
height = 360
gui = ti.GUI("Hello World", res=(width, height), fast_gui=True)
colors = ti.Vector.field(3, dtype=float, shape=(width, height))

@ti.kernel
def render(frame: int):
    for i, j in colors:
        color = ti.Vector([i/width, j/height, 0.0])
        colors[i, j] = color

frame = 0
while gui.running:
    render(frame)
    gui.set_image(colors)
    gui.show()
    frame += 1