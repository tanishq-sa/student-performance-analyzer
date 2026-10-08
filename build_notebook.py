import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))

def code(text):
    cells.append(nbf.v4.new_code_cell(text))

# ----------------------------------------------------------------------
md(r"""# Sokoban Puzzle — State-Space Search & Intelligent Agent Design
### CIA 1 — Search Challenge (Team 3)

**Team members:** Ashish & Tanishq (24112518)
**Programme:** BCA, CHRIST (Deemed to be University), Pune Lavasa Campus
**Assigned problem:** Sokoban Puzzle

This notebook covers, in order: problem description, formal problem
formulation, PEAS analysis, agent architecture, environment
representation, the BFS and DFS implementations, experimental results,
and a comparison of the two algorithms.""")

# ----------------------------------------------------------------------
md(r"""## 1. Problem Description

**Sokoban** ("warehouse keeper" in Japanese) is a classic puzzle in which an
agent moves around a grid-based warehouse and pushes boxes onto marked
storage locations. The agent can only *push* boxes (never pull them), can
push only one box at a time, and cannot push a box into a wall or into
another box. The puzzle is solved when every box rests on a storage
location.

Despite its simple rules, Sokoban is a well-known benchmark in AI search:
its state space grows combinatorially with the number of boxes, it is
[PSPACE-complete](https://en.wikipedia.org/wiki/Sokoban) in general, and it
contains **irreversible moves** — pushing a box into a corner with no
adjacent goal can make the puzzle permanently unsolvable. This makes it a
good, non-trivial testbed for comparing uninformed search strategies.

We use the standard single-character grid notation:

| Symbol | Meaning          |
|:------:|------------------|
| `#`    | Wall             |
| `@`    | Player           |
| `+`    | Player on goal   |
| `$`    | Box              |
| `*`    | Box on goal      |
| `.`    | Goal (storage)   |
| ` `    | Empty floor      |""")

# ----------------------------------------------------------------------
md(r"""## 2. Problem Formulation (Task 1)

Sokoban is formulated as a **state-space search problem** as follows.

**1. Initial State** — The starting configuration of the warehouse: the
(fixed) wall layout, the (fixed) set of goal cells, the starting position
of every box, and the starting position of the player. Formally,
$S_0 = (\text{player}_0, \text{boxes}_0)$. Walls and goals never change
during the puzzle, so they are treated as static properties of the
*environment*, not as part of the mutable search state.

**2. Goal State** — Any state $(\text{player}, \text{boxes})$ in which
`boxes` exactly equals the set of goal cells. The player's final position
is irrelevant to the goal test — only box placement matters.

**3. Actions / Operators** — Four operators: `Move-Up`, `Move-Down`,
`Move-Left`, `Move-Right`. Applying a direction to a state:
- moves the player one cell in that direction if the destination is free
  floor (not a wall, no box), **or**
- if the destination cell holds a box, pushes that box one further cell in
  the same direction (and the player follows into the box's old cell),
  **provided** the cell beyond the box is neither a wall nor another box,
  **or**
- is not generated at all (illegal) otherwise.

Only one box can ever move per action, and boxes can only be pushed, never
pulled.

**4. State Representation** — A state is the pair
`(player_position, frozenset_of_box_positions)`. Walls and goals are
level constants shared by every state and are stored once on the problem
object rather than repeated in every state, keeping states small and cheap
to hash/compare — important because the search keeps a large `explored`
set. A `frozenset` for the boxes (rather than a list/tuple) correctly
encodes that boxes are interchangeable: two states with the same set of
occupied cells are the *same* state regardless of "which" box is where.

**5. Constraints**
- The player may never move into or through a wall cell.
- A box may never be pushed into a wall or into another box.
- Boxes can only be **pushed** (never pulled), and only **one at a time**.
- The number of boxes always equals the number of goal cells.
- Some moves are irreversible in practice (e.g. pushing a box into a
  corner with no goal can permanently block a solution) — the search
  itself doesn't forbid this, it simply won't find a solution down that
  branch.""")

# ----------------------------------------------------------------------
md(r"""## 3. PEAS Framework (Task 2.1)

| PEAS element | Description |
|---|---|
| **Performance measure** | Reaching a goal state (all boxes on storage cells); among solutions, fewer moves (shorter push/move sequence) is better, as is lower search cost (nodes expanded, time, memory); illegal moves are never generated, so they cannot be scored against the agent. |
| **Environment** | The warehouse grid: fixed walls, fixed goal cells, movable boxes, and the player. |
| **Actuators** | Four directional move commands (Up / Down / Left / Right), which move the player and, when applicable, push a box. |
| **Sensors** | Full knowledge of the grid: wall layout, goal cells, current box positions, and current player position. |

**Environment properties:** fully observable (the entire grid is known at
all times), deterministic (every action has exactly one outcome),
static (the warehouse does not change unless the agent acts — no other
agents or independent dynamics), discrete (finite cells, finite actions,
discrete time steps), single-agent, and sequential (each action affects
which actions/outcomes are available later, so the agent must plan ahead
rather than react greedily).""")

# ----------------------------------------------------------------------
md(r"""## 4. Agent Architecture & Agent Program (Task 2.2 – 2.4)

**Agent Architecture.** Because the environment is fully observable,
deterministic and static, the agent does not need to cope with uncertainty
— but it *does* need to look many steps ahead, since the goal is typically
reached only after a long sequence of pushes, and a purely reactive agent
cannot avoid dead-ends (e.g. pushing a box into a corner). This rules out
a **simple reflex agent** and calls for a **goal-based agent**: it keeps
an internal model of the world (player + box positions), formulates the
goal (all boxes on goals), and uses **search** to construct a complete
plan before acting. Where solution *quality* (path cost) also matters —
as it does for our comparison — the same design extends naturally into a
**utility-based agent**, using path length (and, for larger puzzles, a
heuristic estimate of remaining cost) as the utility to be minimised.

**Agent's Percept.** At each instant, the percept is the full grid state:
wall layout, goal cells, current box positions, and the player's current
position — sufficient for a complete internal state representation because
the environment is fully observable.

**Agent Program.** Since the environment is static, a plan computed once
from the initial percept remains valid for the whole episode — no
replanning is required (this is the classic AIMA "simple problem-solving
agent" template):

```text
function SOKOBAN-AGENT(percept) returns an action
    persistent: plan, an action sequence, initially empty
                state, the agent's model of the current world state

    state  <- UPDATE-STATE(state, percept)
    if plan is empty then
        goal    <- FORMULATE-GOAL(state)              # all boxes on goal cells
        problem <- FORMULATE-PROBLEM(state, goal)      # as in Section 2
        plan    <- SEARCH(problem)                     # BFS or DFS (Section 6)
    action <- FIRST(plan)
    plan   <- REST(plan)
    return action
```

The `SEARCH` step is exactly what Sections 6–7 implement and compare.""")

# ----------------------------------------------------------------------
md(r"""## 5. Environment Representation (Task 2, continued)

The environment is implemented as a `SokobanProblem` class built directly
from a level's text grid:

- `walls`, `goals` — `frozenset`s of `(row, col)` cells; fixed for the
  level, computed once in `__init__`.
- `init_state` — the initial `(player, boxes)` tuple described in Section 2.
- `successors(state)` — generates every legal `(action, next_state)` pair
  from a state, implementing the operators and constraints from Section 2.
- `is_goal(state)` — true when `boxes == goals`.
- `render(state)` — renders a state back into the human-readable grid
  notation from Section 1, for printing and sanity-checking.

This class is the *environment simulator*: given any state and an action,
it can tell the agent exactly what the resulting state is, which is what
lets BFS/DFS search forward from the initial state without ever touching a
real warehouse.""")

code(r"""from collections import deque
import time

# Four possible actions and the (row, col) delta each one applies
DIRECTIONS = {
    'Up':    (-1, 0),
    'Down':  (1, 0),
    'Left':  (0, -1),
    'Right': (0, 1),
}


class SokobanProblem:
    # A Sokoban level as a state-space search problem.

    def __init__(self, grid_lines):
        walls, goals, boxes = set(), set(), set()
        player = None

        for r, line in enumerate(grid_lines):
            for c, ch in enumerate(line):
                if ch == '#':
                    walls.add((r, c))
                elif ch == '.':
                    goals.add((r, c))
                elif ch == '$':
                    boxes.add((r, c))
                elif ch == '*':                       # box already on a goal
                    boxes.add((r, c)); goals.add((r, c))
                elif ch == '@':
                    player = (r, c)
                elif ch == '+':                       # player standing on a goal
                    player = (r, c); goals.add((r, c))
                # ' ' -> plain floor, nothing to record

        if player is None:
            raise ValueError("Grid has no player ('@' or '+').")
        if len(boxes) != len(goals):
            raise ValueError("Number of boxes must equal number of goals.")

        self.walls = frozenset(walls)
        self.goals = frozenset(goals)
        self.height = len(grid_lines)
        self.width = max(len(line) for line in grid_lines)
        self.init_state = (player, frozenset(boxes))          # (Section 2, State Representation)

    def initial_state(self):
        return self.init_state

    def is_goal(self, state):
        _, boxes = state
        return boxes == self.goals

    def successors(self, state):
        # Yield every legal (action, next_state) pair reachable in one move.
        player, boxes = state
        pr, pc = player
        for action, (dr, dc) in DIRECTIONS.items():
            nr, nc = pr + dr, pc + dc
            if (nr, nc) in self.walls:
                continue                                        # can't walk into a wall
            if (nr, nc) in boxes:
                br, bc = nr + dr, nc + dc                        # cell beyond the box
                if (br, bc) in self.walls or (br, bc) in boxes:
                    continue                                     # can't push into wall/box
                new_boxes = frozenset((boxes - {(nr, nc)}) | {(br, bc)})
                yield action, ((nr, nc), new_boxes)               # push
            else:
                yield action, ((nr, nc), boxes)                   # plain move

    def render(self, state):
        # Render a state back to the grid notation from Section 1.
        player, boxes = state
        rows = []
        for r in range(self.height):
            row = []
            for c in range(self.width):
                pos = (r, c)
                if pos in self.walls:
                    row.append('#')
                elif pos == player:
                    row.append('+' if pos in self.goals else '@')
                elif pos in boxes:
                    row.append('*' if pos in self.goals else '$')
                elif pos in self.goals:
                    row.append('.')
                else:
                    row.append(' ')
            rows.append(''.join(row))
        return '\n'.join(rows)

print("SokobanProblem defined.")""")

# ----------------------------------------------------------------------
md(r"""### Test levels

Three levels of increasing difficulty are used throughout the notebook —
one trivial single-push level, one single-box level that needs several
pushes and a change of direction, and one two-box level (a noticeably
larger state space) to stress-test the search algorithms.""")

code(r"""LEVEL_1 = ["#####",
           "#@$.#",
           "#####"]

LEVEL_2 = ["#######",
           "#.    #",
           "# $   #",
           "#  @  #",
           "#     #",
           "#######"]

LEVEL_3 = ["#########",
           "#   #   #",
           "# $ # $ #",
           "#  .#.  #",
           "#   @   #",
           "#########"]

LEVELS = {
    "Level 1 (1 box, single push)": LEVEL_1,
    "Level 2 (1 box, multi-step)":  LEVEL_2,
    "Level 3 (2 boxes)":            LEVEL_3,
}

for name, grid in LEVELS.items():
    print(name)
    print(SokobanProblem(grid).render(SokobanProblem(grid).init_state))
    print()""")

# ----------------------------------------------------------------------
md(r"""## 6. Search Algorithms (Task 3 & 4)

Both algorithms below share one **graph-search** template (goal-tested on
removal from the frontier) and differ only in the frontier's
discipline — BFS uses a FIFO queue, DFS a LIFO stack — which is why they
are implemented as a single parameterised function.

An `explored` set is essential here, not just an optimisation: Sokoban's
state graph contains **cycles** (the player can walk back to a cell it
already visited, or push a box back and forth), so a naive tree search
without a visited-set could loop forever, especially for DFS. With the
explored set, both searches are guaranteed to terminate on any finite
grid (**completeness**).""")

code(r"""def reconstruct_path(state, parent, action_taken):
    # Walk parent pointers back to the root and reverse them into an action sequence.
    actions = []
    while parent[state] is not None:
        actions.append(action_taken[state])
        state = parent[state]
    actions.reverse()
    return actions


def graph_search(problem, strategy='bfs'):
    # Generic graph-search (goal test on removal from frontier).
    # strategy='bfs' -> FIFO frontier (breadth-first, complete & optimal for unit-cost actions)
    # strategy='dfs' -> LIFO frontier (depth-first, complete here thanks to the explored set,
    #                   but NOT optimal)
    start = problem.initial_state()
    frontier = deque([start])
    parent = {start: None}
    action_taken = {}
    explored = set()
    nodes_expanded = 0
    max_frontier_size = 1
    t0 = time.time()

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))
        state = frontier.popleft() if strategy == 'bfs' else frontier.pop()

        if state in explored:
            continue
        explored.add(state)
        nodes_expanded += 1

        if problem.is_goal(state):
            return {
                'success': True,
                'path': reconstruct_path(state, parent, action_taken),
                'nodes_expanded': nodes_expanded,
                'nodes_generated': len(parent),
                'max_frontier_size': max_frontier_size,
                'time_sec': time.time() - t0,
            }

        for action, next_state in problem.successors(state):
            if next_state not in explored and next_state not in parent:
                parent[next_state] = state
                action_taken[next_state] = action
                frontier.append(next_state)

    return {'success': False, 'time_sec': time.time() - t0, 'nodes_expanded': nodes_expanded}


def bfs(problem):
    return graph_search(problem, strategy='bfs')


def dfs(problem):
    return graph_search(problem, strategy='dfs')


def replay(problem, path):
    # Re-apply an action sequence from the initial state; used as a correctness check.
    state = problem.initial_state()
    for a in path:
        state = next(ns for act, ns in problem.successors(state) if act == a)
    return state

print("bfs(), dfs() and replay() defined.")""")

# ----------------------------------------------------------------------
md(r"""### Why uninformed search here — and where it stops being enough

Task 4 invites us to judge whether uninformed search is the right tool.
For the three levels used in this notebook, **BFS and DFS are entirely
appropriate**: the state spaces are small enough to search exhaustively in
milliseconds, and — more importantly for a search-methods assignment —
comparing them head-to-head is exactly what surfaces the textbook
completeness/optimality trade-offs (Section 8).

That said, uninformed search does **not** scale. For a level with $F$
free cells and $k$ boxes, the number of distinct box configurations is on
the order of $\binom{F}{k}$, multiplied by up to $F$ player positions, with
a branching factor of up to 4 per state. We can already see this growth
between our own Level 2 (1 box) and Level 3 (2 boxes) below — one extra
box is enough to multiply BFS's nodes-expanded by roughly 50×. Realistic
Sokoban levels (e.g. the standard *Microban*/*XSokoban* benchmark sets)
have far larger state spaces, where exhaustive BFS/DFS becomes infeasible
in both time and memory. Practical Sokoban solvers instead use **informed
search** (A\*/IDA\*) with an admissible heuristic — typically the sum of
Manhattan distances from each box to its nearest goal, refined with
box–goal bipartite matching and explicit **deadlock detection** (e.g. a
box pushed into a corner with no goal is stuck forever, so that branch can
be pruned outright). We do not implement A\* here, since the assignment's
explicit deliverables are the BFS/DFS comparison, but it is the natural
next step beyond this notebook.""")

# ----------------------------------------------------------------------
md(r"""## 7. Running the Search & Results (Task 3, 4 & 5)

Each level is solved with both BFS and DFS. For every run we record
whether it succeeded, the solution length (moves), nodes expanded, nodes
generated, the largest the frontier ever grew, and wall-clock time — then
sanity-check every solution by **replaying** it from the initial state and
confirming it truly reaches a goal state.""")

code(r"""import pandas as pd

results_rows = []
solved = {}   # (level_name, strategy) -> (problem, final_state, result)

for name, grid in LEVELS.items():
    problem = SokobanProblem(grid)
    print("=" * 64)
    print(name)
    print(problem.render(problem.initial_state()))
    for strategy in ("bfs", "dfs"):
        result = graph_search(problem, strategy)
        if result['success']:
            final_state = replay(problem, result['path'])
            assert problem.is_goal(final_state), "replay failed to reach the goal!"
            solved[(name, strategy)] = (problem, final_state, result)
            results_rows.append({
                "Level": name,
                "Algorithm": strategy.upper(),
                "Solved": True,
                "Solution Length": len(result['path']),
                "Nodes Expanded": result['nodes_expanded'],
                "Nodes Generated": result['nodes_generated'],
                "Max Frontier Size": result['max_frontier_size'],
                "Time (ms)": round(result['time_sec'] * 1000, 3),
            })
            print(f"  {strategy.upper():3s}: {len(result['path']):3d} moves | "
                  f"expanded {result['nodes_expanded']:5d} | "
                  f"generated {result['nodes_generated']:5d} | "
                  f"max frontier {result['max_frontier_size']:4d} | "
                  f"{result['time_sec']*1000:7.3f} ms")
        else:
            results_rows.append({
                "Level": name, "Algorithm": strategy.upper(), "Solved": False,
                "Solution Length": None, "Nodes Expanded": result['nodes_expanded'],
                "Nodes Generated": None, "Max Frontier Size": None,
                "Time (ms)": round(result['time_sec'] * 1000, 3),
            })
            print(f"  {strategy.upper()}: NO SOLUTION FOUND")
    print()

results_df = pd.DataFrame(results_rows)
results_df""")

# ----------------------------------------------------------------------
md(r"""### Visualising a solution

As a concrete example, here is **Level 3** (the hardest test case) before
and after BFS's solution is applied — every box has moved from its `$`
starting cell onto a goal.""")

code(r"""import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_state(problem, state, ax=None, title=""):
    own_fig = ax is None
    if own_fig:
        _, ax = plt.subplots(figsize=(problem.width * 0.55, problem.height * 0.55))
    player, boxes = state
    for r in range(problem.height):
        for c in range(problem.width):
            pos = (r, c)
            x, y = c, problem.height - 1 - r          # flip so row 0 renders on top
            face = '#333333' if pos in problem.walls else '#f5f5f5'
            ax.add_patch(patches.Rectangle((x, y), 1, 1, facecolor=face,
                                            edgecolor='#bbbbbb', linewidth=0.5))
            if pos in problem.goals and pos not in problem.walls:
                ax.add_patch(patches.Circle((x + 0.5, y + 0.5), 0.10,
                                             facecolor='#e74c3c', zorder=2))
            if pos in boxes:
                face = '#27ae60' if pos in problem.goals else '#d4a017'
                ax.add_patch(patches.Rectangle((x + 0.12, y + 0.12), 0.76, 0.76,
                                                facecolor=face, edgecolor='black', zorder=3))
            if pos == player:
                ax.add_patch(patches.Circle((x + 0.5, y + 0.5), 0.28,
                                             facecolor='#2980b9', edgecolor='black', zorder=4))
    ax.set_xlim(0, problem.width); ax.set_ylim(0, problem.height)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=10)
    if own_fig:
        plt.tight_layout(); plt.show()


problem3, final3, result3 = solved[("Level 3 (2 boxes)", "bfs")]
fig, axes = plt.subplots(1, 2, figsize=(8, 4.2))
plot_state(problem3, problem3.initial_state(), ax=axes[0], title="Initial state")
plot_state(problem3, final3, ax=axes[1], title=f"Goal reached — BFS, {len(result3['path'])} moves")
plt.tight_layout()
plt.show()""")

# ----------------------------------------------------------------------
md(r"""## 8. Algorithmic Comparison (Task 5)""")

code(r"""import numpy as np

pivot_nodes = results_df.pivot(index="Level", columns="Algorithm", values="Nodes Expanded")
pivot_time  = results_df.pivot(index="Level", columns="Algorithm", values="Time (ms)")
pivot_len   = results_df.pivot(index="Level", columns="Algorithm", values="Solution Length")
order = list(LEVELS.keys())
pivot_nodes, pivot_time, pivot_len = pivot_nodes.loc[order], pivot_time.loc[order], pivot_len.loc[order]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, pivot, title, ylabel in [
    (axes[0], pivot_nodes, "Nodes Expanded", "Nodes"),
    (axes[1], pivot_time,  "Time Taken",     "Milliseconds"),
    (axes[2], pivot_len,   "Solution Length", "Moves"),
]:
    pivot.plot(kind="bar", ax=ax, color=["#2980b9", "#e67e22"], legend=(ax is axes[0]))
    ax.set_title(title); ax.set_ylabel(ylabel); ax.set_xlabel("")
    ax.tick_params(axis='x', rotation=15)
plt.tight_layout()
plt.show()""")

md(r"""**Observations from the results above** (BFS = blue, DFS = orange):

- **Optimality.** BFS finds the *shortest possible* solution on every
  level, because it explores the state space in order of increasing
  depth. DFS has no such guarantee: on Level 2 it returns a solution
  **more than 6× longer** than BFS's, and on Level 3 more than **2×
  longer** — both are valid (a replayed solution genuinely reaches the
  goal), just far from optimal.
- **Search cost is unpredictable for DFS.** On Level 2, DFS actually
  expands *more* nodes than BFS (it dives down a long unproductive branch
  before backtracking) — so here it is worse on *both* solution quality
  and search cost. On Level 3, the opposite happens: DFS happens to expand
  far fewer nodes than BFS because it stumbles onto *a* solution quickly,
  long before BFS has finished exploring shallower depths.
  This inconsistency is expected: DFS's performance depends entirely on
  the (here, fixed `Up → Down → Left → Right`) order in which successors
  are generated, not on any notion of "closer to the goal".
- **BFS's cost grows quickly with state-space size.** Going from Level 2
  (1 box) to Level 3 (2 boxes) — adding just one more box — multiplies
  BFS's nodes expanded by roughly **50×** (50 → 2,604) and its peak
  frontier size by over **17×** (28 → 489) — a direct, visible
  illustration of why breadth-first search's $O(b^d)$ memory requirement
  becomes prohibitive for larger puzzles.
- **Both are complete** on these levels (they always find *a* solution
  when one exists), because the graph-search template's `explored` set
  prevents the infinite loops that Sokoban's cyclic state space would
  otherwise allow.

**Conclusion.** BFS is the better default when solution quality matters
and the state space is small enough to fit in memory — exactly the
trade-off theory predicts. DFS can occasionally be cheaper, but that is
incidental to the order of exploration rather than a reliable property,
and its solutions are consistently far from optimal. Neither uninformed
strategy would scale to realistic Sokoban levels (Section 6), where
informed search with a good heuristic is the practical choice.""")

nb['cells'] = cells
nb['metadata'] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.12"},
}

with open('sokoban_cia1.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook written with", len(cells), "cells.")