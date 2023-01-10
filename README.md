# python-cv-collection
Visualization processing collection implemented with python library taichi

## 簡単な使い方

### GPUの指定

```python
import taichi as ti

ti.init(arch=ti.gpu)    # 自動
ti.init(arch=ti.cuda)   # Cuda
ti.init(arch=ti.opengl) # OpenGL
ti.init(arch=ti.vulkan) # Vulkan
ti.init(arch=ti.matal)  # Metal
ti.init(arch=ti.cpu)    # CPU
```

### 2次元データ構造

`ti.field`を用いる

```python
import taichi as ti
width = 480
height = 360
pixels = ti.field(dtype=float, shape=(width, height))
```

### 並列化

`@ti.kernel`を用いる。外側のループのみ並列化が有効なので注意

```python
@ti.kernel
def fill():
    total = 0
    for i in range(10): # Parallelized
        for j in range(5): # Serialized in each parallel thread
            total += i * j

    if total > 10:
        for k in range(5):  # Not parallelized because it is not at the outermost scope
```

fields型は以下の記述のように並列化できる

```python
@ti.kernel
def paint(t: float):
    for i, j in pixels:  # Parallelized over all pixels
        pass
```

### データ構造

#### GUI

```python
width = 360
height = 480
gui = ti.GUI("Pathtracing", res=(width, height), fast_gui=True)
```

#### カラー画像

```python
width = 360
height = 480
colors = ti.Vector.field(3, dtype=float, shape=(width, height))
```

### Hello World

```python
import taichi as ti

ti.init(arch=ti.gpu)

width = 480
height = 360
gui = ti.GUI("Title here", res=(width, height), fast_gui=True)
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
```

## 便利な関数

```python
@ti.func
def xy2pol(x, y):
    return ti.math.atan2(y, x), ti.math.length(ti.Vector([x, y]))

@ti.func
def pol2xy(s, t):
    return t * ti.math.cos(s), t * ti.math.sin(s)

@ti.func
def hsv2rgb(h, s, v)->ti.Vector:
    rgb = ti.math.clamp(ti.abs(ti.math.mod(h*6.0+ti.Vector([0.0, 4.0, 2.0]), 6.0)-3.0)-1.0, 0.0, 1.0)
    return v * ti.math.mix(ti.Vector([1.0, 1.0, 1.0]), rgb, s)
```