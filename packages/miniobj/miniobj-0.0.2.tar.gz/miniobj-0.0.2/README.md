# miniobj
Minimum wavefront .obj file parser in Python

## Installation
```bash
pip install miniobj
```

## Usage
```python
from miniobj import MiniObj

obj_mesh = MiniObj("mesh.obj")
# convert quad faces to triangles, ngon faces are not supported yet
obj_mesh.load(as_triangles=False)

obj_mesh.export("output.obj")
```

## Quantization
```python
obj_mesh.scale_unit() # scale min coord to 0, max coord to 1
obj_mesh.quantize(bins=64) # quantize to 64x64x64
obj_mesh.export("output.obj")
```

Check out [main.py](main.py) for more examples.
