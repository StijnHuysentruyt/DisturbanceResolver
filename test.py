from unified_planning.shortcuts import *

Location = UserType('Location')
robot_at = unified_planning.model.Fluent('robot_at', BoolType(), l=Location)
connected = unified_planning.model.Fluent('connected', BoolType(), l_from=Location, l_to=Location)

move = InstantaneousAction('move', l_from=Location, l_to=Location)
l_from = move.parameter('l_from')
l_to = move.parameter('l_to')
move.add_precondition(connected(l_from, l_to))
move.add_precondition(robot_at(l_from))
move.add_effect(robot_at(l_from), False)
move.add_effect(robot_at(l_to), True)

problem = Problem('robot')
problem.add_fluent(robot_at, default_initial_value=False)
problem.add_fluent(connected, default_initial_value=False)
problem.add_action(move)

NLOC = 10
locations = [Object('l%s' % i, Location) for i in range(NLOC)]
problem.add_objects(locations)

problem.set_initial_value(robot_at(locations[0]), True)
for i in range(NLOC - 1):
    problem.set_initial_value(connected(locations[i], locations[i+1]), True)
problem.add_goal(robot_at(locations[-1]))

with OneshotPlanner(name='pyperplan') as planner:
    result = planner.solve(problem)
    if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
        print("Pyperplan returned: %s" % result.plan)
    else:
        print("No plan found.")

with OneshotPlanner(problem_kind=problem.kind) as planner:
    result = planner.solve(problem)
    print("%s returned: %s" % (planner.name, result.plan))

with OneshotPlanner(names=['tamer', 'tamer', 'pyperplan'],
                    params=[{'heuristic': 'hadd'}, {'heuristic': 'hmax'}, {}]) as planner:
    plan = planner.solve(problem).plan
    print("%s returned: %s" % (planner.name, plan))