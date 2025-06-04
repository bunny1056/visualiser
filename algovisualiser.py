# Algorithm Visualizer
# Data Structures & Algorithms (DSA) Visualizer using Python & Tkinter
# Visualizes: Binary Search, Ternary Search, Bubble Sort, Selection Sort, Merge Sort, Heap Sort

import tkinter as tk
from tkinter import ttk
import random
import time

# ----------------------------- Sorting Algorithms -----------------------------
def bubble_sort(data, draw, delay):
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                draw(data, ['red' if x == j or x == j+1 else 'blue' for x in range(len(data))])
                time.sleep(delay)

def selection_sort(data, draw, delay):
    for i in range(len(data)):
        min_idx = i
        for j in range(i+1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        draw(data, ['green' if x == i or x == min_idx else 'blue' for x in range(len(data))])
        time.sleep(delay)

def merge_sort(data, draw, delay):
    def merge_sort_helper(data, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_helper(data, left, mid)
            merge_sort_helper(data, mid+1, right)
            merge(data, left, mid, right)
            draw(data, ['purple' if x >= left and x <= right else 'blue' for x in range(len(data))])
            time.sleep(delay)

    def merge(data, left, mid, right):
        left_part = data[left:mid+1]
        right_part = data[mid+1:right+1]
        i = j = 0
        for k in range(left, right+1):
            if i < len(left_part) and (j >= len(right_part) or left_part[i] <= right_part[j]):
                data[k] = left_part[i]
                i += 1
            else:
                data[k] = right_part[j]
                j += 1

    merge_sort_helper(data, 0, len(data)-1)

def heap_sort(data, draw, delay):
    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and data[l] > data[largest]:
            largest = l
        if r < n and data[r] > data[largest]:
            largest = r

        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            draw(data, ['red' if x == i or x == largest else 'blue' for x in range(len(data))])
            time.sleep(delay)
            heapify(n, largest)

    n = len(data)
    for i in range(n//2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n-1, 0, -1):
        data[i], data[0] = data[0], data[i]
        draw(data, ['green' if x == i or x == 0 else 'blue' for x in range(len(data))])
        time.sleep(delay)
        heapify(i, 0)

# ----------------------------- Search Algorithms -----------------------------
def binary_search(data, draw, delay, target):
    l, r = 0, len(data) - 1
    while l <= r:
        m = (l + r) // 2
        draw(data, ['yellow' if x == m else 'blue' for x in range(len(data))])
        time.sleep(delay)
        if data[m] == target:
            draw(data, ['green' if x == m else 'blue' for x in range(len(data))])
            return m
        elif data[m] < target:
            l = m + 1
        else:
            r = m - 1
    return -1

def ternary_search(data, draw, delay, target):
    def helper(l, r):
        if r >= l:
            mid1 = l + (r - l) // 3
            mid2 = r - (r - l) // 3
            draw(data, ['yellow' if x == mid1 or x == mid2 else 'blue' for x in range(len(data))])
            time.sleep(delay)
            if data[mid1] == target:
                draw(data, ['green' if x == mid1 else 'blue' for x in range(len(data))])
                return mid1
            if data[mid2] == target:
                draw(data, ['green' if x == mid2 else 'blue' for x in range(len(data))])
                return mid2
            if target < data[mid1]:
                return helper(l, mid1 - 1)
            elif target > data[mid2]:
                return helper(mid2 + 1, r)
            else:
                return helper(mid1 + 1, mid2 - 1)
        return -1
    return helper(0, len(data)-1)

# ----------------------------- UI Setup -----------------------------
def draw_data(canvas, data, color_array):
    canvas.delete("all")
    c_height = 400
    c_width = 800
    x_width = c_width / len(data)
    scaling = max(data)
    for i, val in enumerate(data):
        x0 = i * x_width
        y0 = c_height - (val / scaling * 350)
        x1 = (i + 1) * x_width
        y1 = c_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
    canvas.update()

def start_algorithm():
    global data
    if not data: return
    algorithm = algo_menu.get()
    speed = speed_scale.get()
    target = int(entry.get()) if entry.get().isdigit() else None

    if algorithm == 'Bubble Sort':
        bubble_sort(data, lambda d, c: draw_data(canvas, d, c), speed)
    elif algorithm == 'Selection Sort':
        selection_sort(data, lambda d, c: draw_data(canvas, d, c), speed)
    elif algorithm == 'Merge Sort':
        merge_sort(data, lambda d, c: draw_data(canvas, d, c), speed)
    elif algorithm == 'Heap Sort':
        heap_sort(data, lambda d, c: draw_data(canvas, d, c), speed)
    elif algorithm == 'Binary Search' and target is not None:
        data.sort()
        binary_search(data, lambda d, c: draw_data(canvas, d, c), speed, target)
    elif algorithm == 'Ternary Search' and target is not None:
        data.sort()
        ternary_search(data, lambda d, c: draw_data(canvas, d, c), speed, target)

def generate():
    global data
    data = [random.randint(10, 100) for _ in range(50)]
    draw_data(canvas, data, ['blue' for _ in range(len(data))])

# ----------------------------- Main GUI -----------------------------
root = tk.Tk()
root.title("Algorithm Visualizer - DSA Based")
root.maxsize(1000, 700)
root.config(bg='white')

algo_menu = ttk.Combobox(root, values=[
    'Bubble Sort', 'Selection Sort', 'Merge Sort', 'Heap Sort',
    'Binary Search', 'Ternary Search'
])
algo_menu.grid(row=0, column=1, padx=5, pady=5)
algo_menu.current(0)

speed_scale = tk.Scale(root, from_=0.01, to=1.0, resolution=0.01, length=200,
                       digits=3, orient=tk.HORIZONTAL, label="Select Delay (s)")
speed_scale.grid(row=0, column=2, padx=5, pady=5)
speed_scale.set(0.1)

entry = tk.Entry(root)
entry.grid(row=0, column=3, padx=5)

tk.Button(root, text="Generate", command=generate, bg='lightblue').grid(row=0, column=0, padx=5, pady=5)
tk.Button(root, text="Start", command=start_algorithm, bg='lightgreen').grid(row=0, column=4, padx=5, pady=5)

canvas = tk.Canvas(root, width=800, height=400, bg='white')
canvas.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

root.mainloop()
