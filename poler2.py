import taichi as ti

ti.init(arch=ti.gpu)

PI2 = 2*ti.math.pi

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

org = ti.Vector.field(3, dtype=float, shape=(width, height))
@ti.kernel
def tex():
    for i, j in org:
        x, y = i/width, j/height
        r, g, b = hsv2rgb(x, y, 1.0)
        org[i, j] = ti.Vector([r, g, b])

@ti.kernel
def tex2pol():
    for i, j in colors:
        x, y = i/width-0.5, j/height-0.5
        s, t = xy2pol(x, y)
        s = ti.math.mod(s, PI2)
        x_org, y_org = int(width*s/PI2), int(height*t)
        colors[i, j] = org[x_org, y_org]

while gui.running:
    tex()
    tex2pol()
    gui.set_image(colors)
    gui.show()