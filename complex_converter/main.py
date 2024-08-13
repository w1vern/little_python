import math

def algToEx(x, y):
    r = (x**2+y**2)**0.5
    xfi = math.acos(x/r)*180/math.pi
    yfi = math.asin(y/r)*180/math.pi
    fi = xfi * yfi / abs(yfi)
    return (r, fi)

def exToAlg(r, fi):
    return (r * math.cos(fi * math.pi / 180), r * math.sin(fi * math.pi / 180))


#print(algToEx(-0.902, -1.015))
print(exToAlg(415.575, -17.338))