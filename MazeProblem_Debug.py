"""
MAZE PROBLEM - DEBUG REŽIMAS
Detalus trasavimas kaip veikia labirinto problema su ta pačia architektūra
"""

from search import *
from MazeProblem import *


def debug_maze_step_by_step():
    """Išsamus žingsnis po žingsnio debugas"""
    
    print("=" * 80)
    print("MAZE PROBLEM - DEBUG REŽIMAS")
    print("Demonstruojame architektūrą Step-by-Step")
    print("=" * 80)
    
    # =========================================================================
    # ŽINGSNIS 1: Problemos Sukūrimas
    # =========================================================================
    print("\n【 ŽINGSNIS 1: Sukuriame MazeProblem objektą 】")
    print("-" * 80)
    
    maze_raw = [
        ['.', '.', '#', '.', '.'],
        ['.', '#', '#', '.', '.'],
        ['.', '.', '.', '#', '.'],
        ['#', '.', '#', '#', '.'],
        ['.', '.', '.', '.', '.']
    ]
    start = (0, 0)
    goal = (4, 4)
    
    print("Labirintas (5x5):")
    for i, row in enumerate(maze_raw):
        print(f"  {i} {''.join(row)}")
    
    print(f"\nPradžia (S): {start}")
    print(f"Tikslas (G): {goal}")
    
    # Sukuriame MazeProblem objektą
    problem = MazeProblem(maze_raw, start, goal)
    
    print(f"\nMazeProblem objektas sukurtas!")
    print(f"  - maze: {problem.rows}x{problem.cols} masyvas")
    print(f"  - initial: {problem.initial}")
    print(f"  - goal: {problem.goal}")
    
    # =========================================================================
    # ŽINGSNIS 2: Node Objekto Kūrimas
    # =========================================================================
    print("\n【 ŽINGSNIS 2: Sukuriame pradinį Node 】")
    print("-" * 80)
    
    root = Node(problem.initial)
    
    print(f"Node: {root}")
    print(f"  - state: {root.state}")
    print(f"  - parent: {root.parent}")
    print(f"  - action: {root.action}")
    print(f"  - path_cost: {root.path_cost}")
    print(f"  - depth: {root.depth}")
    
    # =========================================================================
    # ŽINGSNIS 3: Actions - Galimi Veiksmai
    # =========================================================================
    print("\n【 ŽINGSNIS 3: problem.actions(state) 】")
    print("-" * 80)
    
    current_state = problem.initial
    actions = problem.actions(current_state)
    
    print(f"Dabartinė pozicija: {current_state}")
    print(f"Tai yra eilutė={current_state[0]}, stulpelis={current_state[1]}")
    print(f"\nTikriname kryptis:")
    
    row, col = current_state
    print(f"  UP    (↑): row-1={row-1}, col={col} → ", end="")
    if row > 0 and problem.maze[row-1][col] != '#':
        print(f"✓ '{problem.maze[row-1][col]}' (galima)")
    else:
        print("✗ (siena arba už ribų)")
    
    print(f"  DOWN  (↓): row+1={row+1}, col={col} → ", end="")
    if row < problem.rows-1 and problem.maze[row+1][col] != '#':
        print(f"✓ '{problem.maze[row+1][col]}' (galima)")
    else:
        print("✗ (siena arba už ribų)")
    
    print(f"  LEFT  (←): row={row}, col-1={col-1} → ", end="")
    if col > 0 and problem.maze[row][col-1] != '#':
        print(f"✓ '{problem.maze[row][col-1]}' (galima)")
    else:
        print("✗ (siena arba už ribų)")
    
    print(f"  RIGHT (→): row={row}, col+1={col+1} → ", end="")
    if col < problem.cols-1 and problem.maze[row][col+1] != '#':
        print(f"✓ '{problem.maze[row][col+1]}' (galima)")
    else:
        print("✗ (siena arba už ribų)")
    
    print(f"\nGalimi veiksmai: {actions}")
    
    # =========================================================================
    # ŽINGSNIS 4: Result - Rezultatas Po Veiksmo
    # =========================================================================
    print("\n【 ŽINGSNIS 4: problem.result(state, action) 】")
    print("-" * 80)
    
    for action in actions:
        new_state = problem.result(current_state, action)
        print(f"\nVeiksmas: {action:8} → nauja pozicija: {new_state}")
        print(f"  Labirinte: '{problem.maze[new_state[0]][new_state[1]]}'")
    
    # =========================================================================
    # ŽINGSNIS 5: Node.expand() - Vaikų Generavimas
    # =========================================================================
    print("\n【 ŽINGSNIS 5: root.expand(problem) 】")
    print("-" * 80)
    
    children = root.expand(problem)
    
    print(f"Sugeneruota {len(children)} vaikų mazgų:\n")
    for i, child in enumerate(children, 1):
        print(f"  Vaikas #{i}:")
        print(f"    - action: {child.action}")
        print(f"    - state: {child.state}")
        print(f"    - parent.state: {child.parent.state}")
        print(f"    - depth: {child.depth}")
        print(f"    - path_cost: {child.path_cost}")
    
    # =========================================================================
    # ŽINGSNIS 6: Euristika h(n) - Manhattan Distance
    # =========================================================================
    print("\n【 ŽINGSNIS 6: problem.h(node) - Manhattan Distance 】")
    print("-" * 80)
    
    h_root = problem.h(root)
    print(f"h(root) = {h_root}")
    
    print(f"\nKaip skaičiuojama Manhattan Distance?")
    print(f"  h(n) = |x1 - x2| + |y1 - y2|")
    print(f"\n  Dabartinė pozicija: {root.state}")
    print(f"  Tikslinė pozicija: {problem.goal}")
    print(f"  h = |{root.state[0]} - {problem.goal[0]}| + |{root.state[1]} - {problem.goal[1]}|")
    print(f"  h = {abs(root.state[0] - problem.goal[0])} + {abs(root.state[1] - problem.goal[1])} = {h_root}")
    
    print(f"\nVaikų euristikos:")
    for child in children:
        h_child = problem.h(child)
        print(f"  {child.action:8} → {child.state} → h={h_child}")
    
    # =========================================================================
    # ŽINGSNIS 7: Simuliuojame Best-First Search
    # =========================================================================
    print("\n【 ŽINGSNIS 7: Best-First Search simuliacija 】")
    print("-" * 80)
    
    frontier = PriorityQueue('min', lambda n: problem.h(n))
    frontier.append(root)
    explored = set()
    
    print("PRADŽIA: frontier = [root], explored = {}\n")
    
    max_steps = 8
    step = 0
    
    while frontier and step < max_steps:
        step += 1
        print(f"{'─' * 40}")
        print(f"Žingsnis #{step}")
        print(f"{'─' * 40}")
        
        node = frontier.pop()
        print(f"Pop: state={node.state}, h={problem.h(node)}, depth={node.depth}")
        
        if problem.goal_test(node.state):
            print(">>> TIKSLAS PASIEKTAS! <<<")
            break
        
        explored.add(node.state)
        children = node.expand(problem)
        new_children = [c for c in children if c.state not in explored and c not in frontier]
        
        print(f"Expand: {len(children)} vaikų, {len(new_children)} nauji")
        
        for child in new_children:
            frontier.append(child)
            print(f"  → Append: {child.action} → {child.state}, h={problem.h(child)}")
        
        print(f"Frontier size: {len(frontier)}, Explored: {len(explored)}\n")
    
    # =========================================================================
    # ŽINGSNIS 8: Pilnas Sprendimas
    # =========================================================================
    print("\n【 ŽINGSNIS 8: Pilnas sprendimas su vizualizacija 】")
    print("=" * 80)
    
    problem2 = MazeProblem(maze_raw, start, goal)
    
    # Vizualizuojame pradinį labirintą
    maze_display = [list(row) for row in maze_raw]
    maze_display[start[0]][start[1]] = 'S'
    maze_display[goal[0]][goal[1]] = 'G'
    problem2.maze = maze_display
    
    print("\nPRADINIS LABIRINTAS:")
    problem2.visualize_maze()
    
    # Sprendžiame
    print("\nVykdomas best_first_graph_search...")
    solution_node = best_first_graph_search(problem2, lambda n: problem2.h(n))
    
    if solution_node:
        solution = solution_node.solution()
        path = solution_node.path()
        path_states = [node.state for node in path]
        
        print(f"\n✓ SPRENDIMAS RASTAS!")
        print(f"  Žingsnių: {len(solution)}")
        print(f"  Veiksmų seka: {solution}")
        
        # Vizualizuojame sprendimą
        problem2.visualize_maze(path_states)
        
        # Detalus kelias
        print(f"\n{'─' * 80}")
        print("DETALUS KELIAS:")
        print(f"{'─' * 80}")
        for i, node in enumerate(path):
            action = node.action if node.action else "START"
            h_val = problem2.h(node)
            print(f"  {i}. {action:8} → {node.state}, h={h_val}, cost={node.path_cost}")
    
    # =========================================================================
    # ŽINGSNIS 9: Architektūros Palyginimas su EightPuzzle
    # =========================================================================
    print("\n" + "=" * 80)
    print("【 ŽINGSNIS 9: ARCHITEKTŪROS PALYGINIMAS 】")
    print("=" * 80)
    
    print("""
┌───────────────────┬─────────────────────────┬─────────────────────────┐
│   Komponentas     │      EightPuzzle        │       MazeProblem       │
├───────────────────┼─────────────────────────┼─────────────────────────┤
│ Bazinė klasė      │ Problem                 │ Problem (same!)         │
├───────────────────┼─────────────────────────┼─────────────────────────┤
│ State             │ tuple 9 skaičių         │ tuple (row, col)        │
│                   │ (2,4,3,1,5,6,7,8,0)     │ (0, 0)                  │
├───────────────────┼─────────────────────────┼─────────────────────────┤
│ actions(state)    │ UP/DOWN/LEFT/RIGHT      │ UP/DOWN/LEFT/RIGHT      │
│                   │ tikrina lentos ribas    │ tikrina sienas          │
├───────────────────┼─────────────────────────┼─────────────────────────┤
│ result(state,act) │ apsikeičia plokštelėmis │ juda į naują poziciją   │
├───────────────────┼─────────────────────────┼─────────────────────────┤
│ goal_test(state)  │ state == goal           │ state == goal (same!)   │
├───────────────────┼─────────────────────────┼─────────────────────────┤
│ h(node)           │ misplaced tiles         │ Manhattan distance      │
│                   │ (netaisyklingų skaičius)│ (|x1-x2| + |y1-y2|)    │
├───────────────────┼─────────────────────────┼─────────────────────────┤
│ Node              │ Tas pats objektas       │ Tas pats objektas!      │
├───────────────────┼─────────────────────────┼─────────────────────────┤
│ Algoritmai        │ breadth_first, best_first, A*, depth_first        │
│                   │ ▲▲▲ UNIVERSALŪS - veikia su ABIEM problemomis! ▲▲▲│
└───────────────────┴───────────────────────────────────────────────────┘

PAGRINDINĖ IDĖJA:
  • Ta pati architektūra
  • Tie patys algoritmai
  • Skiriasi tik PROBLEMOS SPECIFIKA (kaip reprezentuojame būseną)
  • Modular Design - galime lengvai kurti naujas problemas!
    """)
    
    print("=" * 80)
    print("DEBUG PABAIGA")
    print("=" * 80)


if __name__ == "__main__":
    debug_maze_step_by_step()
