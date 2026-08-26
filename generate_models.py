# -*- coding: utf-8 -*-
"""
程序化生成低多边形 .obj 模型 + 纹理贴图 - 2D生存建造游戏资源包
共44个模型：18个资源物品 + 26个建筑
增强版：高面数 + 程序化纹理 + 细节增强
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
TEX_SIZE = 256


# ============================================================
# 纹理生成
# ============================================================
def _noise(img, draw, base_color, intensity=30):
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            n = random.randint(-intensity, intensity)
            r = max(0, min(255, base_color[0] + n))
            g = max(0, min(255, base_color[1] + n))
            b = max(0, min(255, base_color[2] + n))
            pixels[x, y] = (r, g, b)


def gen_wood(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (110, 75, 45))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (110, 75, 45), 20)
    for i in range(20):
        y = random.randint(0, TEX_SIZE)
        color = (random.randint(70, 100), random.randint(45, 65), random.randint(25, 40))
        draw.line([(0, y), (TEX_SIZE, y + random.randint(-5, 5))], fill=color, width=random.randint(1, 3))
    for _ in range(3):
        cx, cy = random.randint(30, TEX_SIZE-30), random.randint(30, TEX_SIZE-30)
        r = random.randint(8, 20)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(60, 40, 20), width=2)
        draw.ellipse([cx-r//2, cy-r//2, cx+r//2, cy+r//2], outline=(50, 30, 15), width=1)
    img = img.filter(ImageFilter.SMOOTH)
    img.save(path)


def gen_stone(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (120, 120, 125))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (120, 120, 125), 35)
    for _ in range(8):
        x, y = random.randint(0, TEX_SIZE), random.randint(0, TEX_SIZE)
        points = [(x, y)]
        for _ in range(random.randint(3, 8)):
            x += random.randint(-30, 30); y += random.randint(-30, 30)
            points.append((x, y))
        draw.line(points, fill=(70, 70, 75), width=random.randint(1, 2))
    for _ in range(15):
        cx, cy = random.randint(0, TEX_SIZE), random.randint(0, TEX_SIZE)
        r = random.randint(3, 12)
        color = (random.randint(80, 110), random.randint(80, 110), random.randint(85, 115))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    img.save(path)


def gen_metal(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (170, 175, 180))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (170, 175, 180), 15)
    for _ in range(20):
        x1, y1 = random.randint(0, TEX_SIZE), random.randint(0, TEX_SIZE)
        x2 = x1 + random.randint(-50, 50); y2 = y1 + random.randint(-10, 10)
        draw.line([(x1, y1), (x2, y2)], fill=(130, 135, 140), width=1)
    draw.rectangle([0, 0, TEX_SIZE, 8], fill=(200, 205, 210))
    img.save(path)


def gen_meat(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (180, 80, 70))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (180, 80, 70), 25)
    for _ in range(12):
        y = random.randint(0, TEX_SIZE)
        color = (random.randint(140, 170), random.randint(55, 75), random.randint(50, 65))
        draw.line([(0, y), (TEX_SIZE, y + random.randint(-8, 8))], fill=color, width=random.randint(2, 5))
    for _ in range(8):
        cx, cy = random.randint(0, TEX_SIZE), random.randint(0, TEX_SIZE)
        r = random.randint(5, 15)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(220, 200, 180))
    img.save(path)


def gen_plant(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (60, 130, 55))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (60, 130, 55), 25)
    for _ in range(8):
        x = random.randint(0, TEX_SIZE)
        draw.line([(x, 0), (x + random.randint(-20, 20), TEX_SIZE)], fill=(40, 90, 35), width=1)
    for _ in range(10):
        cx, cy = random.randint(0, TEX_SIZE), random.randint(0, TEX_SIZE)
        r = random.randint(3, 10)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(35, 80, 30))
    img.save(path)


def gen_crystal(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (140, 70, 200))
    draw = ImageDraw.Draw(img)
    pixels = img.load()
    for y in range(TEX_SIZE):
        for x in range(TEX_SIZE):
            t = y / TEX_SIZE
            r = int(140 + 60 * (1 - t)); g = int(70 + 80 * (1 - t)); b = int(200 + 55 * t)
            pixels[x, y] = (r, g, b)
    draw.polygon([(0, 0), (TEX_SIZE//3, 0), (0, TEX_SIZE//2)], fill=(200, 150, 230))
    draw.polygon([(TEX_SIZE, 0), (TEX_SIZE*2//3, 0), (TEX_SIZE, TEX_SIZE//3)], fill=(180, 120, 220))
    img = img.filter(ImageFilter.SMOOTH)
    img.save(path)


def gen_water(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (60, 130, 180))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (60, 130, 180), 15)
    for _ in range(10):
        y = random.randint(0, TEX_SIZE)
        draw.line([(0, y), (TEX_SIZE, y + random.randint(-3, 3))], fill=(80, 160, 210), width=2)
    img.save(path)


def gen_leather(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (150, 110, 75))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (150, 110, 75), 30)
    for _ in range(50):
        cx, cy = random.randint(0, TEX_SIZE), random.randint(0, TEX_SIZE)
        draw.ellipse([cx-1, cy-1, cx+1, cy+1], fill=(110, 80, 50))
    img.save(path)


def gen_bone(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (230, 225, 210))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (230, 225, 210), 12)
    for _ in range(8):
        y = random.randint(0, TEX_SIZE)
        draw.line([(0, y), (TEX_SIZE, y + random.randint(-3, 3))], fill=(200, 195, 180), width=1)
    img.save(path)


def gen_paper(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (220, 205, 170))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (220, 205, 170), 15)
    for y in range(30, TEX_SIZE-20, 18):
        draw.line([(20, y), (TEX_SIZE-20, y)], fill=(160, 140, 100), width=1)
    img.save(path)


def gen_iron_ore(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (100, 95, 90))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (100, 95, 90), 30)
    for _ in range(6):
        points = []
        x, y = random.randint(0, TEX_SIZE), random.randint(0, TEX_SIZE)
        for _ in range(random.randint(4, 8)):
            x += random.randint(-25, 25); y += random.randint(-25, 25)
            points.append((x, y))
        draw.line(points, fill=(180, 170, 150), width=random.randint(2, 4))
    img.save(path)


def gen_berry(path):
    img = Image.new("RGB", (TEX_SIZE, TEX_SIZE), (170, 30, 50))
    draw = ImageDraw.Draw(img)
    _noise(img, draw, (170, 30, 50), 20)
    draw.ellipse([30, 20, 80, 60], fill=(220, 80, 100))
    img.save(path)


def gen_glass(path):
    img = Image.new("RGBA", (TEX_SIZE, TEX_SIZE), (180, 210, 230, 100))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, TEX_SIZE, 10], fill=(220, 240, 250, 150))
    draw.line([(0, TEX_SIZE//2), (TEX_SIZE, TEX_SIZE//2 - 20)], fill=(255, 255, 255, 80), width=3)
    img.save(path)


TEXTURE_GENS = {
    "wood": gen_wood, "stone": gen_stone, "metal": gen_metal,
    "meat": gen_meat, "plant": gen_plant, "crystal": gen_crystal,
    "water": gen_water, "leather": gen_leather, "bone": gen_bone,
    "paper": gen_paper, "iron_ore": gen_iron_ore, "berry": gen_berry,
    "glass": gen_glass,
}

MODEL_TEX = {
    "wood": "wood", "resin": "crystal", "rare_branch": "wood",
    "stone": "stone", "iron_ore": "iron_ore", "iron": "metal",
    "crystal": "crystal", "meat": "meat", "cooked_meat": "meat",
    "hide": "leather", "bone": "bone", "berry": "berry",
    "herb": "plant", "seed": "plant", "potion": "glass",
    "recipe_scroll": "paper", "codex": "leather", "clue_map": "paper",
    "foundation": "stone", "wall": "stone", "roof": "wood",
    "door": "wood", "window": "glass", "stairs": "stone",
    "furniture": "wood", "torch": "wood", "road": "stone",
    "flower_pot": "stone", "crate": "wood", "workbench": "wood",
    "furnace": "stone", "kitchen": "stone", "grinder": "metal",
    "shop": "wood", "order_board": "wood", "display_case": "wood",
    "defense_wall": "stone", "trap": "metal", "turret": "metal",
    "farm_plot": "plant", "greenhouse": "glass", "animal_pen": "wood",
    "water_trough": "stone", "fence": "wood",
}

MODEL_COLORS = {
    "wood": (0.55, 0.38, 0.22), "resin": (0.85, 0.65, 0.25),
    "rare_branch": (0.45, 0.30, 0.55), "stone": (0.55, 0.55, 0.58),
    "iron_ore": (0.45, 0.42, 0.40), "iron": (0.70, 0.72, 0.75),
    "crystal": (0.55, 0.30, 0.80), "meat": (0.70, 0.30, 0.28),
    "cooked_meat": (0.55, 0.32, 0.20), "hide": (0.65, 0.50, 0.35),
    "bone": (0.90, 0.88, 0.80), "berry": (0.75, 0.15, 0.25),
    "herb": (0.30, 0.60, 0.30), "seed": (0.70, 0.55, 0.30),
    "potion": (0.25, 0.55, 0.70), "recipe_scroll": (0.85, 0.78, 0.60),
    "codex": (0.60, 0.45, 0.30), "clue_map": (0.80, 0.72, 0.55),
    "foundation": (0.50, 0.48, 0.45), "wall": (0.60, 0.55, 0.48),
    "roof": (0.55, 0.30, 0.25), "door": (0.45, 0.30, 0.18),
    "window": (0.55, 0.60, 0.65), "stairs": (0.55, 0.52, 0.48),
    "furniture": (0.50, 0.35, 0.22), "torch": (0.40, 0.28, 0.18),
    "road": (0.45, 0.43, 0.40), "flower_pot": (0.60, 0.45, 0.35),
    "crate": (0.55, 0.40, 0.25), "workbench": (0.50, 0.35, 0.22),
    "furnace": (0.40, 0.38, 0.36), "kitchen": (0.50, 0.48, 0.45),
    "grinder": (0.55, 0.52, 0.50), "shop": (0.55, 0.40, 0.30),
    "order_board": (0.50, 0.38, 0.25), "display_case": (0.60, 0.55, 0.48),
    "defense_wall": (0.45, 0.42, 0.40), "trap": (0.40, 0.38, 0.35),
    "turret": (0.45, 0.48, 0.52), "farm_plot": (0.40, 0.30, 0.20),
    "greenhouse": (0.55, 0.65, 0.70), "animal_pen": (0.50, 0.38, 0.25),
    "water_trough": (0.45, 0.43, 0.40), "fence": (0.50, 0.35, 0.22),
}


# ============================================================
# ObjBuilder
# ============================================================
class ObjBuilder:
    def __init__(self, name="model"):
        self.name = name
        self.verts = []
        self.faces = []

    def _add_v(self, x, y, z):
        self.verts.append((x, y, z))
        return len(self.verts) - 1

    def add_box(self, cx, cy, cz, w, h, d):
        hw, hh, hd = w/2, h/2, d/2
        v = [self._add_v(cx-hw, cy-hh, cz-hd), self._add_v(cx+hw, cy-hh, cz-hd),
             self._add_v(cx+hw, cy+hh, cz-hd), self._add_v(cx-hw, cy+hh, cz-hd),
             self._add_v(cx-hw, cy-hh, cz+hd), self._add_v(cx+hw, cy-hh, cz+hd),
             self._add_v(cx+hw, cy+hh, cz+hd), self._add_v(cx-hw, cy+hh, cz+hd)]
        self.faces += [(v[0],v[1],v[2]),(v[0],v[2],v[3]),(v[5],v[4],v[7]),(v[5],v[7],v[6]),
                       (v[4],v[0],v[3]),(v[4],v[3],v[7]),(v[1],v[5],v[6]),(v[1],v[6],v[2]),
                       (v[3],v[2],v[6]),(v[3],v[6],v[7]),(v[4],v[5],v[1]),(v[4],v[1],v[0])]

    def add_cylinder(self, cx, cy, cz, r, h, sides=16):
        hh = h/2
        bottom, top = [], []
        for i in range(sides):
            a = 2*math.pi*i/sides
            x, z = cx + r*math.cos(a), cz + r*math.sin(a)
            bottom.append(self._add_v(x, cy-hh, z))
            top.append(self._add_v(x, cy+hh, z))
        for i in range(sides):
            j = (i+1)%sides
            self.faces += [(bottom[i],bottom[j],top[j]),(bottom[i],top[j],top[i])]
        tc = self._add_v(cx, cy+hh, cz)
        for i in range(sides):
            j = (i+1)%sides
            self.faces.append((tc, top[i], top[j]))
        bc = self._add_v(cx, cy-hh, cz)
        for i in range(sides):
            j = (i+1)%sides
            self.faces.append((bc, bottom[j], bottom[i]))

    def add_cone(self, cx, cy, cz, r, h, sides=16):
        hh = h/2
        bottom = []
        for i in range(sides):
            a = 2*math.pi*i/sides
            x, z = cx + r*math.cos(a), cz + r*math.sin(a)
            bottom.append(self._add_v(x, cy-hh, z))
        tip = self._add_v(cx, cy+hh, cz)
        for i in range(sides):
            j = (i+1)%sides
            self.faces.append((bottom[i], bottom[j], tip))
        bc = self._add_v(cx, cy-hh, cz)
        for i in range(sides):
            j = (i+1)%sides
            self.faces.append((bc, bottom[j], bottom[i]))

    def add_sphere(self, cx, cy, cz, r, rings=8, segs=12):
        vertices = []
        for i in range(rings+1):
            phi = math.pi * i / rings
            for j in range(segs):
                theta = 2*math.pi*j/segs
                x = cx + r*math.sin(phi)*math.cos(theta)
                y = cy + r*math.cos(phi)
                z = cz + r*math.sin(phi)*math.sin(theta)
                vertices.append(self._add_v(x, y, z))
        for i in range(rings):
            for j in range(segs):
                a = i*segs + j
                b = i*segs + (j+1)%segs
                c = (i+1)*segs + j
                d = (i+1)*segs + (j+1)%segs
                self.faces += [(a, b, d), (a, d, c)]

    def add_plane(self, cx, cy, cz, w, d):
        hw, hd = w/2, d/2
        v = [self._add_v(cx-hw, cy, cz-hd), self._add_v(cx+hw, cy, cz-hd),
             self._add_v(cx+hw, cy, cz+hd), self._add_v(cx-hw, cy, cz+hd)]
        self.faces += [(v[0], v[1], v[2]), (v[0], v[2], v[3])]

    def add_prism(self, cx, cy, cz, w, h, d):
        hw, hh, hd = w/2, h/2, d/2
        bl = self._add_v(cx-hw, cy-hh, cz-hd); br = self._add_v(cx+hw, cy-hh, cz-hd)
        fl = self._add_v(cx-hw, cy-hh, cz+hd); fr = self._add_v(cx+hw, cy-hh, cz+hd)
        tl = self._add_v(cx-hw, cy+hh, cz); tr = self._add_v(cx+hw, cy+hh, cz)
        self.faces += [(bl,br,fr),(bl,fr,fl),(bl,br,tr),(bl,tr,tl),
                       (fl,tr,fr),(fl,tl,tr),(bl,tl,fl),(br,fr,tr)]

    def scale(self, factor):
        self.verts = [(x*factor, y*factor, z*factor) for x, y, z in self.verts]

    def _compute_normals(self):
        normals = [[0.0, 0.0, 0.0] for _ in range(len(self.verts))]
        for face in self.faces:
            i0, i1, i2 = face
            v0, v1, v2 = self.verts[i0], self.verts[i1], self.verts[i2]
            e1 = (v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2])
            e2 = (v2[0]-v0[0], v2[1]-v0[1], v2[2]-v0[2])
            nx = e1[1]*e2[2] - e1[2]*e2[1]
            ny = e1[2]*e2[0] - e1[0]*e2[2]
            nz = e1[0]*e2[1] - e1[1]*e2[0]
            for idx in (i0, i1, i2):
                normals[idx][0] += nx; normals[idx][1] += ny; normals[idx][2] += nz
        result = []
        for nx, ny, nz in normals:
            length = math.sqrt(nx*nx + ny*ny + nz*nz)
            if length > 1e-8:
                result.append((nx/length, ny/length, nz/length))
            else:
                result.append((0.0, 1.0, 0.0))
        return result

    def write(self, path):
        normals = self._compute_normals()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"# {self.name}.obj - generated by survival_model_gen\n")
            f.write(f"# vertices: {len(self.verts)} faces: {len(self.faces)}\n")
            f.write("mtllib survival.mtl\n")
            f.write(f"usemtl {self.name}\n")
            for x, y, z in self.verts:
                f.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")
            for nx, ny, nz in normals:
                f.write(f"vn {nx:.4f} {ny:.4f} {nz:.4f}\n")
            for face in self.faces:
                f.write("f " + " ".join(f"{i+1}//{i+1}" for i in face) + "\n")
        return len(self.verts), len(self.faces)


# ============================================================
# 资源物品模型 (18个)
# ============================================================
def m_wood():
    o = ObjBuilder("wood")
    o.add_cylinder(0, 0.4, 0, 0.15, 0.8, 16)
    o.add_cylinder(0, 0.4, 0, 0.12, 0.82, 16)
    return o

def m_resin():
    o = ObjBuilder("resin")
    o.add_sphere(0, 0.2, 0, 0.18, 8, 12)
    o.add_cone(0, 0.05, 0, 0.1, 0.12, 12)
    return o

def m_rare_branch():
    o = ObjBuilder("rare_branch")
    o.add_cylinder(0, 0.25, 0, 0.05, 0.6, 12)
    o.add_cylinder(0.1, 0.4, 0, 0.035, 0.3, 10)
    o.add_cylinder(-0.08, 0.35, 0.06, 0.03, 0.25, 10)
    o.add_sphere(0.1, 0.58, 0, 0.05, 6, 8)
    o.add_sphere(-0.08, 0.5, 0.06, 0.04, 6, 8)
    return o

def m_stone():
    o = ObjBuilder("stone")
    o.add_box(0, 0.18, 0, 0.45, 0.36, 0.4)
    o.add_box(0.12, 0.28, -0.06, 0.18, 0.18, 0.18)
    o.add_box(-0.1, 0.12, 0.1, 0.12, 0.12, 0.12)
    return o

def m_iron_ore():
    o = ObjBuilder("iron_ore")
    o.add_box(0, 0.18, 0, 0.45, 0.36, 0.4)
    o.add_box(0.1, 0.22, 0.06, 0.12, 0.12, 0.12)
    o.add_box(-0.08, 0.28, -0.1, 0.1, 0.1, 0.1)
    o.add_box(0.05, 0.1, -0.08, 0.08, 0.08, 0.08)
    return o

def m_iron():
    o = ObjBuilder("iron")
    o.add_box(0, 0.1, 0, 0.45, 0.2, 0.25)
    o.add_box(0, 0.2, 0, 0.4, 0.05, 0.2)
    o.add_box(-0.15, 0.05, 0, 0.1, 0.08, 0.2)
    return o

def m_crystal():
    o = ObjBuilder("crystal")
    o.add_cone(0, 0.25, 0, 0.14, 0.5, 8)
    o.add_cone(0.12, 0.15, 0.06, 0.07, 0.25, 6)
    o.add_cone(-0.1, 0.12, -0.04, 0.06, 0.22, 6)
    o.add_cone(0.05, 0.1, -0.1, 0.05, 0.18, 5)
    return o

def m_meat():
    o = ObjBuilder("meat")
    o.add_box(0, 0.1, 0, 0.35, 0.2, 0.25)
    o.add_cylinder(0.22, 0.1, 0, 0.05, 0.22, 12)
    o.add_sphere(0.22, 0.1, 0.12, 0.06, 6, 8)
    return o

def m_cooked_meat():
    o = ObjBuilder("cooked_meat")
    o.add_box(0, 0.1, 0, 0.35, 0.2, 0.25)
    o.add_cylinder(0.22, 0.1, 0, 0.05, 0.22, 12)
    o.add_box(0, 0.2, 0, 0.3, 0.04, 0.2)
    return o

def m_hide():
    o = ObjBuilder("hide")
    o.add_plane(0, 0.02, 0, 0.55, 0.45)
    o.add_box(0, 0.04, 0, 0.5, 0.05, 0.4)
    return o

def m_bone():
    o = ObjBuilder("bone")
    o.add_cylinder(0, 0.06, 0, 0.05, 0.45, 12)
    o.add_sphere(-0.22, 0.06, 0, 0.08, 8, 10)
    o.add_sphere(0.22, 0.06, 0, 0.08, 8, 10)
    return o

def m_berry():
    o = ObjBuilder("berry")
    o.add_sphere(-0.07, 0.1, 0, 0.07, 8, 10)
    o.add_sphere(0.07, 0.1, 0.03, 0.07, 8, 10)
    o.add_sphere(0, 0.14, -0.05, 0.06, 8, 10)
    o.add_cylinder(0, 0.02, 0, 0.025, 0.05, 8)
    return o

def m_herb():
    o = ObjBuilder("herb")
    o.add_cylinder(-0.06, 0.12, 0, 0.02, 0.24, 8)
    o.add_cylinder(0.06, 0.14, 0.03, 0.02, 0.28, 8)
    o.add_cylinder(0, 0.1, -0.04, 0.018, 0.2, 8)
    o.add_sphere(-0.06, 0.26, 0, 0.04, 6, 8)
    o.add_sphere(0.06, 0.3, 0.03, 0.04, 6, 8)
    o.add_sphere(0, 0.22, -0.04, 0.035, 6, 8)
    return o

def m_seed():
    o = ObjBuilder("seed")
    o.add_sphere(-0.05, 0.05, 0, 0.05, 6, 8)
    o.add_sphere(0.05, 0.05, 0.03, 0.05, 6, 8)
    o.add_sphere(0, 0.06, -0.04, 0.045, 6, 8)
    return o

def m_potion():
    o = ObjBuilder("potion")
    o.add_cylinder(0, 0.06, 0, 0.05, 0.12, 12)
    o.add_cylinder(0, 0.22, 0, 0.1, 0.2, 16)
    o.add_cylinder(0, 0.36, 0, 0.04, 0.1, 10)
    o.add_cylinder(0, 0.44, 0, 0.05, 0.06, 10)
    return o

def m_recipe_scroll():
    o = ObjBuilder("recipe_scroll")
    o.add_cylinder(0, 0.06, 0, 0.06, 0.35, 16)
    o.add_box(0, 0.06, 0, 0.18, 0.1, 0.3)
    return o

def m_codex():
    o = ObjBuilder("codex")
    o.add_box(0, 0.1, 0, 0.35, 0.2, 0.25)
    o.add_box(0, 0.2, 0, 0.32, 0.03, 0.22)
    o.add_box(0, 0.1, 0.13, 0.3, 0.18, 0.02)
    return o

def m_clue_map():
    o = ObjBuilder("clue_map")
    o.add_plane(0, 0.02, 0, 0.45, 0.35)
    o.add_box(-0.2, 0.05, 0, 0.05, 0.1, 0.35)
    o.add_box(0.2, 0.05, 0, 0.05, 0.1, 0.35)
    return o


# ============================================================
# 建筑模型 (26个)
# ============================================================
def m_foundation():
    o = ObjBuilder("foundation")
    o.add_box(0, 0.12, 0, 2.2, 0.24, 2.2)
    o.add_box(0, 0.25, 0, 2, 0.05, 2)
    return o

def m_wall():
    o = ObjBuilder("wall")
    o.add_box(0, 1, 0, 2, 2, 0.35)
    o.add_box(0, 1.95, 0, 2.05, 0.1, 0.4)
    return o

def m_roof():
    o = ObjBuilder("roof")
    o.add_prism(0, 0.55, 0, 2.4, 1.1, 2.4)
    return o

def m_door():
    o = ObjBuilder("door")
    o.add_box(0, 1, 0, 1, 2, 0.18)
    o.add_box(0.35, 1, 0.1, 0.07, 0.12, 0.07)
    o.add_box(0, 2.08, 0, 1.1, 0.12, 0.22)
    o.add_box(-0.45, 1, 0, 0.1, 2, 0.2)
    o.add_box(0.45, 1, 0, 0.1, 2, 0.2)
    return o

def m_window():
    o = ObjBuilder("window")
    o.add_box(0, 0.85, 0, 1.1, 1.3, 0.12)
    o.add_box(0, 0.85, 0.03, 0.9, 1.1, 0.05)
    o.add_box(0, 0.85, 0.04, 0.05, 1.1, 0.06)
    o.add_box(0, 0.85, 0.04, 0.9, 0.05, 0.06)
    return o

def m_stairs():
    o = ObjBuilder("stairs")
    for i in range(6):
        o.add_box(0, 0.1+i*0.18, (2.4-i*0.4)-0.2, 1.4, 0.18, 0.4)
    return o

def m_furniture():
    o = ObjBuilder("furniture")
    o.add_box(0, 0.45, 0, 1.2, 0.1, 0.7)
    for x, z in [(-0.5,-0.25),(0.5,-0.25),(-0.5,0.25),(0.5,0.25)]:
        o.add_box(x, 0.22, z, 0.1, 0.45, 0.1)
    o.add_box(-0.2, 0.55, 0, 0.15, 0.12, 0.1)
    o.add_box(0, 0.28, 0.8, 0.5, 0.08, 0.5)
    o.add_box(0, 0.6, 0.95, 0.5, 0.55, 0.08)
    for x, z in [(-0.18,0.6),(0.18,0.6),(-0.18,0.95),(0.18,0.95)]:
        o.add_box(x, 0.14, z, 0.06, 0.28, 0.06)
    return o

def m_torch():
    o = ObjBuilder("torch")
    o.add_cylinder(0, 0.5, 0, 0.05, 1.1, 12)
    o.add_cone(0, 1.15, 0, 0.12, 0.3, 12)
    o.add_cone(0, 1.2, 0, 0.07, 0.2, 10)
    return o

def m_road():
    o = ObjBuilder("road")
    o.add_plane(0, 0.02, 0, 2.2, 2.2)
    for i in range(-1, 2):
        for j in range(-1, 2):
            o.add_box(i*0.65, 0.05, j*0.65, 0.55, 0.06, 0.55)
    return o

def m_flower_pot():
    o = ObjBuilder("flower_pot")
    o.add_cylinder(0, 0.22, 0, 0.22, 0.44, 16)
    o.add_cylinder(0, 0.48, 0, 0.25, 0.1, 16)
    o.add_cylinder(-0.06, 0.7, 0, 0.018, 0.35, 8)
    o.add_cylinder(0.06, 0.65, 0.04, 0.018, 0.3, 8)
    o.add_sphere(-0.06, 0.9, 0, 0.07, 8, 10)
    o.add_sphere(0.06, 0.82, 0.04, 0.06, 8, 10)
    return o

def m_crate():
    o = ObjBuilder("crate")
    o.add_box(0, 0.45, 0, 0.9, 0.9, 0.9)
    o.add_box(0, 0.45, 0.46, 0.8, 0.8, 0.03)
    return o

def m_workbench():
    o = ObjBuilder("workbench")
    o.add_box(0, 0.5, 0, 1.4, 0.12, 0.8)
    for x, z in [(-0.6,-0.3),(0.6,-0.3),(-0.6,0.3),(0.6,0.3)]:
        o.add_box(x, 0.25, z, 0.12, 0.5, 0.12)
    o.add_box(-0.35, 0.6, 0, 0.25, 0.12, 0.18)
    o.add_box(0.25, 0.6, 0.12, 0.18, 0.1, 0.12)
    o.add_cylinder(0.4, 0.58, -0.15, 0.04, 0.15, 8)
    return o

def m_furnace():
    o = ObjBuilder("furnace")
    o.add_box(0, 0.65, 0, 1.1, 1.3, 0.9)
    o.add_box(0, 0.45, 0.46, 0.55, 0.45, 0.04)
    o.add_cylinder(0.35, 1.4, -0.25, 0.14, 0.55, 12)
    o.add_box(0, 1.32, 0, 1.15, 0.08, 0.95)
    return o

def m_kitchen():
    o = ObjBuilder("kitchen")
    o.add_box(0, 0.45, 0, 1.4, 0.9, 0.7)
    o.add_cylinder(-0.3, 0.95, 0, 0.14, 0.06, 12)
    o.add_cylinder(0.3, 0.95, 0, 0.14, 0.06, 12)
    o.add_cylinder(0, 1.1, 0.18, 0.18, 0.25, 16)
    o.add_box(0, 0.92, 0, 1.3, 0.05, 0.6)
    return o

def m_grinder():
    o = ObjBuilder("grinder")
    o.add_box(0, 0.35, 0, 0.9, 0.7, 0.7)
    o.add_cylinder(0, 0.8, 0, 0.3, 0.35, 16)
    o.add_cylinder(0, 1.0, 0, 0.06, 0.35, 10)
    o.add_box(0, 0.72, 0, 0.7, 0.05, 0.6)
    return o

def m_shop():
    o = ObjBuilder("shop")
    o.add_box(0, 0.55, 0, 1.7, 1.1, 0.9)
    o.add_prism(0, 1.3, 0, 1.9, 0.45, 1.1)
    o.add_box(0, 0.65, 0.46, 1.3, 0.35, 0.04)
    o.add_box(0, 1.1, 0, 1.5, 0.06, 0.8)
    return o

def m_order_board():
    o = ObjBuilder("order_board")
    o.add_box(0, 1.05, 0, 1.1, 1.6, 0.12)
    o.add_box(-0.45, 0.35, 0, 0.12, 0.7, 0.12)
    o.add_box(0.45, 0.35, 0, 0.12, 0.7, 0.12)
    o.add_box(0, 1.15, 0.07, 0.7, 0.5, 0.03)
    return o

def m_display_case():
    o = ObjBuilder("display_case")
    o.add_box(0, 0.55, 0, 1.4, 1.1, 0.6)
    o.add_box(0, 1.2, 0, 1.2, 0.25, 0.5)
    o.add_box(0, 0.75, 0.31, 1.3, 0.5, 0.03)
    o.add_box(0, 0.55, 0, 1.3, 0.05, 0.55)
    return o

def m_defense_wall():
    o = ObjBuilder("defense_wall")
    o.add_box(0, 1.05, 0, 2.2, 2.1, 0.45)
    for i in range(-1, 2):
        o.add_cone(i*0.65, 2.3, 0, 0.17, 0.45, 8)
    o.add_box(0, 2.05, 0, 2.25, 0.1, 0.5)
    return o

def m_trap():
    o = ObjBuilder("trap")
    o.add_box(0, 0.06, 0, 1.1, 0.12, 1.1)
    for i in range(-1, 2):
        for j in range(-1, 2):
            o.add_cone(i*0.32, 0.22, j*0.32, 0.07, 0.32, 8)
    return o

def m_turret():
    o = ObjBuilder("turret")
    o.add_cylinder(0, 0.35, 0, 0.45, 0.7, 16)
    o.add_box(0, 0.78, 0, 0.6, 0.35, 0.6)
    o.add_cylinder(0.35, 0.82, 0, 0.1, 0.7, 16)
    o.add_cylinder(0, 0.78, 0, 0.15, 0.2, 12)
    return o

def m_farm_plot():
    o = ObjBuilder("farm_plot")
    o.add_box(0, 0.12, 0, 2.2, 0.24, 1.7)
    for i in range(-2, 3):
        o.add_box(i*0.38, 0.26, 0, 0.28, 0.05, 1.5)
    return o

def m_greenhouse():
    o = ObjBuilder("greenhouse")
    o.add_box(0, 0.55, 0, 2.2, 1.1, 1.7)
    o.add_prism(0, 1.3, 0, 2.4, 0.45, 1.9)
    o.add_box(0, 0.55, 0.86, 2, 1, 0.03)
    return o

def m_animal_pen():
    o = ObjBuilder("animal_pen")
    o.add_box(0, 0.85, -0.35, 1.7, 1.7, 0.9)
    o.add_prism(0, 1.9, -0.35, 1.9, 0.45, 1.1)
    o.add_box(0, 0.6, -0.35, 0.5, 0.8, 0.05)
    for x in [-1.0, 1.0]:
        for z in [0.2, 0.65, 1.1]:
            o.add_cylinder(x, 0.35, z, 0.05, 0.7, 10)
    o.add_box(0, 0.45, 0.2, 2.0, 0.07, 0.07)
    o.add_box(0, 0.25, 0.2, 2.0, 0.07, 0.07)
    return o

def m_water_trough():
    o = ObjBuilder("water_trough")
    o.add_box(0, 0.22, 0, 1.4, 0.44, 0.6)
    o.add_box(0, 0.38, 0, 1.2, 0.12, 0.42)
    o.add_plane(0, 0.42, 0, 1.1, 0.35)
    return o

def m_fence():
    o = ObjBuilder("fence")
    for x in [-0.65, 0, 0.65]:
        o.add_cylinder(x, 0.45, 0, 0.06, 0.9, 12)
        o.add_cone(x, 0.92, 0, 0.07, 0.12, 10)
    o.add_box(0, 0.55, 0, 1.5, 0.07, 0.07)
    o.add_box(0, 0.3, 0, 1.5, 0.07, 0.07)
    return o


# ============================================================
# 主程序
# ============================================================
MODELS = [
    ("wood", m_wood), ("resin", m_resin), ("rare_branch", m_rare_branch),
    ("stone", m_stone), ("iron_ore", m_iron_ore), ("iron", m_iron),
    ("crystal", m_crystal), ("meat", m_meat), ("cooked_meat", m_cooked_meat),
    ("hide", m_hide), ("bone", m_bone), ("berry", m_berry),
    ("herb", m_herb), ("seed", m_seed), ("potion", m_potion),
    ("recipe_scroll", m_recipe_scroll), ("codex", m_codex), ("clue_map", m_clue_map),
    ("foundation", m_foundation), ("wall", m_wall), ("roof", m_roof),
    ("door", m_door), ("window", m_window), ("stairs", m_stairs),
    ("furniture", m_furniture), ("torch", m_torch), ("road", m_road),
    ("flower_pot", m_flower_pot), ("crate", m_crate),
    ("workbench", m_workbench), ("furnace", m_furnace), ("kitchen", m_kitchen),
    ("grinder", m_grinder), ("shop", m_shop), ("order_board", m_order_board),
    ("display_case", m_display_case),
    ("defense_wall", m_defense_wall), ("trap", m_trap), ("turret", m_turret),
    ("farm_plot", m_farm_plot), ("greenhouse", m_greenhouse),
    ("animal_pen", m_animal_pen), ("water_trough", m_water_trough), ("fence", m_fence),
]


def _write_mtl(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# survival.mtl - generated by survival_model_gen\n")
        for name, (r, g, b) in MODEL_COLORS.items():
            tex = MODEL_TEX.get(name, "stone")
            f.write(f"\nnewmtl {name}\n")
            f.write(f"Ka {r*0.3:.4f} {g*0.3:.4f} {b*0.3:.4f}\n")
            f.write(f"Kd {r:.4f} {g:.4f} {b:.4f}\n")
            f.write(f"Ks 0.1500 0.1500 0.1500\n")
            f.write(f"map_Kd {tex}.png\n")
            f.write("d 1.0000\n")
            f.write("illum 2\n")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("生成纹理贴图...")
    for tex_name, gen_func in TEXTURE_GENS.items():
        tex_path = os.path.join(OUTPUT_DIR, f"{tex_name}.png")
        gen_func(tex_path)
        print(f"  {tex_name}.png")
    _write_mtl(os.path.join(OUTPUT_DIR, "survival.mtl"))
    print("\n生成模型...")
    total_v = total_f = 0
    for idx, (name, func) in enumerate(MODELS):
        builder = func()
        factor = 8 if idx < 18 else 2
        builder.scale(factor)
        path = os.path.join(OUTPUT_DIR, f"{name}.obj")
        v, f = builder.write(path)
        total_v += v
        total_f += f
        print(f"  {name:20s}  x{factor}  v={v:4d}  f={f:4d}")
    print(f"\n完成：{len(MODELS)}模型 + {len(TEXTURE_GENS)}纹理 + 1材质")
    print(f"输出目录：{OUTPUT_DIR}")


if __name__ == "__main__":
    main()
