from math import pi , acos , sin , cos
import math
import sys
import time
from collections import deque  
import heapq
import tkinter as tk

start = time.perf_counter()

def calcd(node1, node2):
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees
   y1, x1 = node1
   y2, x2 = node2

   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

def convert_to_xy(lat, long):
    return(((6600/360)*(180+long))-900, ((2200/180)*(90-lat))-200)
    #return(((1250/360)*(180+long)), ((1000/180)*(90-lat)))

dict_lines = {}
def draw_original_lines(canvas):
    for key, value in dict_edges.items():
        start = dict_nodes.get(key)
        start1, start2 = convert_to_xy(start[0], start[1])
        for val in value:
            end = dict_nodes.get(val[0])
            end1, end2 = convert_to_xy(end[0], end[1])
            line = canvas.create_line((start1), (start2), (end1), (end2))
            canvas.itemconfig(line, fill="white")
            dict_lines[(key, val[0])] = line
            if (val[0], key) not in dict_lines:
                dict_lines[(val[0], key)] = line

dict_nodecity = {}
dict_nodes = {}
dict_edges = {}

with open("rrNodeCity.txt") as f:
    for line in f:
        temp = []
        for edge in line.split():
            temp.append(edge)
        if len(temp)==3:
            dict_nodecity[temp[1] + ' ' + temp[2]] = temp[0]
        else:
            dict_nodecity[temp[1]] = temp[0]

with open("rrNodes.txt") as f:
    for line in f:
        temp = []
        for edge in line.split():
            temp.append(edge)
        temp_tuple = (float(temp[1]), float(temp[2]))
        dict_nodes[temp[0]] = temp_tuple

with open("rrEdges.txt") as f:
    for line in f:
        temp = []
        for edge in line.split():
            temp.append(edge)
        tuple_1 = dict_nodes.get(temp[0])
        tuple_2 = dict_nodes.get(temp[-1])
        distance = calcd(tuple_1, tuple_2)
        distance2 = calcd(tuple_2, tuple_1)
        if temp[0] not in dict_edges:
            dict_edges[temp[0]] = []
        if temp[-1] not in dict_edges:
            dict_edges[temp[-1]] = []
        dict_edges[temp[0]].append((temp[-1], distance))
        dict_edges[temp[-1]].append((temp[0], distance2))

end = time.perf_counter()

def dijikstra(start, end, r, c):
    start_node = dict_nodecity.get(start)
    end_node = dict_nodecity.get(end)
    closed = set()
    fringe = [(0, start_node, None, None, None)]
    heapq.heapify(fringe)
    while fringe:
        v = heapq.heappop(fringe)
        if v[1]==end_node:
            current = v
            while current is not None:
                c.itemconfig(current[2], fill="green")
                c.itemconfig(current[3], fill="green")
                current = current[4]
            r.update()
            time.sleep(5)
            r.destroy()
            return v[0]
        if v[1] not in closed:
            closed.add(v[1])
            count = 0
            for child in dict_edges.get(v[1]):
                if child[1] not in closed:
                    if (v[1], child[0]) in dict_lines:
                        count+=1
                        temp = (v[0]+child[1], child[0], dict_lines.get((v[1], child[0])), dict_lines.get((child[0], v[1])), v) 
                        heapq.heappush(fringe, temp)
                        c.itemconfig(dict_lines.get((v[1], child[0])), fill="red")
                        if count==5:
                            r.update()
    return None

def a_star(start, end, r2, c2):
    start_node = dict_nodecity.get(start)
    end_node = dict_nodecity.get(end)
    tuple_2 = dict_nodes.get(end_node)
    closed = set()
    temp_1 = dict_nodes.get(start_node)
    fringe = [(calcd(temp_1, tuple_2), start_node, 0, None, None, None, None)]
    heapq.heapify(fringe)
    count = 0
    while fringe:
        v = heapq.heappop(fringe)
        if v[1]==end_node:
            store = v
            while store is not None:
                c2.itemconfig(store[4], fill="green")
                c2.itemconfig(store[5], fill="green")
                store = store[3]
            r2.update()
            time.sleep(5)
            r2.destroy()
            return v[2]
        if v[1] not in closed:
            closed.add(v[1])
            for child in dict_edges.get(v[1]):
                if child not in closed:
                    if (v[1], child[0]) in dict_lines:
                        tuple_1 = dict_nodes.get(child[0])
                        distance_to_end = calcd(tuple_1, tuple_2)
                        temp = (v[2]+child[1]+distance_to_end, child[0], v[2]+child[1], v, dict_lines[(v[1], child[0])], dict_lines[(child[0], v[1])]) 
                        heapq.heappush(fringe, temp)
                        c2.itemconfig(dict_lines.get((v[1], child[0])), fill="red")
                        count+=1
                        if count==200:
                            r2.update()
                            count = 0
    return None

root = tk.Tk() #creates the frame

canvas = tk.Canvas(root, height=1000, width=1500, bg='black') #creates a canvas widget, which can be used for drawing lines and shapes
draw_original_lines(canvas)
canvas.pack(expand=True) #packing widgets places them on the board

dijikstra(sys.argv[1], sys.argv[2], root, canvas)
#a_star(sys.argv[1], sys.argv[2], root, canvas)

root.mainloop()

root2 = tk.Tk() #creates the frame

canvas2 = tk.Canvas(root2, height=1000, width=1500, bg='black') #creates a canvas widget, which can be used for drawing lines and shapes
draw_original_lines(canvas2)
canvas2.pack(expand=True) #packing widgets places them on the board

a_star(sys.argv[1], sys.argv[2], root2, canvas2)

root2.mainloop()



"""print("Time to create data structure: " + str(end-start))
start_dijikstra = time.perf_counter()
str_dijikstra = str(dijikstra(sys.argv[1], sys.argv[2]))
end_dijikstra = time.perf_counter()
print(sys.argv[1] + " to " + sys.argv[2] + " with Dijkstra: " + str_dijikstra + " in " + str(end_dijikstra-start_dijikstra) + " seconds")
start_astar = time.perf_counter()
str_astar = str(a_star(sys.argv[1], sys.argv[2]))
end_astar = time.perf_counter()
print(sys.argv[1] + " to " + sys.argv[2] + " with A*: " + str_astar + " in " + str(end_astar-start_astar) + " seconds")"""