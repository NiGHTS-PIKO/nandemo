import tkinter as tk
import math

def draw_polygon():
    canvas.delete("all")
    try:
        n = int(entry.get())
        if n < 3:
            label_result.config(text="角の数は3以上にしてください")
            return
        
        # 計算部分
        triangles = n - 2
        angle_sum = 180 * triangles
        one_angle = angle_sum / n

        # 解説表示
        explanation = (f"{n}角形は三角形{triangles}個に分割できます。\n"
                       f"内角の和：{angle_sum:.2f}°\n"
                       f"正{n}角形なら1つの内角：{one_angle:.2f}°")
        label_result.config(text=explanation)

        # 描画部分
        radius = 100
        center_x, center_y = 150, 150
        points = []

        for i in range(n):
            angle = 2 * math.pi * i / n
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))

        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            canvas.create_line(x1, y1, x2, y2, fill="black")

    except:
        label_result.config(text="整数を入力してください")

# GUI構成
root = tk.Tk()
root.title("多角形詠唱GUI：図形×角度×思想ログ")

entry = tk.Entry(root)
entry.pack()

btn = tk.Button(root, text="詠唱する", command=draw_polygon)
btn.pack()

canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack()

label_result = tk.Label(root, text="", justify="left")
label_result.pack()

root.mainloop()
