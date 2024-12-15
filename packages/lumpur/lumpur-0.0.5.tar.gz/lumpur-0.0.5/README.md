# lumpur
learn to use methods for processing unclear response


## contribute
+ Learn the instructions on [first-contributions](https://github.com/firstcontributions/first-contributions).
+ Apply to this repository what you learn there.


## features
+ `Polynomial` class in `num.polynomial` module.
+ `plot_binary()` function in `dat.dataviz` module.
+ `binary()`function in `dat.clasdata` module.
+ `abbr()` function in `use.misc.info` module.


## examples
Following are some examples of lumpur.

### polynomial
```py
from lumpur.num.polynomial import Polynomial

p1 = Polynomial([1, 2, 3])
print('y1 =', p1)
p2 = Polynomial([0, -2, 5, 6, 9])
print('y2 =', p2)
p3 = p1 + p2
print('y3 =', p3)
```
```
y1 = 1 + 2x + 3x^2
y2 = -2x + 5x^2 + 6x^3 + 9x^4
y3 = 1 + 8x^2 + 6x^3 + 9x^4
```

```py
from lumpur.num.polynomial import Polynomial

p1 = Polynomial([1, -2, 3])
print('y1 =', p1)
p2 = Polynomial([-2, 1])
print('y2 =', p2)
p3 = p1 * p2
print('y3 =', p3)
```
```
y1 = 1 - 2x + 3x^2
y2 = -2 + x^1
y3 = -2 + 5x - 8x^2 + 3x^3
```

### circular decision boundary
$$
0.41 - 0.8x - 1.2y + x^2 + y^2 = 0
$$
```py
import lumpur.dat.clasdata as ldc
import lumpur.dat.dataviz as ldv

coeffs = [[0.41], [-0.8, -1.2], [1, 0, 1]]
r1 = [0, 1.05, 0.05]
r2 = [0, 1.05, 0.05]
df = ldc.binary(coeffs, r1=r1, r2=r2)
ldv.plot_binary(df)
```
<img src="https://raw.githubusercontent.com/dudung/lumpur/refs/heads/main/docs/images/dataviz_circular.png" width="300" />

### linear decision boundary
$$
-x + y = 0
$$
```py
import lumpur.dat.clasdata as ldc
import lumpur.dat.dataviz as ldv

coeffs = [[0], [-1, 1]]
df = ldc.binary(coeffs)
ldv.plot_binary(df)
```
<img src="https://raw.githubusercontent.com/dudung/lumpur/refs/heads/main/docs/images/dataviz_linear.png" width="300" />

### abbreviation
```py
import lumpur.use.misc.info as info

print(info.abbrv())
```

```
learn to use methods for processing unclear response
```
