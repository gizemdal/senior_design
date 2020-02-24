# Game State
from character import Character
import queue

id = 0 # plot point id
class PlotPoint(object):

    def __init__(self):
        global id
        self.id = id
        id += 1 # increment global id for unique ids per plot point

# Plot data structure: a directed graph-like structure with plot points as vertices and plot dependencies as edges
class Plot(object):
    
    def __init__(self, start):
        self.start = start
        self.plot_points = {} # id -> plot point mapping
        self.adjacency_list = {} # plotPoint -> (adjacent plot point, dependencies/preconditions) mapping

        # add starting plot point to plot point dict
        self.plot_points[self.start.id] = self.start
    
    def add_plot_point(self, point):
        if point.id not in self.plot_points:
            self.plot_points[point.id] = point

    def add_new_adjacent(self, from_plot, to_plot, conditions):
        if from_plot.id not in self.adjacency_list:
            self.adjacency_list[from_plot.id] = (to_plot.id, conditions)
        else:
            self.adjacency_list[from_plot.id] = self.adjacency_list[from_plot.id].append((to_plot.id, conditions))
    
    def add_condition_to_existing_pair(self, from_plot, to_plot, condition):
        for adj in self.adjacency_list[from_plot.id]:
            if adj[0] == to_plot.id:
                adj = (adj[0], adj[1].append(condition))
                return
    
    def does_path_exist(self, from_plot, to_plot):
        q = queue.Queue()
        q.put(from_plot.id)
        visited = []
        while not q.empty():
            current = q.get()
            for adj in self.adjacency_list[current]:
                if adj[0] == to_plot.id:
                    return True
                if adj[0] not in visited:
                    q.put(adj[0])
            visited.append(current)
        return False

class GameState(object):

    def __init__(self, player, start_at, plot):
        self.player = player
        self.current_location = start_at
        self.npcs = {}
        self.locations = {}
        self.plot = plot
        self.current_plot_point = self.plot.start

    def is_condition_satisfied(self, condition):
        # Condition = (condition text, condition element)
        # Depending on condition text, check if the given condition element satisfies the condition
        
        # Multiple if checks
        if condition[0] == 'item_in_player_inventory':
            if self.player.check_item(condition[1]):
                return True
        elif condition[0] == 'item_in_npc_inventory':
            # In this case, the condition[1] will be of type (npc, item) tuple
            npc = condition[1][0]
            if npc.check_item(condition[1][1]):
                return True
        elif condition[0] == 'item_in_location':
            # In this case, the condition[1] will be of type (location, item) tuple
            loc = condition[1][0]
            if loc.check_item(condition[1][1]):
                return True
        elif condition[0] == 'player_is_friends_with':
            # In this case, the condition[1] will contain the NPC character
            if self.player.relationship_status(condition[1]) in ['friend', 'good friend']:
                return True
        return False