from tkinter import *
from math import *
import time
import numpy as np

root = Tk()
root.title("Винтовая поверхность")
root.geometry("640x600")
root.resizable(False, False)

PRECISION = 30

WIDTH = 640
HEIGHT = 481

def changeAlpha(val):
    global polys
    polys = genPolys(screw, 4 * pi, -2, 2, PRECISION, float(alpha.get()), float(beta.get()))
    draw()

def changeBeta(val):
    global polys
    polys = genPolys(screw, 4 * pi, -2, 2, PRECISION, float(alpha.get()), float(beta.get()))
    draw()

canvas = Canvas(bg="white", width=WIDTH, height=HEIGHT)
alpha = Scale(orient=HORIZONTAL, length=200, from_=0.5, to=2., resolution=0.1, command=changeAlpha)
beta = Scale(orient=HORIZONTAL, length=200, from_=0.5, to=2., resolution=0.1, command=changeBeta)
alpha.pack(anchor=CENTER, expand=1)
beta.pack(anchor=CENTER, expand=1)
canvas.pack(anchor=CENTER, expand=1)

def screw(u, v, alpha, beta):
    return np.array([(alpha * u * cos(u) ) * cos(u), (beta * u * sin(u)), v])

def genPolys(f, maxU, minV, maxV, precision, alpha, beta):
    polys = []
    for t1 in range(precision):
        for t2 in range(precision):
            polys.append((
                    f(((t1) * maxU / precision), ((t2 - precision / 2) * (maxV - minV) / precision), alpha, beta),
                    f(((t1) * maxU / precision), ((t2 + 1 - precision / 2) * (maxV - minV) / precision), alpha, beta),
                    f(((t1+1) * maxU / precision), ((t2 + 1 - precision / 2) * (maxV - minV) / precision), alpha, beta),
                    ))
            polys.append((
                    f(((t1) * maxU / precision), ((t2 - precision / 2) * (maxV - minV) / precision), alpha, beta),
                    f(((t1+ 1) * maxU / precision), ((t2 - precision / 2) * (maxV - minV) / precision), alpha, beta),
                    f(((t1+1) * maxU / precision), ((t2 + 1 - precision / 2) * (maxV - minV) / precision), alpha, beta),
                    ))
    return polys

polys = genPolys(screw, 4 * pi, -2, 2, PRECISION, float(alpha.get()), float(beta.get()))

def translate(point, vec):
    trMat = np.eye(4)
    trMat[0][3] = vec[0]
    trMat[1][3] = vec[1]
    trMat[2][3] = vec[2]
    return trMat.dot(point)

def scale(point, vec):
    trMat = np.eye(4)
    trMat[0][0] = vec[0]
    trMat[1][1] = vec[1]
    trMat[2][2] = vec[2]
    return trMat.dot(np.append(point, 1)[:, np.newaxis])

def rotateX(vec, phi):
    rMat = np.eye(4)
    rMat[1][1] = cos(phi)
    rMat[1][2] = -sin(phi)
    rMat[2][1] = sin(phi)
    rMat[2][2] = cos(phi)
    return rMat.dot(vec)

def rotateY(vec, phi):
    rMat = np.eye(4)
    rMat[0][0] = cos(phi)
    rMat[0][2] = sin(phi)
    rMat[2][0] = -sin(phi)
    rMat[2][2] = cos(phi)
    return rMat.dot(vec)

def rotateZ(vec, phi):
    rMat = np.eye(4)
    rMat[0][0] = cos(phi)
    rMat[0][1] = -sin(phi)
    rMat[1][0] = sin(phi)
    rMat[1][1] = cos(phi)
    return rMat.dot(vec)

tMat = 64*np.eye(4)

def drawGrid():
    for i in range(21):
        Xline = [[-10, -10 + i, 0, 1],[10,-10 + i,0, 1]]
        Yline = [[10 - i, -10, 0, 1],[10 - i,10,0, 1]]
        Zline = [[0, 0, 10, 1],[0,0,-10, 1]]
        canvas.create_line(int(tMat.dot(Xline[0])[0] + WIDTH / 2),int(tMat.dot(Xline[0])[1] + HEIGHT / 2),int(tMat.dot(Xline[1])[0] + WIDTH / 2),int(tMat.dot(Xline[1])[1] + HEIGHT / 2))
        canvas.create_line(int(tMat.dot(Yline[0])[0] + WIDTH / 2),int(tMat.dot(Yline[0])[1] + HEIGHT / 2),int(tMat.dot(Yline[1])[0] + WIDTH / 2),int(tMat.dot(Yline[1])[1] + HEIGHT / 2))
        canvas.create_line(int(tMat.dot(Zline[0])[0] + WIDTH / 2),int(tMat.dot(Zline[0])[1] + HEIGHT / 2),int(tMat.dot(Zline[1])[0] + WIDTH / 2),int(tMat.dot(Zline[1])[1] + HEIGHT / 2))
    for i in range(-10, 11):
        ZStroke = [[-0.125, 0, i,1], [0.125, 0, i,1]]
        canvas.create_line(int(tMat.dot(ZStroke[0])[0] + WIDTH / 2),int(tMat.dot(ZStroke[0])[1] + HEIGHT / 2),int(tMat.dot(ZStroke[1])[0] + WIDTH / 2),int(tMat.dot(ZStroke[1])[1] + HEIGHT / 2))

def draw():
    canvas.delete("all")
    drawGrid()
    for poly in polys:
        polyProj = list(map(lambda x : tMat.dot(np.append(x, 1)[:, np.newaxis]), poly))
        canvas.create_polygon(int(polyProj[0][0] + WIDTH / 2), int(polyProj[0][1] + HEIGHT / 2), int(polyProj[1][0] + WIDTH / 2), int(polyProj[1][1] + HEIGHT / 2), int(polyProj[2][0] + WIDTH / 2), int(polyProj[2][1] + HEIGHT / 2), fill='#0000FF')

draw()

def keydown(e):
    global tMat
    if e.char == "w":
        tMat *= 1.1
    elif e.char == "s":
        tMat *= 1/1.1
    elif e.keycode == 111:
        tMat = rotateX(tMat, (pi / 16))
    elif e.keycode == 116:
        tMat = rotateX(tMat, (-pi / 16))
    elif e.keycode == 113:
        tMat = rotateY(tMat, (pi / 16))
    elif e.keycode == 114:
        tMat = rotateY(tMat, (-pi / 16))
    draw()

root.bind("<KeyPress>", keydown)

root.mainloop()
