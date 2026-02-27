"""
WATER JUG PROBLEM - Vandens Indų Problema
Klasikinė AI problema naudojant tą pačią architektūrą

Problema: Turime du indus (A ir B) su skirtingais talpomis.
Galime pilti vandenį, išpilti, perpilti iš vieno į kitą.
Tikslas: Pasiekti tikslini vandens kiekį viename iš indų.

Klasikinis pavyzdys: 
  - Indas A talpa: 4 litrai
  - Indas B talpa: 3 litrai
  - Tikslas: Gauti 2 litrus inde A
"""

from search import *


class WaterJugProblem(Problem):
    """
    Vandens Indų problema.
    Paveldėta iš Problem - ta pati architektūra kaip EightPuzzle ir MazeProblem!
    
    Būsena (state): tuple (a, b) kur:
        a = vandens kiekis inde A (litrai)
        b = vandens kiekis inde B (litrai)
    """
    
    def __init__(self, capacity_a, capacity_b, initial=(0, 0), goal=(2, 0)):
        """
        Args:
            capacity_a: Indo A talpa
            capacity_b: Indo B talpa
            initial: Pradinė būsena (kiek vandens kiekviename inde)
            goal: Tikslāinė būsena
        """
        super().__init__(initial, goal)
        self.capacity_a = capacity_a
        self.capacity_b = capacity_b
    
    def actions(self, state):
        """
        Grąžina galimus veiksmus.
        
        Galimi veiksmai:
        1. FILL_A - Pripildyti indą A iki viršaus
        2. FILL_B - Pripildyti indą B iki viršaus
        3. EMPTY_A - Išpilti visą vandenį iš A
        4. EMPTY_B - Išpilti visą vandenį iš B
        5. POUR_A_TO_B - Perpilti iš A į B (kiek telpa)
        6. POUR_B_TO_A - Perpilti iš B į A (kiek telpa)
        
        Same architecture as EightPuzzle.actions()!
        """
        a, b = state
        possible_actions = []
        
        # FILL - Galime pripildyti, jei ne pilnas
        if a < self.capacity_a:
            possible_actions.append('FILL_A')
        if b < self.capacity_b:
            possible_actions.append('FILL_B')
        
        # EMPTY - Galime išpilti, jei ne tuščias
        if a > 0:
            possible_actions.append('EMPTY_A')
        if b > 0:
            possible_actions.append('EMPTY_B')
        
        # POUR - Galime perpilti, jei yra iš kur ir yra kur
        if a > 0 and b < self.capacity_b:
            possible_actions.append('POUR_A_TO_B')
        if b > 0 and a < self.capacity_a:
            possible_actions.append('POUR_B_TO_A')
        
        return possible_actions
    
    def result(self, state, action):
        """
        Grąžina naują būseną po veiksmo.
        
        Same architecture as EightPuzzle.result()!
        """
        a, b = state
        
        if action == 'FILL_A':
            return (self.capacity_a, b)
        
        elif action == 'FILL_B':
            return (a, self.capacity_b)
        
        elif action == 'EMPTY_A':
            return (0, b)
        
        elif action == 'EMPTY_B':
            return (a, 0)
        
        elif action == 'POUR_A_TO_B':
            # Perpilame iš A į B kiek telpa
            pour_amount = min(a, self.capacity_b - b)
            return (a - pour_amount, b + pour_amount)
        
        elif action == 'POUR_B_TO_A':
            # Perpilame iš B į A kiek telpa
            pour_amount = min(b, self.capacity_a - a)
            return (a + pour_amount, b - pour_amount)
        
        return state
    
    def goal_test(self, state):
        """
        Patikrina ar pasiekėme tikslą.
        
        Same as before!
        """
        return state == self.goal
    
    def h(self, node):
        """
        Euristinė funkcija.
        
        Naudojame paprastą euristiką: skirtumas tarp dabartinės būsenos ir tikslo.
        
        Similar to EightPuzzle.h()!
        """
        a, b = node.state
        goal_a, goal_b = self.goal
        
        # Paprastas skirtumas
        return abs(a - goal_a) + abs(b - goal_b)
    
    def visualize_state(self, state, action=None):
        """Vizualizuoja indus"""
        a, b = state
        
        if action:
            print(f"\nVeiksmas: {action}")
        
        print(f"\n  Indas A (talpa {self.capacity_a}L)  Indas B (talpa {self.capacity_b}L)")
        print(f"  {'─' * 15}  {'─' * 15}")
        
        # Piešiame indus
        for level in range(max(self.capacity_a, self.capacity_b), 0, -1):
            a_vis = '█' * 8 if a >= level else ' ' * 8
            b_vis = '█' * 8 if b >= level else ' ' * 8
            print(f"  |{a_vis}|  |{b_vis}|")
        
        print(f"  {'─' * 10}  {'─' * 10}")
        print(f"    {a}L / {self.capacity_a}L      {b}L / {self.capacity_b}L")


# =============================================================================
# PAVYZDŽIŲ PROBLEMOS
# =============================================================================

def classic_4_3_problem():
    """
    Klasikinis 4-3 litrų problema.
    Tikslas: Gauti 2 litrus inde A
    """
    return WaterJugProblem(
        capacity_a=4,
        capacity_b=3,
        initial=(0, 0),
        goal=(2, 0)
    )


def challenge_5_3_problem():
    """
    Sudėtingesnė 5-3 litrų problema.
    Tikslas: Gauti 4 litrus inde A
    """
    return WaterJugProblem(
        capacity_a=5,
        capacity_b=3,
        initial=(0, 0),
        goal=(4, 0)
    )


def die_hard_problem():
    """
    Problema iš filmo "Die Hard 3"!
    Bruce Willis ir Samuel L. Jackson turi nusaugoti bombą.
    
    Turimi indai: 5 litrų ir 3 litrų
    Tikslas: Gauti tiksliai 4 litrus!
    """
    return WaterJugProblem(
        capacity_a=5,
        capacity_b=3,
        initial=(0, 0),
        goal=(4, 0)
    )


# =============================================================================
# TESTAS
# =============================================================================

def test_water_jug(problem_type='classic', search_method='best_first'):
    """Testuoja vandens indų problemą"""
    
    print("=" * 80)
    print("WATER JUG PROBLEM")
    print("=" * 80)
    
    # Pasirenkame problemą
    if problem_type == 'classic':
        problem = classic_4_3_problem()
        print("\n📦 Klasikinė 4-3 litrų problema")
    elif problem_type == 'challenge':
        problem = challenge_5_3_problem()
        print("\n📦 Sudėtingesnė 5-3 litrų problema")
    elif problem_type == 'die_hard':
        problem = die_hard_problem()
        print("\n💣 Die Hard 3 problema!")
    else:
        problem = classic_4_3_problem()
    
    print(f"   Indas A talpa: {problem.capacity_a} litrai")
    print(f"   Indas B talpa: {problem.capacity_b} litrai")
    print(f"   Pradžia: {problem.initial}")
    print(f"   Tikslas: {problem.goal}")
    
    # Vizualizuojame pradinę būseną
    print("\nPRADINĖ BŪSENA:")
    problem.visualize_state(problem.initial)
    
    print("\nTIKSLINĖ BŪSENA:")
    problem.visualize_state(problem.goal)
    
    # Paleidžiame algoritmą
    print(f"\n{'─' * 80}")
    print(f"Vykdomas {search_method.upper()} algoritmas...")
    print(f"{'─' * 80}")
    
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
        
        print("\n✓ SPRENDIMAS RASTAS!")
        print(f"\n{'─' * 80}")
        print("STATISTIKA:")
        print(f"{'─' * 80}")
        print(f"  Žingsnių skaičius: {len(solution)}")
        print(f"  Laikas: {(end_time - start_time) * 1000:.2f} ms")
        print(f"  Veiksmų seka: {' → '.join(solution)}")
        
        # Vizualizuojame sprendimą žingsnis po žingsnio
        print(f"\n{'=' * 80}")
        print("SPRENDIMO ŽINGSNIAI:")
        print(f"{'=' * 80}")
        
        for i, node in enumerate(path):
            print(f"\n{'─' * 80}")
            print(f"ŽINGSNIS {i}: ", end="")
            if node.action:
                print(node.action)
            else:
                print("PRADŽIA")
            print(f"{'─' * 80}")
            
            problem.visualize_state(node.state)
            print(f"  Būsena: {node.state}, h(n)={problem.h(node)}, cost={node.path_cost}")
        
        print("\n" + "=" * 80)
        print("🎉 TIKSLAS PASIEKTAS!")
        print("=" * 80)
    else:
        print("\n✗ Sprendimas NERASTAS!")


def interactive_water_jug():
    """Interaktyvus režimas - vartotojas gali bandyti pats"""
    print("=" * 80)
    print("WATER JUG - INTERAKTYVUS REŽIMAS")
    print("=" * 80)
    
    print("\nĮveskite parametrus:")
    cap_a = int(input("Indo A talpa (litrai): "))
    cap_b = int(input("Indo B talpa (litrai): "))
    goal_a = int(input("Tikslas - litrai inde A: "))
    goal_b = int(input("Tikslas - litrai inde B: "))
    
    problem = WaterJugProblem(cap_a, cap_b, (0, 0), (goal_a, goal_b))
    
    print("\n" + "=" * 80)
    print("JŪSŲ PROBLEMA:")
    print("=" * 80)
    print(f"Indai: {cap_a}L ir {cap_b}L")
    print(f"Tikslas: ({goal_a}, {goal_b})")
    
    problem.visualize_state(problem.goal, "TIKSLAS")
    
    print("\nSprendžiame su A* algoritmu...")
    solution_node = astar_search(problem)
    
    if solution_node:
        print("✓ Sprendimas rastas!")
        print(f"Žingsnių: {len(solution_node.solution())}")
        
        choice = input("\nAr norite pamatyti sprendimą? (t/n): ")
        if choice.lower() == 't':
            for i, node in enumerate(solution_node.path()):
                print(f"\nŽingsnis {i}:")
                if node.action:
                    print(f"Veiksmas: {node.action}")
                problem.visualize_state(node.state)
                input("Spauskite Enter tęsti...")
    else:
        print("✗ Sprendimas nerastas - galbūt neįmanoma pasiekti šios būsenos!")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Test 1: Klasikinė problema
    test_water_jug('classic', 'astar')
    
    # Test 2: Die Hard problema
    print("\n\n")
    test_water_jug('die_hard', 'astar')
    
    # Test 3: Interaktyvus (nekomentukite jei norite)
    # print("\n\n")
    # interactive_water_jug()
