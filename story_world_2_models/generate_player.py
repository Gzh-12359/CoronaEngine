#!/usr/bin/env python3
"""
Minecraft Player Model (Steve-style) Generator
生成 Minecraft 玩家风格的 OBJ 模型 + 64x64 皮肤纹理 + MTL，可直接导入引擎
"""
import os
from PIL import Image, ImageDraw

OUT_DIR = r"C:\Users\guo\Documents\12\story_world_2_models\import_ready"
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================================
# 1. 生成 64x64 Steve 风格皮肤纹理
# ============================================================================

def generate_skin():
    """生成经典 Steve 风格 64x64 皮肤"""
    SKIN = (184, 136, 106, 255)      # 肤色
    SKIN_DARK = (160, 115, 90, 255)  # 阴影肤色
    HAIR = (58, 42, 26, 255)          # 深棕头发
    HAIR_LIGHT = (78, 58, 38, 255)   # 浅棕头发
    SHIRT = (0, 175, 175, 255)        # 青色衬衫 (Steve经典)
    SHIRT_DARK = (0, 140, 140, 255)   # 衬衫阴影
    PANTS = (59, 59, 159, 255)        # 蓝色裤子
    PANTS_DARK = (45, 45, 120, 255)   # 裤子阴影
    SHOE = (74, 53, 32, 255)          # 棕色鞋子
    EYE_WHITE = (255, 255, 255, 255)
    EYE_BLUE = (46, 117, 153, 255)
    MOUTH = (114, 62, 52, 255)

    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    def fill_rect(x, y, w, h, color):
        draw.rectangle([x, y, x+w-1, y+h-1], fill=color)

    def shade_rect(x, y, w, h, base, shade, shade_height=2):
        fill_rect(x, y, w, h, base)
        fill_rect(x, y, w, shade_height, shade)

    # === 头部 ===
    # 顶面 (8,0) 8x8 - 头发
    fill_rect(8, 0, 8, 8, HAIR)
    fill_rect(8, 0, 8, 2, HAIR_LIGHT)
    # 底面 (16,0) 8x8 - 肤色(下巴底)
    fill_rect(16, 0, 8, 8, SKIN_DARK)
    # 右面 (0,8) 8x8 - 头发+耳朵
    fill_rect(0, 8, 8, 3, HAIR)
    fill_rect(0, 11, 8, 5, SKIN)
    fill_rect(0, 11, 2, 2, SKIN_DARK)  # 耳朵阴影
    # 正面/脸 (8,8) 8x8
    fill_rect(8, 8, 8, 2, HAIR)         # 头发刘海
    fill_rect(8, 10, 8, 6, SKIN)        # 脸
    # 眼睛
    fill_rect(9, 11, 2, 2, EYE_WHITE)
    fill_rect(10, 11, 1, 2, EYE_BLUE)
    fill_rect(13, 11, 2, 2, EYE_WHITE)
    fill_rect(14, 11, 1, 2, EYE_BLUE)
    # 鼻子
    fill_rect(11, 12, 2, 2, SKIN_DARK)
    # 嘴
    fill_rect(10, 14, 4, 1, MOUTH)
    # 左面 (16,8) 8x8 - 头发+耳朵
    fill_rect(16, 8, 8, 3, HAIR)
    fill_rect(16, 11, 8, 5, SKIN)
    fill_rect(22, 11, 2, 2, SKIN_DARK)
    # 后面 (24,8) 8x8 - 头发
    fill_rect(24, 8, 8, 8, HAIR)
    fill_rect(24, 8, 8, 2, HAIR_LIGHT)

    # === 身体 ===
    # 顶面 (20,16) 8x4 - 衬衫领口
    fill_rect(20, 16, 8, 4, SHIRT)
    fill_rect(22, 16, 4, 2, SKIN)  # 领口
    # 底面 (28,16) 8x4
    fill_rect(28, 16, 8, 4, SHIRT_DARK)
    # 右面 (16,20) 4x12 - 衬衫袖窿
    shade_rect(16, 20, 4, 12, SHIRT, SHIRT_DARK, 2)
    # 正面 (20,20) 8x12 - 衬衫
    shade_rect(20, 20, 8, 12, SHIRT, SHIRT_DARK, 2)
    fill_rect(22, 20, 4, 2, SKIN)  # 领口
    # 左面 (28,20) 4x12
    shade_rect(28, 20, 4, 12, SHIRT, SHIRT_DARK, 2)
    # 后面 (32,20) 8x12
    shade_rect(32, 20, 8, 12, SHIRT, SHIRT_DARK, 2)

    # === 右臂 ===
    # 顶面 (44,16) 4x4
    fill_rect(44, 16, 4, 4, SHIRT_DARK)
    # 底面 (48,16) 4x4 - 手
    fill_rect(48, 16, 4, 4, SKIN_DARK)
    # 右面/外侧 (40,20) 4x12
    shade_rect(40, 20, 4, 10, SHIRT, SHIRT_DARK, 2)
    fill_rect(40, 30, 4, 2, SKIN)  # 手
    # 正面 (44,20) 4x12
    shade_rect(44, 20, 4, 10, SHIRT, SHIRT_DARK, 2)
    fill_rect(44, 30, 4, 2, SKIN)
    # 左面/内侧 (48,20) 4x12
    shade_rect(48, 20, 4, 10, SHIRT, SHIRT_DARK, 2)
    fill_rect(48, 30, 4, 2, SKIN)
    # 后面 (52,20) 4x12
    shade_rect(52, 20, 4, 10, SHIRT, SHIRT_DARK, 2)
    fill_rect(52, 30, 4, 2, SKIN)

    # === 左臂 ===
    # 顶面 (36,48) 4x4
    fill_rect(36, 48, 4, 4, SHIRT_DARK)
    # 底面 (40,48) 4x4
    fill_rect(40, 48, 4, 4, SKIN_DARK)
    # 右面/内侧 (32,52) 4x12
    shade_rect(32, 52, 4, 10, SHIRT, SHIRT_DARK, 2)
    fill_rect(32, 62, 4, 2, SKIN)
    # 正面 (36,52) 4x12
    shade_rect(36, 52, 4, 10, SHIRT, SHIRT_DARK, 2)
    fill_rect(36, 62, 4, 2, SKIN)
    # 左面/外侧 (40,52) 4x12
    shade_rect(40, 52, 4, 10, SHIRT, SHIRT_DARK, 2)
    fill_rect(40, 62, 4, 2, SKIN)
    # 后面 (44,52) 4x12
    shade_rect(44, 52, 4, 10, SHIRT, SHIRT_DARK, 2)
    fill_rect(44, 62, 4, 2, SKIN)

    # === 右腿 ===
    # 顶面 (4,16) 4x4
    fill_rect(4, 16, 4, 4, PANTS_DARK)
    # 底面 (8,16) 4x4 - 鞋底
    fill_rect(8, 16, 4, 4, SHOE)
    # 右面/外侧 (0,20) 4x12
    shade_rect(0, 20, 4, 10, PANTS, PANTS_DARK, 2)
    fill_rect(0, 30, 4, 2, SHOE)  # 鞋
    # 正面 (4,20) 4x12
    shade_rect(4, 20, 4, 10, PANTS, PANTS_DARK, 2)
    fill_rect(4, 30, 4, 2, SHOE)
    # 左面/内侧 (8,20) 4x12
    shade_rect(8, 20, 4, 10, PANTS, PANTS_DARK, 2)
    fill_rect(8, 30, 4, 2, SHOE)
    # 后面 (12,20) 4x12
    shade_rect(12, 20, 4, 10, PANTS, PANTS_DARK, 2)
    fill_rect(12, 30, 4, 2, SHOE)

    # === 左腿 ===
    # 顶面 (20,48) 4x4
    fill_rect(20, 48, 4, 4, PANTS_DARK)
    # 底面 (24,48) 4x4
    fill_rect(24, 48, 4, 4, SHOE)
    # 右面/内侧 (16,52) 4x12
    shade_rect(16, 52, 4, 10, PANTS, PANTS_DARK, 2)
    fill_rect(16, 62, 4, 2, SHOE)
    # 正面 (20,52) 4x12
    shade_rect(20, 52, 4, 10, PANTS, PANTS_DARK, 2)
    fill_rect(20, 62, 4, 2, SHOE)
    # 左面/外侧 (24,52) 4x12
    shade_rect(24, 52, 4, 10, PANTS, PANTS_DARK, 2)
    fill_rect(24, 62, 4, 2, SHOE)
    # 后面 (28,52) 4x12
    shade_rect(28, 52, 4, 10, PANTS, PANTS_DARK, 2)
    fill_rect(28, 62, 4, 2, SHOE)

    skin_path = os.path.join(OUT_DIR, "player_skin.png")
    img.save(skin_path)
    print(f"Skin saved: {skin_path}")
    return skin_path

# ============================================================================
# 2. 生成玩家 OBJ 模型
# ============================================================================

# 每个身体部位：from, to, 以及6个面在皮肤纹理中的像素矩形(px,py,pw,ph)
# 面顺序：down, up, north, south, west, east
BODY_PARTS = {
    "head": {
        "from": (-4, 24, -4), "to": (4, 32, 4),
        "faces": {
            "down":  (16, 0, 8, 8),
            "up":    (8, 0, 8, 8),
            "north": (8, 8, 8, 8),   # 脸
            "south": (24, 8, 8, 8),  # 后脑
            "west":  (0, 8, 8, 8),   # 右脸
            "east":  (16, 8, 8, 8),  # 左脸
        }
    },
    "body": {
        "from": (-4, 12, -2), "to": (4, 24, 2),
        "faces": {
            "down":  (28, 16, 8, 4),
            "up":    (20, 16, 8, 4),
            "north": (20, 20, 8, 12),  # 衬衫正面
            "south": (32, 20, 8, 12),
            "west":  (16, 20, 4, 12),
            "east":  (28, 20, 4, 12),
        }
    },
    "right_arm": {
        "from": (-8, 12, -2), "to": (-4, 24, 2),
        "faces": {
            "down":  (48, 16, 4, 4),
            "up":    (44, 16, 4, 4),
            "north": (44, 20, 4, 12),
            "south": (52, 20, 4, 12),
            "west":  (40, 20, 4, 12),  # 外侧
            "east":  (48, 20, 4, 12),  # 内侧
        }
    },
    "left_arm": {
        "from": (4, 12, -2), "to": (8, 24, 2),
        "faces": {
            "down":  (40, 48, 4, 4),
            "up":    (36, 48, 4, 4),
            "north": (36, 52, 4, 12),
            "south": (44, 52, 4, 12),
            "west":  (32, 52, 4, 12),  # 内侧
            "east":  (40, 52, 4, 12),  # 外侧
        }
    },
    "right_leg": {
        "from": (-4, 0, -2), "to": (0, 12, 2),
        "faces": {
            "down":  (8, 16, 4, 4),
            "up":    (4, 16, 4, 4),
            "north": (4, 20, 4, 12),
            "south": (12, 20, 4, 12),
            "west":  (0, 20, 4, 12),   # 外侧
            "east":  (8, 20, 4, 12),   # 内侧
        }
    },
    "left_leg": {
        "from": (0, 0, -2), "to": (4, 12, 2),
        "faces": {
            "down":  (24, 48, 4, 4),
            "up":    (20, 48, 4, 4),
            "north": (20, 52, 4, 12),
            "south": (28, 52, 4, 12),
            "west":  (16, 52, 4, 12),  # 内侧
            "east":  (24, 52, 4, 12),  # 外侧
        }
    },
}

# 立方体8顶点索引：0=fxfyfz,1=txfyfz,2=txfytz,3=fxfytz,4=fxtyfz,5=txtyfz,6=txtytz,7=fxtytz
FACE_VERTS = {
    "down":  [0, 2, 1, 0, 3, 2],
    "up":    [4, 5, 6, 4, 6, 7],
    "north": [0, 1, 5, 0, 5, 4],
    "south": [3, 7, 6, 3, 6, 2],
    "west":  [0, 4, 7, 0, 7, 3],
    "east":  [1, 2, 6, 1, 6, 5],
}
FACE_NORMALS = {
    "down": (0, -1, 0), "up": (0, 1, 0),
    "north": (0, 0, -1), "south": (0, 0, 1),
    "west": (-1, 0, 0), "east": (1, 0, 0),
}

def pixel_to_uv(px, py, pw, ph):
    """像素矩形 -> 每个面6个顶点的UV坐标列表，V轴翻转"""
    u0, u1 = px / 64.0, (px + pw) / 64.0
    v0, v1 = 1.0 - (py + ph) / 64.0, 1.0 - py / 64.0  # 翻转
    # 4角：nw, ne, se, sw
    corners = {"nw": (u0, v1), "ne": (u1, v1), "se": (u1, v0), "sw": (u0, v0)}
    # 每个面6顶点对应的角（与FACE_VERTS对应）
    face_corner_map = {
        "down":  ["sw", "se", "ne", "sw", "nw", "ne"],
        "up":    ["nw", "ne", "se", "nw", "se", "sw"],
        "north": ["sw", "se", "ne", "sw", "ne", "nw"],
        "south": ["sw", "nw", "ne", "sw", "ne", "se"],
        "west":  ["se", "ne", "nw", "se", "nw", "sw"],
        "east":  ["sw", "se", "ne", "sw", "ne", "nw"],
    }
    # 转换为实际UV坐标
    return {face: [corners[c] for c in corner_list] for face, corner_list in face_corner_map.items()}

def generate_player_obj():
    obj_lines = []
    v_offset = 0
    vt_offset = 0
    vn_offset = 0

    obj_lines.append("# Minecraft Player Model (Steve-style)")
    obj_lines.append("# 6 body parts: head, body, right_arm, left_arm, right_leg, left_leg")
    obj_lines.append("mtllib player_model.mtl")
    obj_lines.append("")

    for part_name, part in BODY_PARTS.items():
        f = part["from"]
        t = part["to"]
        fx, fy, fz = f
        tx, ty, tz = t
        verts = [
            (fx, fy, fz), (tx, fy, fz), (tx, fy, tz), (fx, fy, tz),
            (fx, ty, fz), (tx, ty, fz), (tx, ty, tz), (fx, ty, tz),
        ]
        obj_lines.append(f"g {part_name}")

        for face_name in ["down", "up", "north", "south", "west", "east"]:
            if face_name not in part["faces"]:
                continue
            px, py, pw, ph = part["faces"][face_name]
            corner_map = pixel_to_uv(px, py, pw, ph)
            face_corners = corner_map[face_name]
            vert_indices = FACE_VERTS[face_name]
            normal = FACE_NORMALS[face_name]

            # 写入6个顶点
            for vi in vert_indices:
                v = verts[vi]
                obj_lines.append(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}")
            # 写入6个UV
            for corner in face_corners:
                u, v = corner
                obj_lines.append(f"vt {u:.4f} {v:.4f}")
            # 写入法线
            obj_lines.append(f"vn {normal[0]:.4f} {normal[1]:.4f} {normal[2]:.4f}")

            # 写入面（2个三角形）
            obj_lines.append("usemtl mat_player_skin")
            tri1 = " ".join(f"{v_offset+i+1}/{vt_offset+i+1}/{vn_offset+1}" for i in range(3))
            tri2 = " ".join(f"{v_offset+i+1}/{vt_offset+i+1}/{vn_offset+1}" for i in range(3, 6))
            obj_lines.append(f"f {tri1}")
            obj_lines.append(f"f {tri2}")
            obj_lines.append("")

            v_offset += 6
            vt_offset += 6
            vn_offset += 1

    obj_path = os.path.join(OUT_DIR, "player_model.obj")
    with open(obj_path, "w", encoding="utf-8") as f:
        f.write("\n".join(obj_lines))
    print(f"OBJ saved: {obj_path}")

    # MTL
    mtl_lines = [
        "# Materials for Minecraft Player Model",
        "",
        "newmtl mat_player_skin",
        "Ka 1.0 1.0 1.0",
        "Kd 1.0 1.0 1.0",
        "Ks 0.0 0.0 0.0",
        "d 1.0",
        "map_Kd player_skin.png",
        "",
    ]
    mtl_path = os.path.join(OUT_DIR, "player_model.mtl")
    with open(mtl_path, "w", encoding="utf-8") as f:
        f.write("\n".join(mtl_lines))
    print(f"MTL saved: {mtl_path}")

    return obj_path, mtl_path

# ============================================================================
if __name__ == "__main__":
    generate_skin()
    generate_player_obj()
    print("\n=== Player model generation complete ===")
    print(f"Output directory: {OUT_DIR}")
    print("Files: player_model.obj, player_model.mtl, player_skin.png")
