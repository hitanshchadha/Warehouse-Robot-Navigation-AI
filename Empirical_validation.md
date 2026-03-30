# Empirical Validation: Theoretical vs. Practical Performance

## 1. Theoretical Predictions (D2 Recap)
Based on standard algorithm analysis, the expected complexities for our search algorithms in a grid-based state space were:

* **Breadth-First Search (BFS):** Time and Space complexity of $O(b^d)$, where branching factor $b \le 4$.
* **Uniform Cost Search (UCS):** Time and Space complexity of $O(b^{1 + \lfloor C^*/\epsilon \rfloor})$. Expected to explore a massive number of nodes in L2 due to multiple target items.
* **A* Search:** Time complexity dependent on heuristic quality, optimally $O(b^d)$ worst-case, but practically much lower. Space complexity bounded by $O(b^d)$ due to maintaining the priority queue (Open list).
* **Iterative Deepening A* (IDA*):** Time complexity similar to A* but often higher due to node re-expansions. Space complexity is expected to be strictly linear $O(b \times d)$ representing the depth stack.

## 2. Empirical Observations (D3 Results)
When running the implementation across Easy, Medium, and Hard test cases, we observed the following practical behaviors:

* **BFS (L1):** Explored uniformly in a radius. The node expansion count stopped growing exponentially very early and instead grew quadratically in relation to the grid dimensions.
* **UCS (L2):** In multi-item cases (e.g., the Medium case with 2 items and Hard with 3 items), the node expansion count was significantly larger than BFS. The search spread widely in multiple directions simultaneously.
* **A* (L3):** Using the **Max Priority Item Manhattan** heuristic, the algorithm highly directed its search. Compared to an uninformed algorithm in L3 constraints, the total expanded nodes were drastically reduced.
* **IDA* (L3):** Using the **MST Heuristic**, IDA* maintained an extremely low memory footprint. However, the time taken and total node expansions were noticeably higher on the Hard testcase compared to A* due to the cost boundaries constantly triggering restarts when hitting battery or cost limits.

## 3. Comparative Analysis: Do Node Counts Match Complexity Analysis?

For the most part, the empirical node counts align with the theoretical behavior, but there are distinct differences between "Tree Search" theoretical complexity and our "Graph Search" implementation:

### A. The Bounded Grid Effect (BFS & UCS)
* Pure complexity analysis predicts $O(4^d)$ node expansions. However, our actual node count is strictly bounded by the state space representation. 
* Because we implemented an `explored` set tracking the state `(curr_pos, coll)` (in UCS) and `(current_pos, has_item)` (in BFS), duplicate paths are aggressively pruned. Thus, the practical maximum node expansion is bounded by $O(V \times 2^k)$, where $V$ is the number of valid grid cells and $k$ is the number of uncollected items. The empirical node counts are therefore much lower than $O(b^d)$ predictions.

### B. State Space Explosion in L2/L3 vs L1
* We predicted UCS and A* would take longer on multi-item maps. This perfectly matched empirical results.
* As items ($k$) increase, the $2^k$ multiplier in our state tuple `((x,y), frozenset(collected_items))` causes the state space to multiply. A cell `(4,4)` explored with 0 items is treated as an entirely different node than `(4,4)` explored with 1 item. The empirical node count perfectly reflects this exponential subset scaling.

### C. A* Pruning vs. IDA* Re-expansions
* IDA* was predicted to use less memory but expand more nodes overall. This was directly validated in our code.
* In `astar.py`, the state is checked against `best_state_battery` to prune suboptimal paths immediately. In `idastar.py`, when a path's $f\text{-cost}$ exceeds the `current_bound` (which initially starts as the MST heuristic cost), the branch terminates and restarts with a new bound. Consequently, shallow nodes in the IDA* grid are explored multiple times across different boundary iterations, making its expansion count higher than A*, even though its queue structure (recursion stack) is drastically smaller.

## 4. Conclusion
The node counts and algorithmic behavior in the implementation strongly corroborate the theoretical D2 analysis, with the primary differences stemming from graph-search cycle checking (memoization via dictionaries/sets) and the physical limits introduced by the battery constraints. The implementation successfully demonstrates the space-time tradeoffs between A* (faster, memory-heavy) and IDA* (slower due to re-expansions, memory-efficient).
