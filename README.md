# Warehouse-Robot-Navigation-AI
# Intelligent Warehouse Robot Navigation
**CS F407 – Artificial Intelligence | Group Assignment (D3 Implementation)**  

**Group Number:** 22  
**Project:** Intelligent Warehouse Robot Navigation    

---

## Team Members

| Name | ID |
|------|----|
| Hitansh Chadha | 2022A8PS1255P |
| Vedant Mathur | 2022A3PS0375P |
| Krishna Raghunath | 2023A1PS0213P |

---

## Setup Instructions
### Install pygame using the command:
`pip install pygame`
then run `main.py` file

---
## Project Overview

This project focuses on designing and implementing an **intelligent search-based agent** for autonomous navigation in a warehouse environment. The robot must navigate a grid-based warehouse, collect items, manage energy constraints, and reach delivery points while avoiding static obstacles.
 
**Complexity Level Implemented:** L3  

---

## Problem Description

The warehouse is modeled as a **fully observable, deterministic, static, discrete, single-agent environment**.

- The environment is a 2D grid with obstacles and collectible items  
- The robot starts from a known initial position  
- Items must be collected and delivered efficiently  
- Higher complexity levels introduce energy constraints and item priorities  

### State Representation
---

## Implemented Complexity Levels

| Level | Description | Algorithm(s) Used |
|------|------------|------------------|
| **L1** | Single item pickup, static obstacles | BFS |
| **L2** | Multiple items, minimum path cost | UCS |
| **L3** | Energy constraints and weighted item priorities | A*, IDA* |

---

## Algorithms Implemented

In accordance with **D2 (Algorithm Analysis)** and **D3 (Implementation)** requirements, the following algorithms were implemented from scratch.

### Uninformed Search Algorithms

#### 1. Breadth-First Search (BFS)
- Used in **L1**
- Guarantees shortest path in an unweighted grid
- Complete and optimal for uniform cost environments

#### 2. Uniform Cost Search (UCS)
- Used in **L2**
- Expands the lowest path-cost node first
- Guarantees optimal solution with weighted step costs

---

### Informed Search Algorithms

#### 3. A* Search
- Used in **L3**
- Combines path cost with heuristic guidance
- More efficient than UCS due to heuristic pruning

#### 4. Iterative Deepening A* (IDA*)
- Used in **L3**
- Memory-efficient alternative to A*
- Suitable for larger state spaces with limited memory

---

## Heuristics (Designed in D1)

Two admissible and consistent heuristics were formally designed and proved in **D1**, then implemented in **D3**.

### 1️⃣ Manhattan Distance Heuristic (for A*)

h(n) = |x₁ − x₂| + |y₁ − y₂|
- Admissible 
- Consistent 
- Suitable for grid-based movement with four-directional actions

### 2️⃣ Minimum Spanning Tree (MST) Heuristic (for IDA*)

h(n) = Cost of MST over remaining uncollected items
- Models a relaxed version of the problem
- Admissible 
- Consistent 
- More informed for multi-item collection tasks

---

## System Architecture


Grid Input
↓
Search Engine
(BFS / UCS / A* / IDA*)
↓
State Transition & Cost Evaluation
↓
Path Generation
↓
Visualization Layer

- Implemented in **Python 3**
- Modular search engine design
- Visualization using **Pygame**
- Easy comparison of algorithms and heuristics

---



