from flask import Flask, render_template, request, jsonify
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

city_map = {
    # West Java
    'CILEGON': {'JAKARTA': 10},
    'JAKARTA': {'CILEGON': 10, 'CIKAMPEK': 8, 'BOGOR': 6},
    'BOGOR': {'JAKARTA': 6, 'BANDUNG': 3},
    'CIKAMPEK': {'JAKARTA': 8, 'BANDUNG': 8, 'CIREBON': 14},
    'BANDUNG': {'CIKAMPEK': 8, 'CIREBON': 14, 'TASIKMALAYA': 11, 'BOGOR': 13},
    'CIREBON': {'CIKAMPEK': 14, 'BANDUNG': 14, 'TEGAL': 8},
    'TASIKMALAYA': {'BANDUNG': 11, 'PURWOKERTO': 14},

    # Mid Java
    'TEGAL': {'CIREBON': 8, 'PURWOKERTO': 10, 'SEMARANG': 17},
    'PURWOKERTO': {'TEGAL': 10, 'YOGYAKARTA': 14, 'TASIKMALAYA': 14},
    'SEMARANG': {'TEGAL': 17, 'SURAKARTA': 10, 'KUDUS': 6},
    'SURAKARTA': {'SEMARANG': 10, 'YOGYAKARTA': 6, 'MADIUN': 11},
    'YOGYAKARTA': {'PURWOKERTO': 14, 'SURAKARTA': 6, 'PACITAN': 11},
    'KUDUS': {'REMBANG': 6, 'SEMARANG': 6},
    'REMBANG': {'KUDUS': 6, 'TUBAN': 10, 'MADIUN': 15},

    # East Java
    'MADIUN': {'SURAKARTA': 11, 'NGANJUK': 6, 'PONOROGO': 3, 'REMBANG': 15},
    'PONOROGO': {'MADIUN': 3, 'PACITAN': 8, 'TULUNGAGUNG': 9},
    'PACITAN': {'YOGYAKARTA': 11, 'PONOROGO': 8},
    'NGANJUK': {'SIDOARJO': 10, 'MADIUN': 6, 'TULUNGAGUNG': 7},
    'SIDOARJO': {'NGANJUK': 10, 'MALANG': 8, 'SURABAYA': 1, 'PROBOLINGGO': 10},
    'MALANG': {'SIDOARJO': 8, 'TULUNGAGUNG': 10, 'LUMAJANG': 9},
    'SURABAYA': {'SIDOARJO': 1, 'GRESIK': 2},
    'GRESIK': {'SURABAYA': 2, 'TUBAN': 9},
    'TULUNGAGUNG': {'PONOROGO': 9, 'MALANG': 10, 'NGANJUK': 7},
    'TUBAN': {'GRESIK': 9, 'REMBANG': 10},
    'PROBOLINGGO': {'SIDOARJO': 10, 'SITUBONDO': 11, 'LUMAJANG': 5},
    'BANYUWANGI': {'SITUBONDO': 10, 'JEMBER': 7},
    'JEMBER': {'BANYUWANGI': 7, 'LUMAJANG': 7, 'SITUBONDO': 7},
    'LUMAJANG': {'JEMBER': 7, 'MALANG': 9, 'PROBOLINGGO': 5},
    'SITUBONDO': {'JEMBER': 7, 'PROBOLINGGO': 11, 'BANYUWANGI': 10}
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
