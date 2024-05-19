from flask import Flask, render_template, request, jsonify
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

# Data city_map
# city_map = {
#     'SURABAYA': {'SIDOARJO': 5, 'GRESIK': 9, 'MOJOKERTO': 4},
#     'SIDOARJO': {'SURABAYA': 5, 'GRESIK': 3, 'JOMBANG': 7},
#     'GRESIK': {'SURABAYA': 9, 'SIDOARJO': 3, 'MOJOKERTO': 2, 'JOMBANG': 6, 'MALANG': 3},
#     'MOJOKERTO': {'SURABAYA': 4, 'GRESIK': 2, 'MALANG': 8},
#     'JOMBANG': {'SIDOARJO': 7, 'GRESIK': 6, 'MALANG': 5},
#     'MALANG': {'GRESIK': 3, 'MOJOKERTO': 8, 'JOMBANG': 5}
# }

city_map = {
    'JAKARTA': {'BOGOR': 60, 'DEPOK': 25, 'TANGERANG': 35, 'BEKASI': 25, 'BANDUNG': 150},
    'BOGOR': {'JAKARTA': 60, 'DEPOK': 30, 'BANDUNG': 120},
    'DEPOK': {'JAKARTA': 25, 'BOGOR': 30},
    'TANGERANG': {'JAKARTA': 35},
    'BEKASI': {'JAKARTA': 25},
    'BANDUNG': {'JAKARTA': 150, 'BOGOR': 120, 'CIREBON': 130, 'SEMARANG': 360},
    'CIREBON': {'BANDUNG': 130, 'SEMARANG': 210},
    'SEMARANG': {'CIREBON': 210, 'YOGYAKARTA': 120, 'SOLO': 100},
    'YOGYAKARTA': {'SEMARANG': 120, 'SOLO': 60, 'MAGELANG': 40},
    'SOLO': {'SEMARANG': 100, 'YOGYAKARTA': 60, 'PURWOKERTO': 170},
    'MAGELANG': {'YOGYAKARTA': 40},
    'PURWOKERTO': {'SOLO': 170, 'TEGAL': 100},
    'TEGAL': {'PURWOKERTO': 100},
    'SURABAYA': {'SIDOARJO': 25, 'GRESIK': 9, 'MOJOKERTO': 4, 'BANYUWANGI': 300},
    'SIDOARJO': {'SURABAYA': 25, 'GRESIK': 3, 'JOMBANG': 7},
    'GRESIK': {'SURABAYA': 9, 'SIDOARJO': 3, 'MOJOKERTO': 2, 'JOMBANG': 6, 'MALANG': 3},
    'MOJOKERTO': {'SURABAYA': 4, 'GRESIK': 2, 'MALANG': 8},
    'JOMBANG': {'SIDOARJO': 7, 'GRESIK': 6, 'MALANG': 5},
    'MALANG': {'GRESIK': 3, 'MOJOKERTO': 8, 'JOMBANG': 5},
    'BANYUWANGI': {'SURABAYA': 300}
}


# BFS implementation
def bfs(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in set(graph[vertex]) - set(path):
            if next == goal:
                return path + [next]
            else:
                queue.append((next, path + [next]))
    return None

# DFS implementation
def dfs(graph, start, goal, path=[]):
    path = path + [start]
    if start == goal:
        return path
    for node in graph[start]:
        if node not in path:
            newpath = dfs(graph, node, goal, path)
            if newpath:
                return newpath
    return None

# Generate city graph for visualization
def generate_city_graph():
    G = nx.Graph()

    for city, neighbors in city_map.items():
        for neighbor, distance in neighbors.items():
            G.add_edge(city, neighbor, weight=distance)

    return G

# Route to render the index page
@app.route('/')
def index():
    G = generate_city_graph()

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', edge_color='gray')
    plt.savefig('static/city_graph.png')  # Save the graph as a static image
    plt.clf()  # Clear the plot

    return render_template('index.html')

# Route to handle the form submission and perform selected algorithm search
@app.route('/search_route', methods=['POST'])
def search_route():
    start = request.form.get('start').upper()
    goal = request.form.get('goal').upper()
    algorithm = request.form.get('algorithm')

    if start not in city_map or goal not in city_map:
        return jsonify({'result': 'Kota awal atau Kota tujuan invalid.'})

    path = None
    if algorithm == 'BFS':
        path = bfs(city_map, start, goal)
    elif algorithm == 'DFS':
        path = dfs(city_map, start, goal)

    if path:
        result = "Rute ditemukan: " + " -> ".join(path)
    else:
        result = "Rute tidak ditemukan"

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
