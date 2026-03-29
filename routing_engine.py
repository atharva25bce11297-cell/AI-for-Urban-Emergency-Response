import heapq
import sqlite3

# ==========================================
# 1. CORE LOGIC (Fortified)
# ==========================================
class CityNode:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = {} 
        
    def heuristic(self, goal_node):
        return abs(self.x - goal_node.x) + abs(self.y - goal_node.y)
        
    def __lt__(self, other):
        return self.name < other.name 
        
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, CityNode) and self.name == other.name

def a_star_search(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    g_costs = {start: 0}
    came_from = {start: None}
    
    found_path = False
    
    while frontier:
        current_f, current_node = heapq.heappop(frontier)
        
        if current_node == goal:
            found_path = True
            break
            
        for next_node, travel_time in current_node.neighbors.items():
            new_g_cost = g_costs[current_node] + travel_time
            if next_node not in g_costs or new_g_cost < g_costs[next_node]:
                g_costs[next_node] = new_g_cost
                f_cost = new_g_cost + next_node.heuristic(goal)
                heapq.heappush(frontier, (f_cost, next_node))
                came_from[next_node] = current_node
                
    if not found_path:
        return None, -1
                
    path = []
    current = goal
    while current is not None:
        path.append(current.name)
        current = came_from.get(current)
    path.reverse()
    return path, g_costs[goal]

# ==========================================
# 2. UPGRADED DATABASE MANAGEMENT
# ==========================================
def setup_database():
    conn = sqlite3.connect('smart_city.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS intersections (
            city_name TEXT,
            name TEXT,
            x INTEGER,
            y INTEGER,
            PRIMARY KEY (city_name, name)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roads (
            city_name TEXT,
            start_node TEXT,
            end_node TEXT,
            travel_time INTEGER
        )
    ''')
    conn.commit()
    return conn

def save_city_to_db(conn, city_name, city_map):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM intersections WHERE city_name = ?', (city_name,))
    cursor.execute('DELETE FROM roads WHERE city_name = ?', (city_name,))
    
    for name, node in city_map.items():
        cursor.execute('INSERT INTO intersections (city_name, name, x, y) VALUES (?, ?, ?, ?)', 
                       (city_name, name, node.x, node.y))
        for neighbor, time in node.neighbors.items():
            cursor.execute('INSERT INTO roads (city_name, start_node, end_node, travel_time) VALUES (?, ?, ?, ?)', 
                           (city_name, name, neighbor.name, time))
    conn.commit()
    print(f"\n💾 '{city_name}' successfully saved to database!")

def load_city_from_db(conn, city_name):
    cursor = conn.cursor()
    city_map = {}
    
    cursor.execute('SELECT name, x, y FROM intersections WHERE city_name = ?', (city_name,))
    for row in cursor.fetchall():
        name, x, y = row
        city_map[name] = CityNode(name, x, y)
        
    cursor.execute('SELECT start_node, end_node, travel_time FROM roads WHERE city_name = ?', (city_name,))
    for start, end, time in cursor.fetchall():
        if start in city_map and end in city_map:
            city_map[start].neighbors[city_map[end]] = time
            
    print(f"\n📂 '{city_name}' successfully loaded!")
    return city_map

def get_saved_cities(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT city_name FROM intersections')
    return [row[0] for row in cursor.fetchall()]

# ==========================================
# 3. MAIN INTERFACE (WITH QoL UPDATES)
# ==========================================
def main():
    print("🌍 WELCOME TO THE SMART CITY DISPATCH BUILDER 🌍\n")
    db_connection = setup_database()
    city_map = None
    active_city_name = ""
    
    saved_cities = get_saved_cities(db_connection)
    
    if saved_cities:
        print("Saved Cities Found:")
        for i, city in enumerate(saved_cities):
            print(f"  {i+1}. {city}")
        print(f"  {len(saved_cities)+1}. Build a NEW city")
        
        choice = input("\nEnter the number of your choice: ").strip()
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(saved_cities):
                active_city_name = saved_cities[choice_idx]
                city_map = load_city_from_db(db_connection, active_city_name)
        except ValueError:
            pass 

    if city_map is None:
        active_city_name = input("\nEnter a name for your NEW city: ").strip()
        city_map = {}
        try:
            num_nodes = int(input(f"How many intersections are in {active_city_name}? "))
            for i in range(num_nodes):
                name = input(f"Name for intersection {i+1}: ").strip()
                x = int(input(f"X coordinate for {name}: "))
                y = int(input(f"Y coordinate for {name}: "))
                city_map[name] = CityNode(name, x, y)
                
            num_roads = int(input("\nHow many roads connect these intersections? "))
            for i in range(num_roads):
                print(f"\nRoad {i+1}:")
                start_node = input("Starts at (exact name): ").strip()
                end_node = input("Ends at (exact name): ").strip()
                time = int(input("Travel time in minutes: "))
                
                if start_node in city_map and end_node in city_map:
                    city_map[start_node].neighbors[city_map[end_node]] = time
                    city_map[end_node].neighbors[city_map[start_node]] = time
                else:
                    print("⚠️ Typo detected! One of those intersections doesn't exist. Road skipped.")
                    
            save_city_to_db(db_connection, active_city_name, city_map)
        except ValueError:
            print("Invalid number entered. Exiting.")
            return

    # --- Run the Emergency Dispatch (Numbered UI) ---
    print(f"\n🚨 --- {active_city_name.upper()} DISPATCH CENTER --- 🚨")
    
    # Create an ordered list of names
    intersection_names = list(city_map.keys())
    print("Available Intersections:")
    for idx, name in enumerate(intersection_names):
        print(f"  {idx + 1}. {name}")
    
    try:
        # Get numerical input from the user and subtract 1 (because Python lists start at 0)
        start_idx = int(input("\nEnter the NUMBER for the ambulance's current location: ").strip()) - 1
        goal_idx = int(input("Enter the NUMBER for the emergency location: ").strip()) - 1
        
        # Check if the numbers entered are actually valid options
        if 0 <= start_idx < len(intersection_names) and 0 <= goal_idx < len(intersection_names):
            start_loc = intersection_names[start_idx]
            goal_loc = intersection_names[goal_idx]
            
            print("\nCalculating optimal route...")
            path, total_time = a_star_search(city_map[start_loc], city_map[goal_loc])
            
            if path is None:
                print("❌ Dispatch Failed: No connected route exists between those locations!")
            else:
                print("\n✅ [Optimal Route Breakdown]")
                
                # Step-by-step route formatting
                route_str = path[0]
                for i in range(len(path) - 1):
                    curr_node = path[i]
                    next_node = path[i+1]
                    segment_time = city_map[curr_node].neighbors[city_map[next_node]]
                    route_str += f" --[{segment_time} min]--> {next_node}"
                
                print(route_str)
                print(f"⏱️ Total Response Time: {total_time} minutes")
        else:
            print("❌ Dispatch Failed: Number chosen is not on the list.")
    except ValueError:
        print("❌ Dispatch Failed: Please enter a valid number, not text.")
        
    db_connection.close()

if __name__ == "__main__":
    main()