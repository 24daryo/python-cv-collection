import taichi as ti

ti.init(arch=ti.gpu, default_ip=ti.i32)

width, height = 480, 360
gui = ti.GUI("xor", res=(width, height), fast_gui=True)
colors = ti.Vector.field(3, dtype=float, shape=(width, height))

k = 0x4567

@ti.func
def xor16(n):
    n ^= n << 7 & 0xFFFF
    n ^= n >> 9 & 0xFFFF
    n ^= n << 8 & 0xFFFF
    return n*k & 0xFFFF

@ti.kernel
def render():
    for i, j in colors:
        rand_x = xor16(i*width+j)/0xFFFF
        colors[i, j] = ti.Vector([rand_x, rand_x, rand_x])

while gui.running:
    render()
    gui.set_image(colors)
    gui.show()
