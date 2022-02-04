import networkx as nx
import matplotlib.pyplot as plt
import requests
from threading import Thread
import re
from time import sleep

seen = set()
graph = nx.Graph()

titles = {}
htmls = {}
hyperlinks = {}

def get_html(link):
    if link in htmls:
        return htmls[link]
    sleep(0.05)
    print(link)
    html = requests.get(link).text
    htmls[link] = html
    return html

def get_title(link):
    if link in titles:
        return titles[link]
    k = re.findall(r'(?<=<title>).+(?=</title>)', get_html(link))
    k = k[0] if k else "X"
    titles[link] = k
    return k

def get_hyperlinks(link):
    if link in hyperlinks:
        return hyperlinks[link]

    html_page = get_html(link)
    links = re.findall(r'(?<=href=")http.+?(?=")', html_page)[:10]
    d = {}
    for x in links:
        d[get_title(x)] = x
    hyperlinks[link] = d
    return d


def draw(current, kids):
    c_t = get_title(current)
    for x in kids:
        if c_t == x:
            continue
        graph.add_edge(c_t, x)

link = "http://google.com/"

def get_graph(link, depth=3):
    if depth <= 0:
        return
    kids = get_hyperlinks(link)
    print("working at depth", depth)
    draw(link, kids)
    threads = []
    for x in kids.values():
        thread = Thread(target = get_graph, args=(x, depth - 1))
        threads.append(thread)
        thread.start()

    for x in threads:
        x.join()

get_graph(link, 4)
nx.draw(graph, with_labels = True, font_size=5, node_size=100)
plt.show()
