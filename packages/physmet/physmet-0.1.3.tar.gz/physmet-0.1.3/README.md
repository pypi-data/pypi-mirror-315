# physmet

This package provides support for defining and working with objects that
comprise numeric data and an associated metric unit.

```python
import physmet
x = physmet.axis.coordinates([3, 6, 9], 'm')
y = physmet.axis.coordinates([4, 8], 'J')
a = physmet.array([[1.5, 2.0], [-3.0, 10.0], [-1.5, -10.0]], 'cm / s', axes={'x': x, 'y': y})
a
s = physmet.scalar(8.0, unit='s')
s
a * s
z = physmet.axis.coordinates([0, 2, 4, 6], 'mK')
z.unit
z.unit.quantity
b = physmet.array([[1.5, 2.0, -1.0, -1.0], [-3.0, 10.0, 1.0, 1.0]], 'au^2', axes={'y': y, 'z': z})
a
b
a / b
```
