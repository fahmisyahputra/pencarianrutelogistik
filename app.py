from flask import Flask, render_template, request, jsonify
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
    queue = [(start, [start], 0)]  # Initial path and distance
    while queue:
        (vertex, path, distance) = queue.pop(0)
        for next in set(graph[vertex]) - set(path):
            if next == goal:
                return path + [next], distance + (graph[vertex][next] * 10)  # Multiply distance by 10
            else:
                queue.append((next, path + [next], distance + (graph[vertex][next] * 10)))  # Multiply distance by 10
    return None, None

# DFS implementation
def dfs(graph, start, goal, path=[], distance=0):
    path = path + [start]
    if start == goal:
        return path, distance
    for node in graph[start]:
        if node not in path:
            newpath, newdistance = dfs(graph, node, goal, path, distance + (graph[start][node] * 10))  # Multiply distance by 10
            if newpath:
                return newpath, newdistance
    return None, None

# Route to render the index page
@app.route('/')
def index():
    return render_template('main.html')

# Route to handle the form submission and perform selected algorithm search
@app.route('/search_route', methods=['POST'])
def search_route():
    start = request.form.get('start').upper()
    goal = request.form.get('goal').upper()
    algorithm = request.form.get('algorithm')

    if start not in city_map and goal not in city_map:
        return jsonify({'result': f'{start} and {goal} cities are invalid.', 'status': 'error'})
    elif start not in city_map:
        return jsonify({'result': f'{start} city is invalid.', 'status': 'error'})
    elif goal not in city_map:
        return jsonify({'result': f'{goal} city is invalid.', 'status': 'error'})

    path = None
    total_distance = 0

    if algorithm == 'BFS':
        path, total_distance = bfs(city_map, start, goal)
    elif algorithm == 'DFS':
        path, total_distance = dfs(city_map, start, goal)

    if path:
        route_str = ' -> '.join(path)
        distance_str = ''
        prev_city = None
        for city in path:
            if prev_city:
                distance = city_map[prev_city][city] * 10
                distance_str += f"\n{prev_city} -> {city} = {distance} km"
            prev_city = city

        result = f"Route Found:<br> {route_str}<br><br>Distance between Each City:<br>{distance_str.replace('\n', '<br>')}<br><br>Total Distance: {total_distance} km"
    else:
        result = "Rute tidak ditemukan"

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
