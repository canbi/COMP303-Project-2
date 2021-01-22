import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import *


root = Tk()                   # creates window
root.geometry('800x600+400+300') #window width, height and starting position
root.title('Find Shortest Path')   #window title

number_of_cities = 0
source = 0
destination = 0
constant_diff = 3
graph= {"from": [], "to": [], "weight": [], "color": []}

edges_list={}
shortest_path=[]

def main():
    global textBox
    global errorBox
    global variableSource
    global variableDes

    errorBox=Label(root, text="", fg="red",font=("Arial",12,'bold'),wraplength=150, justify=LEFT)
    errorBox.pack()
    errorBox.place(x=50,y=180)

    Label(root, text="Number of Nodes\nN>0 and N<20",font=("Arial",12,'bold'), justify=LEFT).place(x=50,y=50)
    textBox=Text(root,font=("Arial",12,'bold'), width=5, height=1)
    textBox.pack()
    textBox.place(x=60,y=100)

    buttonGenerate=Button(root,text="Initialize Graph", font=("Arial",12,'bold'), command=lambda: initilizeButton())
    buttonGenerate.pack()
    buttonGenerate.place(x=50,y=130)

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

            Label(root, text="Source",font=("Arial",12,'bold'), justify=LEFT).place(x=300,y=50)
            Label(root, text="Destionation",font=("Arial",12,'bold'), justify=LEFT).place(x=400,y=50)
            Label(root, text="->",font=("Arial",16,'bold'), justify=LEFT).place(x=380,y=80)

            OPTIONS = [*range(1,number_of_cities+1)]
            variableSource.set(OPTIONS[0]) # default value
            sourceMenu = OptionMenu(root, variableSource, *OPTIONS)
            sourceMenu.pack()
            sourceMenu.place(x=310,y=80)

            variableDes.set(OPTIONS[1]) # default value
            destinationMenu = OptionMenu(root, variableDes, *OPTIONS)
            destinationMenu.pack()
            destinationMenu.place(x=420,y=80)

            buttonPath=Button(root,text="Find Shortest Path", font=("Arial",12,'bold'), command=lambda: findShortestPath())
            buttonPath.pack()
            buttonPath.place(x=315,y=120)




def findShortestPath():
    initGraph()
    drawGraph()


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
    number_of_edges=0;
    # initialize edges
    print(number_of_cities)
    for i in range(1,number_of_cities+1):
        for j in range(1,number_of_cities+1):
            if i != j and j>i and abs(i-j) <= constant_diff:
                graph["from"].append(i)
                graph["to"].append(j)
                graph["weight"].append(i+j)
                edges_list[str(i)+"-"+str(j)]= number_of_edges
                number_of_edges+=1
    graph["color"]=["black" for i in range(number_of_edges)]

def drawGraph():

    # Simple integer weights on edges:
    pd.options.display.max_columns = 20
    #TODO dataframe kullanamya gerek var mı? her şeyi graph'tan verebilir miyiz?
    edges = pd.DataFrame({"source": graph["from"], "target": graph["to"], "weight": graph["weight"], "color": graph["color"]})
    G = nx.from_pandas_edgelist(edges, edge_attr=True)

    fixed_positions={}
    count=1
    for i in range(1,number_of_cities+1):
        fixed_positions[count] = ((count//2)+1 if count%2==1 else count//2, 2 if count%2==1 else 1)
        count +=1

    print(fixed_positions)
    fixed_nodes = fixed_positions.keys()
    pos = nx.spring_layout(G,pos=fixed_positions, fixed = fixed_nodes)
    print(G[2][1]["color"])
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    nx.draw(G, pos= pos, with_labels=True, node_color='skyblue', node_size=500, edge_color=edges['color'], width=2.0, edge_cmap=plt.cm.Blues)
    plt.savefig('graph.png')



    """
    # Coloring specific edge
    i=1
    j=2
    shortest_path.append(j if i>j else i)
    shortest_path.append(i if i>j else j)
    colorValues[edges_list.get(str(j if i>j else i)+"-"+str(i if i>j else j))] ="red"
    edges = pd.DataFrame({"source": fromNode, "target": toNode, "weight": edgeWeights, "color": colorValues})
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    nx.draw_networkx_nodes(G,pos=pos,nodelist=shortest_path,node_color="red", node_size=600)
    nx.draw(G, pos= pos, with_labels=True , node_color='skyblue', node_size=500, edge_color=edges['color'], width=2.0, edge_cmap=plt.cm.Blues)
    plt.show()
    """

if __name__=='__main__':
    main()


