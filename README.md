# 🚑 Smart City Emergency Dispatcher

An intelligent **Problem-Solving Agent** designed to optimize ambulance routing in dynamic urban environments. This project integrates classical **AI Search Strategies** with a persistent **SQL Database** to minimize emergency response times.

---

## 📖 Project Overview

This system models a city as a **State Space** where intersections are nodes and roads are weighted edges. It uses the **A* (A-Star) Search Algorithm** to find the most "rational" path between a starting ambulance location and an emergency site.

* **Informed Search:** Utilizes the $A^*$ algorithm with a **Manhattan Distance Heuristic** ($h(n)$) to prioritize the search direction.
* **Dynamic Environments:** Capable of recalculating routes when "costs" (traffic congestion) change.
* **Knowledge Representation:** Uses an **SQLite** relational database to store and categorize multiple city maps.
* **Utility-Based Agent:** Aims to maximize the utility of "Time Saved" by balancing path length against real-time traffic data.

---

## 🛠️ Features

* **Multi-City Storage:** Save and load multiple distinct city maps (e.g., Bhopal, Delhi) from a single database.
* **Numbered Selection UI:** High-speed Command Line Interface (CLI) that replaces manual typing with numerical selection for error-free dispatching.
* **Detailed Route Analysis:** Provides a step-by-step breakdown of travel time for every segment of the journey.
* **Persistent Memory:** Local storage in `smart_city.db` ensures data persists across sessions.

---

## 🚀 Getting Started

* **Prerequisites:** Python 3.x installed. (Uses built-in `sqlite3` and `heapq`).
* **Installation:** Open your terminal or VS Code in the project folder.
* **Execution:** Run the script using the command: `python routing_engine.py`

---

## 🕹️ How to Use

* **City Selection:** Upon launch, choose a saved city from the numbered list or select the option to **Build a NEW city**.
* **Building a City:** Enter the city name, define intersections with (X, Y) coordinates, and link them with travel times.
* **Emergency Dispatch:** Select the starting ambulance location and the emergency site by their corresponding numbers.
* **Review Results:** The agent calculates the $A^*$ optimal path and displays a breakdown: `Hospital --[5 min]--> Main St --[4 min]--> Crash Site`.

---

## 🏗️ Architecture

* **Search Layer:** $A^*$ implementation and `CityNode` logic handling the core pathfinding.
* **Persistence Layer:** SQLite operations for multi-city data management and storage.
* **Interface Layer:** Interactive numbered CLI for user input and route visualization.
