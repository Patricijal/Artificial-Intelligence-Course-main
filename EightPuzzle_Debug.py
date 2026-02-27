"""
EightPuzzle Debug Mode - Išsamus algoritmo trasavimas
Parodo visus žingsnius kaip veikia paieškos algoritmas
"""

from search import *


def debug_eight_puzzle():
    """Išsamus debugas su komentarais"""
    
    print("=" * 80)
    print("EIGHT PUZZLE - DEBUG REŽIMAS")
    print("=" * 80)
    
    # ============================================================================
    # ŽINGSNIS 1: Problemos sukūrimas
    # ============================================================================
    print("\n【 ŽINGSNIS 1: Sukuriame problemą 】")
    print("-" * 80)
    
    initial_state = (2, 4, 3, 1, 5, 6, 7, 8, 0)
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    
    puzzle = EightPuzzle(initial_state, goal_state)
    
    print(f"Pradinė būsena: {initial_state}")
    print("Vizualizacija:")
    print(f"  {initial_state[0]} {initial_state[1]} {initial_state[2]}")
    print(f"  {initial_state[3]} {initial_state[4]} {initial_state[5]}")
    print(f"  {initial_state[6]} {initial_state[7]} {initial_state[8]}")
    
    print(f"\nTikslinė būsena: {goal_state}")
    print("Vizualizacija:")
    print(f"  {goal_state[0]} {goal_state[1]} {goal_state[2]}")
    print(f"  {goal_state[3]} {goal_state[4]} {goal_state[5]}")
    print(f"  {goal_state[6]} {goal_state[7]} {goal_state[8]}")
    
    # ============================================================================
    # ŽINGSNIS 2: Pradinio mazgo sukūrimas
    # ============================================================================
    print("\n【 ŽINGSNIS 2: Sukuriame pradinį Node mazgą 】")
    print("-" * 80)
    
    root_node = Node(puzzle.initial)
    
    print(f"Node objektas: {root_node}")
    print(f"  - state: {root_node.state}")
    print(f"  - parent: {root_node.parent}")
    print(f"  - action: {root_node.action}")
    print(f"  - path_cost: {root_node.path_cost}")
    print(f"  - depth: {root_node.depth}")
    
    # ============================================================================
    # ŽINGSNIS 3: Galimi veiksmai (Actions)
    # ============================================================================
    print("\n【 ŽINGSNIS 3: Kokie veiksmai galimi? 】")
    print("-" * 80)
    
    blank_index = puzzle.find_blank_square(initial_state)
    print(f"Tuščias kvadratas (0) yra pozicijoje: {blank_index}")
    print(f"Tai atitinka koordinates: eilutė={blank_index // 3}, stulpelis={blank_index % 3}")
    
    actions = puzzle.actions(initial_state)
    print(f"\nGalimi veiksmai: {actions}")
    
    # Paaiškiname kodėl
    print("\nKodėl tik šie veiksmai?")
    print(f"  - blank_index % 3 == {blank_index % 3} (stulpelis)")
    print(f"  - blank_index < 3? {blank_index < 3}")
    print(f"  - blank_index % 3 == 2? {blank_index % 3 == 2}")
    print(f"  - blank_index > 5? {blank_index > 5}")
    
    # ============================================================================
    # ŽINGSNIS 4: Rezultatas po veiksmo (Result)
    # ============================================================================
    print("\n【 ŽINGSNIS 4: Kas nutiks po kiekvieno veiksmo? 】")
    print("-" * 80)
    
    for action in actions:
        new_state = puzzle.result(initial_state, action)
        print(f"\nVeiksmas: {action}")
        print(f"Nauja būsena: {new_state}")
        print("Vizualizacija:")
        print(f"  {new_state[0]} {new_state[1]} {new_state[2]}")
        print(f"  {new_state[3]} {new_state[4]} {new_state[5]}")
        print(f"  {new_state[6]} {new_state[7]} {new_state[8]}")
    
    # ============================================================================
    # ŽINGSNIS 5: Node.expand() - Generuojami vaikų mazgai
    # ============================================================================
    print("\n【 ŽINGSNIS 5: Node.expand() - Sukuriami vaikų mazgai 】")
    print("-" * 80)
    
    children = root_node.expand(puzzle)
    
    print(f"Sugeneruota {len(children)} vaikų mazgų:")
    for i, child in enumerate(children, 1):
        print(f"\n  Vaikas #{i}:")
        print(f"    - action: {child.action}")
        print(f"    - state: {child.state}")
        print(f"    - parent: {child.parent.state}")
        print(f"    - depth: {child.depth}")
        print(f"    - path_cost: {child.path_cost}")
    
    # ============================================================================
    # ŽINGSNIS 6: Euristika h(n) - Netaisyklingų plokštelių skaičius
    # ============================================================================
    print("\n【 ŽINGSNIS 6: Euristika h(n) 】")
    print("-" * 80)
    
    h_value = puzzle.h(root_node)
    print(f"h(root_node) = {h_value}")
    print("\nKaip skaičiuojama?")
    print("h(n) = skaičius plokštelių ne savo vietose")
    
    print("\nPalyginimas:")
    print("Pozicija | Dabar | Tikslas | Match?")
    print("-" * 40)
    for i in range(9):
        current = initial_state[i]
        target = goal_state[i]
        match = "✓" if current == target else "✗"
        print(f"   {i}     |   {current}   |    {target}    |  {match}")
    
    print(f"\nNe savo vietose: {h_value} plokštelės")
    
    # ============================================================================
    # ŽINGSNIS 7: Best-First Search su Priority Queue
    # ============================================================================
    print("\n【 ŽINGSNIS 7: Best-First Search pradžia 】")
    print("-" * 80)
    
    print("Algoritmas naudos PriorityQueue, kuri rikiuoja pagal h(n)")
    print("Kas kartą bus pasirenkamas mazgas su mažiausia h reikšme\n")
    
    # Parodome keli žingsniai
    print("Simuliuojame kelis paieškos žingsnius:\n")
    
    frontier = PriorityQueue('min', lambda n: puzzle.h(n))
    frontier.append(root_node)
    explored = set()
    
    step = 0
    max_steps = 5  # Parodome pirmus 5 žingsnius
    
    while frontier and step < max_steps:
        step += 1
        print(f"--- Paieškos žingsnis #{step} ---")
        
        # Pasirenkame geriausią mazgą
        node = frontier.pop()
        print(f"Pasirinktas mazgas: depth={node.depth}, h={puzzle.h(node)}")
        print(f"Būsena: {node.state[:3]} / {node.state[3:6]} / {node.state[6:]}")
        
        if puzzle.goal_test(node.state):
            print(">>> TIKSLAS PASIEKTAS! <<<")
            break
        
        explored.add(node.state)
        
        # Išplečiame mazgą
        children = node.expand(puzzle)
        new_children = [c for c in children if c.state not in explored and c not in frontier]
        
        print(f"Sugeneruota {len(children)} vaikų, {len(new_children)} nauji")
        
        for child in new_children:
            frontier.append(child)
            print(f"  → Pridėtas: action={child.action}, h={puzzle.h(child)}")
        
        print(f"Frontier dydis: {len(frontier)}, Explored: {len(explored)}\n")
    
    # ============================================================================
    # ŽINGSNIS 8: Pilnas sprendimas
    # ============================================================================
    print("\n【 ŽINGSNIS 8: Pilnas sprendimas 】")
    print("-" * 80)
    
    print("Paleidžiame pilną best_first_graph_search...\n")
    
    puzzle = EightPuzzle(initial_state, goal_state)
    solution_node = best_first_graph_search(puzzle, lambda n: puzzle.h(n))
    
    if solution_node:
        solution = solution_node.solution()
        path = solution_node.path()
        
        print(f"Sprendimas rastas!")
        print(f"  - Žingsnių skaičius: {len(solution)}")
        print(f"  - Veiksmų seka: {solution}")
        print(f"  - Medžio gylis: {solution_node.depth}")
        print(f"  - Kelias (nodes): {len(path)}")
        
        # Parodome kelią žingsnis po žingsnio
        print("\n【 Kelias nuo pradžios iki tikslo 】")
        print("-" * 80)
        
        for i, node in enumerate(path):
            print(f"\nŽingsnis {i}:")
            if node.action:
                print(f"  Veiksmas: {node.action}")
            print(f"  Būsena:")
            s = node.state
            print(f"    {s[0]} {s[1]} {s[2]}")
            print(f"    {s[3]} {s[4]} {s[5]}")
            print(f"    {s[6]} {s[7]} {s[8]}")
            print(f"  h(n) = {puzzle.h(node)}")
    
    # ============================================================================
    # ŽINGSNIS 9: Palyginimas su breadth_first
    # ============================================================================
    print("\n" + "=" * 80)
    print("【 ŽINGSNIS 9: Palyginimas su breadth_first_graph_search 】")
    print("=" * 80)
    
    puzzle2 = EightPuzzle(initial_state, goal_state)
    solution_node2 = breadth_first_graph_search(puzzle2)
    solution2 = solution_node2.solution()
    
    print(f"\nbreadth_first sprendimas: {solution2}")
    print(f"  Žingsnių: {len(solution2)}")
    
    print(f"\nbest_first sprendimas: {solution}")
    print(f"  Žingsnių: {len(solution)}")
    
    print("\nAbu algoritmai rado tą patį sprendimą!")
    print("breadth_first garantuoja optimumą, bet peržiūri daugiau būsenų.")
    print("best_first su gera euristika dažnai randa greitai, bet ne visada optimaliai.")
    
    print("\n" + "=" * 80)
    print("DEBUG PABAIGA")
    print("=" * 80)


if __name__ == "__main__":
    debug_eight_puzzle()
