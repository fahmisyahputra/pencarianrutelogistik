from flask import Flask, render_template, request, jsonify
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

city_map = {
    'JAKARTA': {'BOGOR': 6, 'DEPOK': 3, 'TANGERANG': 4, 'BEKASI': 3, 'BANDUNG': 15},
    'BOGOR': {'JAKARTA': 6, 'DEPOK': 4, 'BANDUNG': 12},
    'DEPOK': {'JAKARTA': 3, 'BOGOR': 4, 'BEKASI': 2},
    'TANGERANG': {'JAKARTA': 4, 'BEKASI': 6},
    'BEKASI': {'JAKARTA': 3, 'DEPOK': 2, 'TANGERANG': 6, 'BANDUNG': 14},
    'BANDUNG': {'JAKARTA': 15, 'BOGOR': 12, 'BEKASI': 14, 'CIREBON': 13, 'SEMARANG': 30},
    'CIREBON': {'BANDUNG': 13, 'SEMARANG': 21, 'TEGAL': 10},
    'SEMARANG': {'CIREBON': 21, 'YOGYAKARTA': 12, 'SOLO': 10, 'BANDUNG': 30, 'TEGAL': 15},
    'YOGYAKARTA': {'SEMARANG': 12, 'SOLO': 6, 'MAGELANG': 4, 'PURWOKERTO': 18},
    'SOLO': {'SEMARANG': 10, 'YOGYAKARTA': 6, 'PURWOKERTO': 17, 'MALANG': 22},
    'MAGELANG': {'YOGYAKARTA': 4, 'SEMARANG': 10},
    'PURWOKERTO': {'SOLO': 17, 'YOGYAKARTA': 18, 'TEGAL': 10},
    'TEGAL': {'PURWOKERTO': 10, 'CIREBON': 10, 'SEMARANG': 15},
    'SURABAYA': {'SIDOARJO': 2, 'GRESIK': 3, 'MOJOKERTO': 4, 'BANYUWANGI': 25, 'MALANG': 7},
    'SIDOARJO': {'SURABAYA': 2, 'GRESIK': 4, 'JOMBANG': 7},
    'GRESIK': {'SURABAYA': 3, 'SIDOARJO': 4, 'MOJOKERTO': 5, 'JOMBANG': 6, 'MALANG': 7},
    'MOJOKERTO': {'SURABAYA': 4, 'GRESIK': 5, 'MALANG': 8},
    'JOMBANG': {'SIDOARJO': 7, 'GRESIK': 6, 'MALANG': 5},
    'MALANG': {'GRESIK': 7, 'MOJOKERTO': 8, 'JOMBANG': 5, 'SOLO': 22, 'SURABAYA': 7},
    'BANYUWANGI': {'SURABAYA': 25}
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
