"""
MAZE PROBLEM - Labirinto Paieškos Uždavinys
Naudoja tą pačią architektūrą kaip EightPuzzle

Tikslas: Rasti kelią nuo Start (S) iki Goal (G) labirinte
Kliūtys žymimos '#', laisvi keliai '.'
"""

from search import *
import numpy as np


class MazeProblem(Problem):
    """
    Labirinto problemos klasė.
    Paveldėta iš Problem bazinės klasės - tokia pati architektūra kaip EightPuzzle!
    
    Būsena (state): tuple (row, col) - dabartinė pozicija labirinte
    """
    
    def __init__(self, maze, initial, goal):
        """
        Inicializuoja labirinto problemą
        
        Args:
            maze: 2D masyvas su labirinto struktūra
                  '.' = laisvas kelias
                  '#' = siena
                  'S' = start
                  'G' = goal
            initial: tuple (row, col) - pradinė pozicija
            goal: tuple (row, col) - tikslinė pozicija
        """
        super().__init__(initial, goal)
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if maze else 0
        
    def actions(self, state):
        """
        Grąžina galimus veiksmus iš dabartinės pozicijos.
        Galima judėti 4 kryptimis: UP, DOWN, LEFT, RIGHT
        
        Similar to EightPuzzle.actions() - bet čia tikriname sienas!
        """
        possible_actions = []
        row, col = state
        
        # UP - į viršų
        if row > 0 and self.maze[row - 1][col] != '#':
            possible_actions.append('UP')
        
        # DOWN - į apačią
        if row < self.rows - 1 and self.maze[row + 1][col] != '#':
            possible_actions.append('DOWN')
        
        # LEFT - į kairę
        if col > 0 and self.maze[row][col - 1] != '#':
            possible_actions.append('LEFT')
        
        # RIGHT - į dešinę
        if col < self.cols - 1 and self.maze[row][col + 1] != '#':
            possible_actions.append('RIGHT')
        
        return possible_actions
    
    def result(self, state, action):
        """
        Grąžina naują būseną po veiksmo atlikimo.
        
        Similar to EightPuzzle.result() - bet dabar judame pozicijoje!
        """
        row, col = state
        
        if action == 'UP':
            return (row - 1, col)
        elif action == 'DOWN':
            return (row + 1, col)
        elif action == 'LEFT':
            return (row, col - 1)
        elif action == 'RIGHT':
            return (row, col + 1)
        else:
            return state
    
    def goal_test(self, state):
        """
        Patikrina ar pasiekėme tikslą.
        
        Same as EightPuzzle.goal_test()
        """
        return state == self.goal
    
    def h(self, node):
        """
        Euristinė funkcija - Manhattan distance.
        
        Similar to EightPuzzle.h() - bet naudojame Manhattan distance!
        
        Manhattan distance = |x1 - x2| + |y1 - y2|
        Tai optimali euristika labirintams (admissible)
        """
        row1, col1 = node.state
        row2, col2 = self.goal
        return abs(row1 - row2) + abs(col1 - col2)
    
    def visualize_maze(self, path=None):
        """
        Vizualizuoja labirintą su keliu (jei duotas)
        """
        maze_copy = [list(row) for row in self.maze]
        
        if path:
            for state in path:
                row, col = state
                if maze_copy[row][col] not in ['S', 'G']:
                    maze_copy[row][col] = '*'
        
        print("\nLabirintas:")
        print("  " + "".join([str(i % 10) for i in range(self.cols)]))
        for i, row in enumerate(maze_copy):
            print(f"{i} {''.join(row)}")
        print("\nLegenda: S=Start, G=Goal, #=Siena, .=Kelias, *=Sprendimo kelias")


# =============================================================================
# PAVYZDŽIŲ LABIRINTAI
# =============================================================================

def create_simple_maze():
    """Paprastas 5x5 labirintas - mokymosi tikslams"""
    maze = [
        ['.', '.', '#', '.', '.'],
        ['.', '#', '#', '.', '.'],
        ['.', '.', '.', '#', '.'],
        ['#', '.', '#', '#', '.'],
        ['.', '.', '.', '.', '.']
    ]
    start = (0, 0)
    goal = (4, 4)
    return maze, start, goal


def create_medium_maze():
    """Vidutinio sudėtingumo 8x8 labirintas"""
    maze = [
        ['.', '.', '.', '#', '.', '.', '.', '.'],
        ['.', '#', '.', '#', '.', '#', '#', '.'],
        ['.', '#', '.', '.', '.', '.', '#', '.'],
        ['.', '#', '#', '#', '#', '.', '#', '.'],
        ['.', '.', '.', '.', '#', '.', '.', '.'],
        ['#', '#', '.', '#', '#', '#', '.', '#'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '.', '#', '#', '.'],
    ]
    start = (0, 0)
    goal = (7, 7)
    return maze, start, goal


def create_complex_maze():
    """Sudėtingas 10x10 labirintas"""
    maze = [
        ['.', '.', '.', '#', '.', '.', '.', '.', '#', '.'],
        ['.', '#', '.', '#', '.', '#', '#', '.', '#', '.'],
        ['.', '#', '.', '.', '.', '.', '#', '.', '.', '.'],
        ['.', '#', '#', '#', '#', '.', '#', '#', '#', '.'],
        ['.', '.', '.', '.', '#', '.', '.', '.', '#', '.'],
        ['#', '#', '#', '.', '#', '#', '#', '.', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '#', '.', '.', '.'],
        ['.', '#', '#', '#', '#', '.', '#', '#', '#', '#'],
        ['.', '.', '.', '.', '#', '.', '.', '.', '.', '.'],
        ['#', '#', '.', '.', '#', '.', '#', '#', '#', '.'],
    ]
    start = (0, 0)
    goal = (9, 9)
    return maze, start, goal


def create_spiral_maze():
    """Spiralinis labirintas - iššūkis algoritmams"""
    maze = [
        ['.', '.', '.', '.', '.', '.', '.'],
        ['#', '#', '#', '#', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '#', '.'],
        ['.', '#', '#', '#', '.', '#', '.'],
        ['.', '#', '.', '.', '.', '#', '.'],
        ['.', '#', '#', '#', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
    ]
    start = (0, 0)
    goal = (4, 2)  # Centre spiralės
    return maze, start, goal


# =============================================================================
# PAGRINDINIS TESTAS
# =============================================================================

def test_maze_problem(maze_type='simple', search_method='best_first'):
    """
    Testuoja labirinto problemą su skirtingais algoritmais
    
    Args:
        maze_type: 'simple', 'medium', 'complex', 'spiral'
        search_method: 'breadth_first', 'best_first', 'astar', 'depth_first'
    """
    print("=" * 80)
    print(f"MAZE PROBLEM - {maze_type.upper()} labirintas")
    print(f"Paieškos algoritmas: {search_method.upper()}")
    print("=" * 80)
    
    # Pasirenkame labirintą
    if maze_type == 'simple':
        maze, start, goal = create_simple_maze()
    elif maze_type == 'medium':
        maze, start, goal = create_medium_maze()
    elif maze_type == 'complex':
        maze, start, goal = create_complex_maze()
    elif maze_type == 'spiral':
        maze, start, goal = create_spiral_maze()
    else:
        maze, start, goal = create_simple_maze()
    
    # Sukuriame problemos objektą
    problem = MazeProblem(maze, start, goal)
    
    print(f"\nPradinė pozicija: {start}")
    print(f"Tikslāinė pozicija: {goal}")
    
    # Vizualizuojame pradinį labirintą
    maze_display = [list(row) for row in maze]
    maze_display[start[0]][start[1]] = 'S'
    maze_display[goal[0]][goal[1]] = 'G'
    problem.maze = maze_display
    problem.visualize_maze()
    
    # Paleidžiame paieškos algoritmą
    print(f"\n{'─' * 80}")
    print(f"Vykdomas {search_method} algoritmas...")
    print(f"{'─' * 80}\n")
    
    import time
    start_time = time.time()
    
    if search_method == 'breadth_first':
        solution_node = breadth_first_graph_search(problem)
    elif search_method == 'best_first':
        solution_node = best_first_graph_search(problem, lambda n: problem.h(n))
    elif search_method == 'astar':
        solution_node = astar_search(problem)
    elif search_method == 'depth_first':
        solution_node = depth_first_graph_search(problem)
    else:
        solution_node = best_first_graph_search(problem, lambda n: problem.h(n))
    
    end_time = time.time()
    
    # Rezultatai
    if solution_node:
        solution = solution_node.solution()
        path = solution_node.path()
        path_states = [node.state for node in path]
        
        print("✓ SPRENDIMAS RASTAS!")
        print(f"\n{'─' * 80}")
        print("STATISTIKA:")
        print(f"{'─' * 80}")
        print(f"  Žingsnių skaičius: {len(solution)}")
        print(f"  Lankytų būsenų: {len(path)}")
        print(f"  Laikas: {(end_time - start_time) * 1000:.2f} ms")
        print(f"  Veiksmų seka: {' → '.join(solution)}")
        
        # Vizualizuojame sprendimą
        problem.visualize_maze(path_states)
        
        # Išsamus kelias
        print(f"\n{'─' * 80}")
        print("IŠSAMUS KELIAS:")
        print(f"{'─' * 80}")
        for i, node in enumerate(path):
            action = node.action if node.action else "START"
            pos = node.state
            h_val = problem.h(node)
            print(f"  Žingsnis {i}: {action:8} → pozicija {pos}, h(n)={h_val}")
    else:
        print("✗ Sprendimas NERASTAS!")


def compare_algorithms(maze_type='medium'):
    """
    Palygina visus algoritmus tame pačiame labirinte
    """
    print("\n" + "=" * 80)
    print("ALGORITMŲ PALYGINIMAS")
    print("=" * 80)
    
    algorithms = ['breadth_first', 'depth_first', 'best_first', 'astar']
    results = {}
    
    for alg in algorithms:
        print(f"\n\nTestuojamas: {alg.upper()}")
        print("-" * 80)
        
        if maze_type == 'simple':
            maze, start, goal = create_simple_maze()
        elif maze_type == 'medium':
            maze, start, goal = create_medium_maze()
        elif maze_type == 'complex':
            maze, start, goal = create_complex_maze()
        else:
            maze, start, goal = create_simple_maze()
        
        problem = MazeProblem(maze, start, goal)
        
        import time
        start_time = time.time()
        
        try:
            if alg == 'breadth_first':
                solution_node = breadth_first_graph_search(problem)
            elif alg == 'depth_first':
                solution_node = depth_first_graph_search(problem)
            elif alg == 'best_first':
                solution_node = best_first_graph_search(problem, lambda n: problem.h(n))
            elif alg == 'astar':
                solution_node = astar_search(problem)
            
            end_time = time.time()
            
            if solution_node:
                solution = solution_node.solution()
                results[alg] = {
                    'steps': len(solution),
                    'time': (end_time - start_time) * 1000,
                    'success': True
                }
                print(f"  ✓ Žingsnių: {len(solution)}, Laikas: {results[alg]['time']:.2f} ms")
            else:
                results[alg] = {'success': False}
                print(f"  ✗ Sprendimas nerastas")
        except Exception as e:
            results[alg] = {'success': False, 'error': str(e)}
            print(f"  ✗ Klaida: {e}")
    
    # Suvestinė
    print("\n" + "=" * 80)
    print("SUVESTINĖ LENTELĖ")
    print("=" * 80)
    print(f"{'Algoritmas':<20} {'Žingsniai':<12} {'Laikas (ms)':<15} {'Statusas'}")
    print("-" * 80)
    
    for alg, data in results.items():
        if data.get('success'):
            print(f"{alg:<20} {data['steps']:<12} {data['time']:<15.2f} ✓")
        else:
            print(f"{alg:<20} {'N/A':<12} {'N/A':<15} ✗")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Test 1: Paprastas labirintas su best_first
    test_maze_problem('simple', 'best_first')
    
    # Test 2: Vidutinis labirintas su A*
    print("\n\n")
    test_maze_problem('medium', 'astar')
    
    # Test 3: Algoritmų palyginimas
    print("\n\n")
    compare_algorithms('medium')
    
    # Test 4: Spiralinis labirintas - iššūkis!
    print("\n\n")
    test_maze_problem('spiral', 'astar')

    # Test 5: Vidutinis labirintas su A*
    print("\n\n")
    test_maze_problem('medium', 'breadth_first')

    # Test 6: Vidutinis labirintas su A*
    print("\n\n")
    test_maze_problem('medium', 'depth_first')
