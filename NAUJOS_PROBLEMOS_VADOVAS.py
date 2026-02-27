"""
═══════════════════════════════════════════════════════════════════════════════
    NAUJOS PAIEŠKOS PROBLEMOS - SUKŪRIMO VADOVAS
    Kaip sukurti savo problemą naudojant tą pačią architektūrą
═══════════════════════════════════════════════════════════════════════════════

📚 SUKURTOS TRYS NAUJOS PROBLEMOS:

1. MazeProblem.py - Labirinto paieškos problema
2. WaterJugProblem.py - Vandens indų problema (klasikinė AI)
3. MazeProblem_Debug.py - Debug režimas su išsamiu trasimu

═══════════════════════════════════════════════════════════════════════════════
1. ARCHITEKTŪROS ŠABLONAS
═══════════════════════════════════════════════════════════════════════════════

Visos problemos naudoja TĄ PAČIĄ architektūrą kaip EightPuzzle:

┌─────────────────────────────────────────────────────────────────────────────┐
│                    Problem (Bazinė Klasė)                                    │
│                              ▲                                               │
│                              │ inheritance                                   │
│          ┌───────────────────┼───────────────────┐                          │
│          │                   │                   │                          │
│    EightPuzzle         MazeProblem        WaterJugProblem                   │
│                                                                              │
│ TAI PATI ARCHITEKTŪRA - SKIRTUMAS TIK IMPLEMENTACIJOJE!                     │
└─────────────────────────────────────────────────────────────────────────────┘


PRIVALOMI METODAI (must implement):
────────────────────────────────────
1. __init__(initial, goal)        → Konstruktorius
2. actions(state)                 → Kokie veiksmai galimi šioje būsenoje?
3. result(state, action)          → Kokia bus būsena po veiksmo?
4. goal_test(state)               → Ar pasiektas tikslas?

OPTIONAL METODAI:
────────────────────────────────────
5. h(node)                        → Euristinė funkcija (greičiau sprendžia)
6. path_cost(...)                 → Kelio kaina (jei reikia custom)


═══════════════════════════════════════════════════════════════════════════════
2. MAZE PROBLEM - LABIRINTAS
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ KONCEPCIJA:                                                                  │
│   • Rasti kelią nuo Start iki Goal labirinte                                │
│   • Vengiame sienų (#)                                                       │
│   • Judame 4 kryptimis: UP, DOWN, LEFT, RIGHT                               │
└─────────────────────────────────────────────────────────────────────────────┘

BŪSENA (state):
────────────────
    tuple (row, col) - pozicija labirinte
    Pavyzdys: (0, 0) = viršutinis kairysis kampas

ARCHITEKTŪROS IMPLEMENTACIJA:
────────────────────────────────

class MazeProblem(Problem):
    
    def __init__(self, maze, initial, goal):
        super().__init__(initial, goal)
        self.maze = maze              # 2D masyvas
        self.rows = len(maze)
        self.cols = len(maze[0])
    
    def actions(self, state):
        # Grąžina UP/DOWN/LEFT/RIGHT
        # Tikrina: ar ne už ribų? ar ne siena?
        row, col = state
        possible = []
        
        if row > 0 and maze[row-1][col] != '#':
            possible.append('UP')
        # ... ir t.t.
        
        return possible
    
    def result(self, state, action):
        # Juda į naują poziciją
        row, col = state
        if action == 'UP':
            return (row-1, col)
        # ... ir t.t.
    
    def h(self, node):
        # Manhattan distance - optimalu labirintams!
        row1, col1 = node.state
        row2, col2 = self.goal
        return abs(row1-row2) + abs(col1-col2)


PAVYZDYS:
─────────
maze = [
    ['.', '.', '#', '.', '.'],
    ['.', '#', '#', '.', '.'],
    ['.', '.', '.', '#', '.'],
    ['#', '.', '#', '#', '.'],
    ['.', '.', '.', '.', '.']
]
problem = MazeProblem(maze, start=(0,0), goal=(4,4))
solution = astar_search(problem).solution()

REZULTATAS:
───────────
  01234
0 S.#..
1 *##..
2 **.#.
3 #*##.
4 .***G

Sprendimas: DOWN → DOWN → RIGHT → DOWN → DOWN → RIGHT → RIGHT → RIGHT


═══════════════════════════════════════════════════════════════════════════════
3. WATER JUG PROBLEM - VANDENS INDAI
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ KONCEPCIJA:                                                                  │
│   • Du indai su skirtingomis talpomis                                       │
│   • Galima: pripildyti, išpilti, perpilti                                   │
│   • Tikslas: Gauti tikslų vandens kiekį                                     │
│                                                                              │
│ Klasikinis pavyzdys (Die Hard 3):                                           │
│   Indai: 5L ir 3L                                                           │
│   Tikslas: Gauti tiksliai 4 litrus                                          │
└─────────────────────────────────────────────────────────────────────────────┘

BŪSENA (state):
────────────────
    tuple (a, b) - vandens kiekis kiekviename inde
    Pavyzdys: (3, 2) = 3L inde A, 2L inde B

ARCHITEKTŪROS IMPLEMENTACIJA:
────────────────────────────────

class WaterJugProblem(Problem):
    
    def __init__(self, capacity_a, capacity_b, initial, goal):
        super().__init__(initial, goal)
        self.capacity_a = capacity_a
        self.capacity_b = capacity_b
    
    def actions(self, state):
        a, b = state
        possible = []
        
        # Galima pripildyti jei ne pilnas
        if a < self.capacity_a:
            possible.append('FILL_A')
        if b < self.capacity_b:
            possible.append('FILL_B')
        
        # Galima išpilti jei ne tuščias
        if a > 0:
            possible.append('EMPTY_A')
        if b > 0:
            possible.append('EMPTY_B')
        
        # Galima perpilti
        if a > 0 and b < self.capacity_b:
            possible.append('POUR_A_TO_B')
        if b > 0 and a < self.capacity_a:
            possible.append('POUR_B_TO_A')
        
        return possible
    
    def result(self, state, action):
        a, b = state
        
        if action == 'FILL_A':
            return (self.capacity_a, b)
        elif action == 'POUR_A_TO_B':
            pour = min(a, self.capacity_b - b)
            return (a - pour, b + pour)
        # ... ir t.t.
    
    def h(self, node):
        # Skirtumas nuo tikslo
        a, b = node.state
        goal_a, goal_b = self.goal
        return abs(a - goal_a) + abs(b - goal_b)


PAVYZDYS:
─────────
problem = WaterJugProblem(
    capacity_a=4,
    capacity_b=3,
    initial=(0, 0),
    goal=(2, 0)
)
solution = astar_search(problem).solution()

SPRENDIMO ŽINGSNIAI:
────────────────────
Žingsnis 0: (0, 0) START
Žingsnis 1: (0, 3) FILL_B         → Pripildome B
Žingsnis 2: (3, 0) POUR_B_TO_A    → Perpilame į A
Žingsnis 3: (3, 3) FILL_B         → Vėl pripildome B
Žingsnis 4: (4, 2) POUR_B_TO_A    → Perpilame (A pilnas, liko 2L B-je)
Žingsnis 5: (0, 2) EMPTY_A        → Išpilame A
Žingsnis 6: (2, 0) POUR_B_TO_A    → Perpilame 2L iš B į A → TIKSLAS!


═══════════════════════════════════════════════════════════════════════════════
4. KAIP SUKURTI SAVO PROBLEMĄ - ŽINGSNIS PO ŽINGSNIO
═══════════════════════════════════════════════════════════════════════════════

ŽINGSNIS 1: APIBRĖŽK PROBLEMĄ
──────────────────────────────
  ❓ Kas yra būsena?
  ❓ Kokie galimi veiksmai?
  ❓ Kas yra tikslas?

ŽINGSNIS 2: SUKURK KLASĘ
──────────────────────────────

class YourProblem(Problem):
    def __init__(self, initial, goal, **custom_params):
        super().__init__(initial, goal)
        # Išsaugok custom parametrus
        self.your_param = custom_params.get('param')


ŽINGSNIS 3: IMPLEMENTUOK ACTIONS
──────────────────────────────────

    def actions(self, state):
        """
        Grąžina list galimų veiksmų šioje būsenoje
        
        Logika:
        1. Išskaidyk state į komponentus
        2. Tikrink kiekvienos galimybės tinkamumą
        3. Grąžink string list
        """
        possible = []
        
        # Tavo logika čia
        if <sąlyga>:
            possible.append('ACTION_NAME')
        
        return possible


ŽINGSNIS 4: IMPLEMENTUOK RESULT
──────────────────────────────────

    def result(self, state, action):
        """
        Grąžina naują būseną po veiksmo
        
        Logika:
        1. Išskaidyk state
        2. Pagal action atlik transformaciją
        3. Grąžink naują state (IMMUTABLE!)
        """
        # Tavo transformacijos logika
        
        if action == 'YOUR_ACTION':
            return new_state
        
        return state


ŽINGSNIS 5: GOAL_TEST (dažniausiai default)
────────────────────────────────────────────

    def goal_test(self, state):
        # Default: state == self.goal
        # Arba custom logika jei reikia
        return state == self.goal


ŽINGSNIS 6: EURISTIKA (optional, bet rekomenduojama)
─────────────────────────────────────────────────────

    def h(self, node):
        """
        Įvertink atstumą iki tikslo
        
        Turi būti ADMISSIBLE:
        - Niekada nepervertink (h <= tikras atstumas)
        - h(goal) = 0
        
        Populiarios euristikos:
        - Manhattan distance: |x1-x2| + |y1-y2|
        - Euclidean distance: sqrt((x1-x2)² + (y1-y2)²)
        - Hamming distance: skaičius skirtumų
        """
        # Tavo euristika
        return estimated_distance_to_goal


═══════════════════════════════════════════════════════════════════════════════
5. PAVYZDŽIŲ NAUDOJIMAS
═══════════════════════════════════════════════════════════════════════════════

MAZE PROBLEM:
─────────────
from MazeProblem import *

# Testuok paprastą labirintą
test_maze_problem('simple', 'best_first')

# Palygink algoritmus
compare_algorithms('medium')

# Debug režimas
python MazeProblem_Debug.py


WATER JUG:
──────────
from WaterJugProblem import *

# Klasikinė problema
test_water_jug('classic', 'astar')

# Die Hard 3 problema!
test_water_jug('die_hard', 'astar')

# Interaktyvus režimas
interactive_water_jug()


═══════════════════════════════════════════════════════════════════════════════
6. GALIMOS KITOS PROBLEMOS (IDĖJOS)
═══════════════════════════════════════════════════════════════════════════════

1. TOWER OF HANOI
   State: (disk_positions_tower_A, tower_B, tower_C)
   Actions: MOVE_A_TO_B, MOVE_B_TO_C, ...
   
2. MISSIONARIES AND CANNIBALS
   State: (missionaries_left, cannibals_left, boat_position)
   Actions: MOVE_1M_1C, MOVE_2M, ...
   
3. SLIDING PUZZLE (N×N)
   State: tuple of numbers
   Actions: UP, DOWN, LEFT, RIGHT
   
4. RUBIK'S CUBE (2×2 mini)
   State: tuple of face colors
   Actions: TURN_FRONT, TURN_RIGHT, ...
   
5. RIVER CROSSING
   State: (items_on_left_bank, boat_position)
   Actions: MOVE_ITEM_X
   
6. KNIGHT'S TOUR
   State: (position, visited_squares)
   Actions: KNIGHT_MOVE_TO_X
   
7. SUDOKU
   State: 9×9 grid
   Actions: PLACE_NUMBER_X_AT_Y


═══════════════════════════════════════════════════════════════════════════════
7. ALGORITMŲ NAUDOJIMAS
═══════════════════════════════════════════════════════════════════════════════

VISI ŠITIE ALGORITMAI VEIKIA SU VISOMIS PROBLEMOMIS!

1. breadth_first_graph_search(problem)
   ✅ Garantuoja optimumą
   ⚠️ Lėtas didelėms problemoms
   
2. depth_first_graph_search(problem)
   ✅ Mažai atminties
   ⚠️ Ne optimalus
   
3. best_first_graph_search(problem, lambda n: problem.h(n))
   ✅ Greitas su gera euristika
   ⚠️ Ne visada optimalus
   
4. astar_search(problem)
   ✅ Optimalus su admissible euristika
   ✅ Greitas
   🏆 REKOMENDUOJAMAS!


NAUDOJIMAS:
───────────
from search import *
from YourProblem import *

problem = YourProblem(initial_state, goal_state)
solution_node = astar_search(problem)

if solution_node:
    solution = solution_node.solution()
    print(f"Sprendimas: {solution}")
    print(f"Žingsnių: {len(solution)}")


═══════════════════════════════════════════════════════════════════════════════
8. RAKTINIAI PRIVALUMAI ŠIOS ARCHITEKTŪROS
═══════════════════════════════════════════════════════════════════════════════

✅ MODULAR DESIGN
   → Galima lengvai kurti naujas problemas
   → Nekeičiame paieškos algoritmų

✅ REUSABLE ALGORITHMS
   → Tie patys algoritmai veikia visur
   → Išbandyta ir patikima

✅ SEPARATION OF CONCERNS
   → Problema apibrėžia "ką spręsti"
   → Algoritmas sprendžia "kaip spręsti"
   → Node tvarko medžio struktūrą

✅ EXTENSIBLE
   → Pridėti naują problemą = 1 klasė
   → Pridėti naują algoritmą = veikia su visomis

✅ TESTABLE
   → Lengva testuoti atskirai
   → Debug režimai padeda mokymuisi


═══════════════════════════════════════════════════════════════════════════════
IŠVADA
═══════════════════════════════════════════════════════════════════════════════

🎯 Sukūrėme 2 naujas problemas su ta pačia architektūra
🎯 Visos naudoja tuos pačius paieškos algoritmus
🎯 Moduliarus dizainas leidžia lengvai kurti daugiau

FAILAI:
  📄 MazeProblem.py - Labirinto problema + testai
  📄 MazeProblem_Debug.py - Debug režimas su išsamiu trasimu  
  📄 WaterJugProblem.py - Vandens indų problema + Die Hard 3
  📄 EightPuzzle_Architektura.txt - Architektūros dokumentacija

PALEISTI:
  python MazeProblem.py
  python MazeProblem_Debug.py
  python WaterJugProblem.py

Dabar tu gali sukurti SAVO problemą naudojant tą pačią architektūrą! 🚀

═══════════════════════════════════════════════════════════════════════════════
"""

# Šis failas yra dokumentacija - nebūtina vykdyti
if __name__ == "__main__":
    print(__doc__)
