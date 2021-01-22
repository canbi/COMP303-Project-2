import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
from dijkstra import *
import time


root = Tk()                   # creates window
root.geometry('530x600+400+300') #window width, height and starting position
root.title('Find Shortest Path')   #window title

number_of_cities = 0
source = 0
destination = 0
constant_diff = 3
graph= {"from": [], "to": [], "weight": [], "color": []}

edges_list={}
path_nodes=[]

def main():
    global textBox
    global errorBox
    global variableSource
    global variableDes
    global img
    global shortest_path
    global shortest_distance

    shortest_path=Label(root, text="", fg="red",font=("Arial",12,'bold'),wraplength=150, justify=LEFT)
    shortest_distance=Label(root, text="", fg="red",font=("Arial",12,'bold'),wraplength=150, justify=LEFT)
    shortest_path.pack()
    shortest_distance.pack()
    shortest_path.place(x=350,y=150)
    shortest_distance.place(x=350,y=170)

    errorBox=Label(root, text="", fg="red",font=("Arial",12,'bold'),wraplength=150, justify=LEFT)
    errorBox.pack()
    errorBox.place(x=50,y=170)

    Label(root, text="Number of Nodes\nN>0 and N<20",font=("Arial",12,'bold'), justify=LEFT).place(x=50,y=40)
    textBox=Text(root,font=("Arial",12,'bold'), width=5, height=1)
    textBox.pack()
    textBox.place(x=60,y=90)

    buttonGenerate=Button(root,text="Initialize Graph", font=("Arial",12,'bold'), command=lambda: initilizeButton())
    buttonGenerate.pack()
    buttonGenerate.place(x=50,y=120)

    variableSource = StringVar(root)
    variableDes = StringVar(root)

    variableSource.trace('w', change_source)
    variableDes.trace('w', change_des)

    root.mainloop()


def initilizeButton():
    global errorBox
    global textBox
    answer=textBox.get("1.0","end-1c")
    errorBox.config(text="")
    if not answer.isdigit():
        textBox.delete('1.0', END)
        errorBox.config(text="Number of Nodes should be integer")
    else:
        global number_of_cities
        if int(answer)<0 or int(answer)>20:
            textBox.delete('1.0', END)
            errorBox.config(text="Number of Nodes should be N>0 or N<20")
        else:
            number_of_cities= int(answer)
            global variableSource
            global variableDes

            Label(root, text="Source",font=("Arial",12,'bold'), justify=LEFT).place(x=300,y=40)
            Label(root, text="Destionation",font=("Arial",12,'bold'), justify=LEFT).place(x=400,y=40)
            Label(root, text="Shortest Path",font=("Arial",12,'bold'), justify=LEFT).place(x=200,y=150)
            Label(root, text="Shortest Distance",font=("Arial",12,'bold'), justify=LEFT).place(x=200,y=170)
            Label(root, text="->",font=("Arial",16,'bold'), justify=LEFT).place(x=380,y=70)

            OPTIONS = [*range(1,number_of_cities+1)]
            variableSource.set(OPTIONS[0]) # default value
            sourceMenu = OptionMenu(root, variableSource, *OPTIONS)
            sourceMenu.pack()
            sourceMenu.place(x=310,y=70)

            variableDes.set(OPTIONS[1]) # default value
            destinationMenu = OptionMenu(root, variableDes, *OPTIONS)
            destinationMenu.pack()
            destinationMenu.place(x=420,y=70)

            buttonPath=Button(root,text="Find Shortest Path", font=("Arial",12,'bold'), command=lambda: findShortestPath())
            buttonPath.pack()
            buttonPath.place(x=315,y=110)
            drawGraph()
            

def drawGraph():
    initGraph()
    drawNetwork()
    printImage()

def findShortestPath():
    drawGraph()
    printAllSteps()


def printAllSteps():
    global graph, destination,source,path_nodes
    path_nodes =[]
    returned_path, returned_distance = Graph(graph).shortest_path(source, destination)
    for i in range(len(returned_path)-1):
        plt.clf()
        # Coloring specific edge
        a = returned_path[i]
        b = returned_path[i+1]

        if a not in path_nodes:
            path_nodes.append(a)
        if b not in path_nodes:
            path_nodes.append(b)

        graph["color"][edges_list.get(str(b if a>b else a)+"-"+str(a if a>b else b))] ="red"
        G,pos,edges = drawInit()
        nx.draw_networkx_nodes(G,pos=pos,nodelist=path_nodes,node_color="red", node_size=600)
        nx.draw(G, pos= pos, with_labels=True , node_color='skyblue', node_size=400, edge_color=edges['color'], width=1.0, edge_cmap=plt.cm.Blues)
        plt.savefig('graph.jpg')
        printImage()
        time.sleep(1)

    shortest_path.config(text=str(' -> '.join(str(elem) for elem in list(returned_path))))
    shortest_distance.config(text=returned_distance)


def printImage():
    global img, imagebox
    plotimage = Image.open("graph.jpg")
    plotimage.thumbnail((480, 360), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(plotimage)
    imagebox = Label(root,image=img)
    imagebox.pack()
    imagebox.place(x=20,y=200)

# on change dropdown value
def change_des(*args):
    global destination
    des_ = int(variableDes.get())
    destination = des_

# on change dropdown value
def change_source(*args):
    global source
    source_ = int(variableSource.get())
    source = source_

def initGraph():
    plt.clf()
    global graph, shortest_distance, shortest_path
    shortest_distance.config(text="")
    shortest_path.config(text="")
    graph= {"from": [], "to": [], "weight": [], "color": []}
    number_of_edges=0;
    for i in range(1,number_of_cities+1):
        for j in range(1,number_of_cities+1):
            if i != j and j>i and abs(i-j) <= constant_diff:
                graph["from"].append(i)
                graph["to"].append(j)
                graph["weight"].append(i+j)
                edges_list[str(i)+"-"+str(j)]= number_of_edges
                number_of_edges+=1
    graph["color"]=["black" for i in range(number_of_edges)]

def drawInit():
    edges = pd.DataFrame({"source": graph["from"], "target": graph["to"], "weight": graph["weight"], "color": graph["color"]})
    G = nx.from_pandas_edgelist(edges, edge_attr=True)
    fixed_positions =fixedPositions()
    pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_positions.keys())
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    return G,pos,edges

def drawNetwork():
    G,pos,edges = drawInit()
    nx.draw(G, pos= pos, with_labels=True, node_color='skyblue', node_size=400, edge_color=edges['color'], width=1.0, edge_cmap=plt.cm.Blues)
    plt.savefig('graph.jpg')

def fixedPositions():
    fixed_positions={}
    count=1
    for i in range(1,number_of_cities+1):
        fixed_positions[count] = ((count//2)+1 if count%2==1 else count//2, 2 if count%2==1 else 1)
        count +=1
    return fixed_positions

if __name__=='__main__':
    main()
