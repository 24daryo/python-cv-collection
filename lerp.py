import taichi as ti

ti.init(arch=ti.gpu)

width = 480
height = 360
gui = ti.GUI("Gradation", res=(width, height), fast_gui=True)
colors = ti.Vector.field(3, dtype=float, shape=(width, height))

@ti.kernel
def render(frame: int):
    red = ti.Vector([1.0, 0.0, 0.0])
    green = ti.Vector([0.0, 1.0, 0.0])
    for i, j in colors:
        # mix(x, y, a) == x*(1-a) + y*a
        color = ti.math.mix(red, green, i/width) # x軸でグラデーション
        colors[i, j] = color

frame = 0
while gui.running:
    render(frame)
    gui.set_image(colors)
    gui.show()
    frame += 1