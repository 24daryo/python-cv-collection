import taichi as ti

ti.init(arch=ti.gpu)

width, height = 480, 360
gui = ti.GUI("Poler", res=(width, height), fast_gui=True)
colors = ti.Vector.field(3, dtype=float, shape=(width, height))

@ti.func
def xy2pol(x, y):
    return ti.math.atan2(y, x), ti.math.length(ti.Vector([x, y]))

@ti.func
def hsv2rgb(h, s, v)->ti.Vector:
    rgb = ti.math.clamp(ti.abs(ti.math.mod(h*6.0+ti.Vector([0.0, 4.0, 2.0]), 6.0)-3.0)-1.0, 0.0, 1.0)
    return v * ti.math.mix(ti.Vector([1.0, 1.0, 1.0]), rgb, s)

@ti.kernel
def render():
    for i, j in colors:
        x, y = i/width-0.5, j/height-0.5
        s, t = xy2pol(x, y)
        hue = s / (2 * ti.math.pi)
        r, g, b = hsv2rgb(hue, t, 1.0)
        colors[i, j] = ti.Vector([r, g, b])

while gui.running:
    render()
    gui.set_image(colors)
    gui.show()