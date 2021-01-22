import datetime
import matplotlib.pyplot as plt
import math
from dijkstra import *
import numpy as np
constant_diff =3

def main():
    n = [10,50,100,200,500,1000,1500,2000]
    results = []
    theory_results = []
    for i in n:
        graph,number_of_edges= initGraph(i)
        start_time= datetime.datetime.now()
        returned_path, returned_distance = Graph(graph).shortest_path(1, i) # S=1 , D=N
        end_time = datetime.datetime.now()
        result = end_time-start_time
        results.append(result.microseconds)
        theory_time = (i+ number_of_edges)*math.log(i)
        theory_results.append(theory_time)

    # Drawing a graph
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('N')
    ax1.set_ylabel('Actual Running Time in microseconds', color=color)
    ax1.plot(n, results, marker='o', color='r')
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Theoretical Running Time', color=color)  # we already handled the x-label with ax1
    ax2.plot(n, theory_results, marker='o', linestyle='--', color='b')
    ax2.tick_params(axis='y', labelcolor=color)
    ax1.legend(['Dijkstra Running Time'], loc='upper right')
    ax2.legend(['Dijkstra Theoretical Time'], loc='upper left')
    plt.title('Shortest Path Finding Algorithms',fontsize=20, )
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig("test.jpg")

def initGraph(n):
    graph= {"from": [], "to": [], "weight": []}
    number_of_edges=0;
    for i in range(1,n+1):
        for j in range(1,n+1):
            if i != j and j>i and abs(i-j) <= constant_diff:
                graph["from"].append(i)
                graph["to"].append(j)
                graph["weight"].append(i+j)
                number_of_edges+=1
    return graph,number_of_edges
if __name__=='__main__':
    main()
