from puzzle import *
from planning_utils import *
import heapq
import datetime


def a_star(puzzle, alpha: float = 1):
    '''
    apply a_star to a given puzzle
    :param puzzle: the puzzle to solve
    :return: a dictionary mapping state (as strings) to the action that should be taken (also a string)
    '''

    # general remark - to obtain hashable keys, instead of using State objects as keys, use state.as_string() since
    # these are immutable.

    initial = puzzle.start_state
    goal = puzzle.goal_state

    # this is the heuristic function for of the start state
    initial_to_goal_heuristic = initial.get_manhattan_distance(goal)

    # the fringe is the queue to pop items from
    fringe = [(initial_to_goal_heuristic, initial)]
    # concluded contains states that were already resolved
    concluded = set()
    # a mapping from state (as a string) to the currently minimal distance (int).
    distances = {initial.to_string(): 0}
    # the return value of the algorithm, a mapping from a state (as a string) to the state leading to it (NOT as string)
    # that achieves the minimal distance to the starting state of puzzle.
    prev = {initial.to_string(): None}

    while len(fringe) > 0:
        current_priority, current_item = heapq.heappop(fringe)
        if current_item.to_string() not in concluded:
            concluded.add(current_item.to_string())
            current_priority = current_priority - alpha * current_item.get_manhattan_distance(goal) \
                if len(fringe) != 0 else current_priority
            if current_item == goal:
                break
            for action in current_item.get_actions():
                next_state = current_item.apply_action(action)
                next_dist = current_priority + 1
                if next_state.to_string() not in distances.keys() or distances[next_state.to_string()] > next_dist:
                    distances[next_state.to_string()] = next_dist
                    prev[next_state.to_string()] = (current_item, action)
                    heapq.heappush(fringe, (next_dist + alpha * next_state.get_manhattan_distance(goal), next_state))
    return prev


def solve(puzzle):
    # compute mapping to previous using dijkstra
    prev_mapping = a_star(puzzle, 1)
    # extract the state-action sequence
    plan = traverse(puzzle.goal_state, prev_mapping)
    print_plan(plan)
    print(f'expanded nodes = {len(prev_mapping.keys())}')
    return plan


if __name__ == '__main__':
    # we create some start and goal states. the number of actions between them is 25 although a shorter plan of
    # length 19 exists (make sure your plan is of the same length)
    initial_state = State()
    case = 1
    if case == 1:
        actions = [
            'r', 'r', 'd', 'l', 'u', 'l', 'd', 'd', 'r', 'r', 'u', 'l', 'd', 'r', 'u', 'u', 'l', 'd', 'l', 'd', 'r', 'r',
            'u', 'l', 'u'
        ]
    elif case == 2:
        print('Harder puzzle:')
        actions = [
            'r', 'r', 'd', 'l', 'u', 'l', 'd', 'd', 'r', 'r', 'u', 'l', 'd', 'r', 'u', 'u', 'l', 'd', 'l', 'd', 'r',
            'r',
            'u', 'l', 'u', 'l', 'd', 'd', 'r', 'u', 'l', 'd', 'r', 'r', 'u'
        ]
    else:
        actions = []
    goal_state = initial_state
    for a in actions:
        goal_state = goal_state.apply_action(a)
    puzzle = Puzzle(initial_state, goal_state)
    print('original number of actions:{}'.format(len(actions)))
    solution_start_time = datetime.datetime.now()
    solve(puzzle)
    print('time to solve {}'.format(datetime.datetime.now()-solution_start_time))
