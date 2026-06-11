# -*- coding: utf-8 -*-
"""
演示：WASD 移动，空格跳跃，鼠标移动转向（适用于 Blockly 生成的运行时环境）
放到 editor/plugins/ScratchTool/ 下，作为演示脚本运行。
"""
import time
from CoronaCore.utils import corona_engine_scratch as CoronaEngine


def run():
    # 可调参数
    move_speed = 200.0    # 单位: 引擎单位/秒
    rot_speed = 180.0     # A/D 键转向速度 (度/秒)
    mouse_sens = 0.15     # 像素 -> 度
    jump_speed = 6.0      # 跳跃初速度
    gravity = 18.0        # 重力加速度

    # 状态
    prev_mx = CoronaEngine.mouse_x()
    vertical_v = 0.0
    grounded = True
    ground_z = CoronaEngine.Z()

    last = time.time()
    try:
        while True:
            now = time.time()
            dt = min(0.05, now - last)
            last = now

            # 鼠标水平移动转向（yaw）
            mx = CoronaEngine.mouse_x()
            dx = mx - prev_mx
            prev_mx = mx
            if abs(dx) > 0.0001:
                CoronaEngine.rotateY(dx * mouse_sens)

            # 键盘控制：W/S 前后移动，A/D 原地转向
            if CoronaEngine.keyboard('KeyW'):
                CoronaEngine.move(move_speed * dt)
            if CoronaEngine.keyboard('KeyS'):
                CoronaEngine.move(-move_speed * dt)
            if CoronaEngine.keyboard('KeyA'):
                CoronaEngine.rotateY(rot_speed * dt)
            if CoronaEngine.keyboard('KeyD'):
                CoronaEngine.rotateY(-rot_speed * dt)

            # 跳跃
            if CoronaEngine.keyboard('Space') and grounded:
                vertical_v = jump_speed
                grounded = False

            # 简单垂直运动/碰地检查
            if not grounded:
                vertical_v -= gravity * dt
                CoronaEngine.Zadd(vertical_v * dt)
                if CoronaEngine.Z() <= ground_z:
                    CoronaEngine.Zset(ground_z)
                    vertical_v = 0.0
                    grounded = True

            # 协作式等待（使用运行时提供的 wait）
            try:
                CoronaEngine.wait(0.016)
            except Exception:
                # 若运行环境没有提供 wait，退回到 time.sleep
                time.sleep(0.016)
    except KeyboardInterrupt:
        # 在交互测试中允许 Ctrl+C 停止
        return


if __name__ == '__main__':
    run()
