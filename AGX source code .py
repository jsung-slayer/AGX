

from collections import defaultdict, deque
import heapq
import random
import time


# =========================================================
# NODE CLASS
# =========================================================

class Node:
    def __init__(self, node_id, data=None):
        self.id = node_id
        self.data = data
        self.visit_count = 0
        self.last_access_time = time.time()
        self.weight = 1

    def accessed(self):
        self.visit_count += 1
        self.last_access_time = time.time()

    def __repr__(self):
        return f"Node({self.id})"


# =========================================================
# ADAPTIVE GRAPH X MAIN ENGINE
# =========================================================

class AdaptiveGraphX:

    def __init__(self, directed=False):
        self.directed = directed

        self.graph = defaultdict(list)
        self.nodes = {}

        self.edge_count = 0

        # Adaptive Learning Storage
        self.traversal_history = []
        self.node_activity = defaultdict(int)
        self.intent_patterns = defaultdict(list)

        # Runtime Optimization Metrics
        self.active_nodes = set()
        self.prediction_cache = {}

        print("[AGX] Adaptive Graph X Initialized")


    # =====================================================
    # NODE OPERATIONS
    # =====================================================

    def add_node(self, node_id, data=None):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, data)
            print(f"[AGX] Node Added: {node_id}")


    def remove_node(self, node_id):
        if node_id not in self.nodes:
            return

        del self.nodes[node_id]

        if node_id in self.graph:
            del self.graph[node_id]

        for src in self.graph:
            self.graph[src] = [
                edge for edge in self.graph[src]
                if edge[0] != node_id
            ]

        print(f"[AGX] Node Removed: {node_id}")


    # =====================================================
    # EDGE OPERATIONS
    # =====================================================

    def add_edge(self, u, v, weight=1):

        self.add_node(u)
        self.add_node(v)

        self.graph[u].append((v, weight))

        if not self.directed:
            self.graph[v].append((u, weight))

        self.edge_count += 1

        print(f"[AGX] Edge Added: {u} -> {v} | Weight={weight}")


    def display_graph(self):
        print("\n========== GRAPH STRUCTURE ==========")

        for node in self.graph:
            print(f"{node} --> {self.graph[node]}")


    # =====================================================
    # BFS TRAVERSAL
    # =====================================================

    def bfs(self, start):

        visited = set()
        queue = deque([start])

        traversal = []

        while queue:
            node = queue.popleft()

            if node not in visited:
                visited.add(node)
                traversal.append(node)

                self.track_node(node)

                for neighbor, _ in self.graph[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        self.store_history("BFS", traversal)

        return traversal


    # =====================================================
    # DFS TRAVERSAL
    # =====================================================

    def dfs(self, start):

        visited = set()
        stack = [start]

        traversal = []

        while stack:
            node = stack.pop()

            if node not in visited:
                visited.add(node)
                traversal.append(node)

                self.track_node(node)

                for neighbor, _ in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        self.store_history("DFS", traversal)

        return traversal


    # =====================================================
    # AUTO SWITCH TRAVERSAL ENGINE
    # =====================================================

    def adaptive_traversal(self, start):

        density = self.calculate_density()

        print(f"[AGX] Graph Density: {density:.2f}")

        if density > 0.5:
            print("[AGX] Using BFS Traversal")
            return self.bfs(start)

        else:
            print("[AGX] Using DFS Traversal")
            return self.dfs(start)


    # =====================================================
    # GRAPH DENSITY
    # =====================================================

    def calculate_density(self):

        v = len(self.nodes)
        e = self.edge_count

        if v <= 1:
            return 0

        max_edges = v * (v - 1)

        return e / max_edges


    # =====================================================
    # DIJKSTRA SHORTEST PATH
    # =====================================================

    def shortest_path(self, start, end):

        pq = [(0, start)]

        distances = {
            node: float('inf')
            for node in self.nodes
        }

        distances[start] = 0

        previous = {}

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_node == end:
                break

            for neighbor, weight in self.graph[current_node]:

                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node

                    heapq.heappush(
                        pq,
                        (distance, neighbor)
                    )

        path = []
        node = end

        while node in previous:
            path.append(node)
            node = previous[node]

        path.append(start)
        path.reverse()

        print(f"[AGX] Optimal Path: {path}")

        return path


    # =====================================================
    # PREDICTIVE PATH SELECTION
    # =====================================================

    def predictive_path_selection(self, start):

        print("[AGX] Running Predictive Path Selection...")

        neighbors = self.graph[start]

        if not neighbors:
            return None

        best_neighbor = max(
            neighbors,
            key=lambda x: self.node_activity[x[0]]
        )

        prediction = best_neighbor[0]

        self.prediction_cache[start] = prediction

        print(
            f"[AGX] Predicted Best Path from {start}: {prediction}"
        )

        return prediction


    # =====================================================
    # DYNAMIC EVALUATION ENGINE
    # =====================================================

    def dynamic_evaluation(self):

        print("\n========== AGX DYNAMIC EVALUATION ==========")

        print(f"Total Nodes: {len(self.nodes)}")
        print(f"Total Edges: {self.edge_count}")
        print(f"Active Nodes: {len(self.active_nodes)}")

        most_active = sorted(
            self.node_activity.items(),
            key=lambda x: x[1],
            reverse=True
        )

        print("Most Active Nodes:")

        for node, score in most_active[:5]:
            print(f"Node {node} -> Activity Score {score}")


    # =====================================================
    # MEMORY OPTIMIZATION
    # =====================================================

    def memory_optimization(self):

        print("\n[AGX] Running Memory Optimization...")

        removed = 0

        for node in list(self.graph.keys()):

            unique_edges = list(set(self.graph[node]))

            removed += len(self.graph[node]) - len(unique_edges)

            self.graph[node] = unique_edges

        print(f"[AGX] Duplicate Edges Removed: {removed}")


    # =====================================================
    # ACTIVE NODE TRACKING
    # =====================================================

    def track_node(self, node):

        self.node_activity[node] += 1
        self.active_nodes.add(node)

        if node in self.nodes:
            self.nodes[node].accessed()


    # =====================================================
    # SELF LEARNING ENGINE
    # =====================================================

    def self_learning_update(self):

        print("\n[AGX] Self Learning Engine Running...")

        if not self.traversal_history:
            return

        algorithm_usage = defaultdict(int)

        for algorithm, _ in self.traversal_history:
            algorithm_usage[algorithm] += 1

        print("Traversal Usage Statistics:")

        for algo, count in algorithm_usage.items():
            print(f"{algo} Used {count} Times")


    # =====================================================
    # STORE HISTORY
    # =====================================================

    def store_history(self, traversal_type, traversal):

        self.traversal_history.append(
            (traversal_type, traversal)
        )


    # =====================================================
    # GRAPH COMPRESSION
    # =====================================================

    def compress_graph(self):

        print("\n[AGX] Compressing Graph...")

        compressed = {}

        for node in self.graph:
            compressed[node] = len(self.graph[node])

        print("Compressed Representation:")
        print(compressed)

        return compressed


    # =====================================================
    # INTENT BASED COMPUTING SYSTEM
    # =====================================================

    def record_user_intent(self, user, action):

        self.intent_patterns[user].append(action)

        print(
            f"[AGX] Intent Recorded -> User: {user}, Action: {action}"
        )


    def predict_user_intent(self, user):

        actions = self.intent_patterns[user]

        if not actions:
            return None

        prediction = max(
            set(actions),
            key=actions.count
        )

        print(
            f"[AGX] Predicted Next Intent for {user}: {prediction}"
        )

        return prediction


    # =====================================================
    # RUNTIME STRUCTURAL EVOLUTION
    # =====================================================

    def evolve_structure(self):

        print("\n[AGX] Runtime Evolution Activated...")

        for node in self.nodes:

            if self.node_activity[node] > 5:

                random_node = random.choice(
                    list(self.nodes.keys())
                )

                if random_node != node:
                    self.add_edge(node, random_node)

        print("[AGX] Graph Structure Updated Dynamically")


# =========================================================
# AGX DEMONSTRATION
# =========================================================

if __name__ == "__main__":

    agx = AdaptiveGraphX(directed=False)

    # =====================================================
    # BUILD SAMPLE GRAPH
    # =====================================================

    agx.add_edge("A", "B", 4)
    agx.add_edge("A", "C", 2)
    agx.add_edge("B", "D", 5)
    agx.add_edge("C", "D", 1)
    agx.add_edge("D", "E", 3)
    agx.add_edge("E", "F", 2)
    agx.add_edge("C", "F", 8)

    # =====================================================
    # DISPLAY GRAPH
    # =====================================================

    agx.display_graph()

    # =====================================================
    # ADAPTIVE TRAVERSAL
    # =====================================================

    result = agx.adaptive_traversal("A")

    print("Traversal Result:")
    print(result)

    # =====================================================
    # SHORTEST PATH
    # =====================================================

    agx.shortest_path("A", "F")

    # =====================================================
    # PREDICTIVE PATH
    # =====================================================

    agx.predictive_path_selection("A")

    # =====================================================
    # USER INTENT SYSTEM
    # =====================================================

    agx.record_user_intent("Surya", "Open Music")
    agx.record_user_intent("Surya", "Open Game")
    agx.record_user_intent("Surya", "Open Music")

    agx.predict_user_intent("Surya")

    # =====================================================
    # MEMORY OPTIMIZATION
    # =====================================================

    agx.memory_optimization()

    # =====================================================
    # GRAPH COMPRESSION
    # =====================================================

    agx.compress_graph()

    # =====================================================
    # SELF LEARNING UPDATE
    # =====================================================

    agx.self_learning_update()

    # =====================================================
    # DYNAMIC EVALUATION
    # =====================================================

    agx.dynamic_evaluation()

    # =====================================================
    # RUNTIME EVOLUTION
    # =====================================================

    agx.evolve_structure()

    print("\n========== AGX EXECUTION COMPLETE ==========")


