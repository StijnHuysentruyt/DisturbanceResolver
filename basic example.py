from unified_planning.shortcuts import *

Resource = UserType('Resource')
Tray = UserType('Tray',Resource)
Rotorhousing = UserType('Rotorhousing',Resource)
Rotor2 = UserType('Rotor2',Resource)

Location = UserType('Location')
connected = unified_planning.model.Fluent('connected', BoolType(), l_from=Resource, l_to=Resource)

move = InstantaneousAction('move', pT=Tray, pRh=Rotorhousing, pR2=Rotor2)
pT = move.parameter('pT')
pRh = move.parameter('pRh')
pR2 = move.parameter('pR2')

move.add_precondition(connected(pT, pRh))
move.add_precondition(connected(pT, pR2))
move.add_effect(connected(pT, pR2), False)
move.add_effect(connected(pRh, pR2), True)

problem = Problem('robot')
problem.add_fluent(connected, default_initial_value=False)
problem.add_action(move)

NLOC = 10

objects = []
objects.append(Object('Tray1',Tray))
objects.append(Object('Rotorhousing1',Rotorhousing))
objects.append(Object('Rotor21',Rotor2))

problem.add_objects(objects)

problem.set_initial_value(connected(objects[0],objects[1]), True)
problem.set_initial_value(connected(objects[0],objects[2]), True)


problem.add_goal(connected(objects[1],objects[2]))

with OneshotPlanner(name='pyperplan') as planner:
    result = planner.solve(problem)
    if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
        print("Pyperplan returned: %s" % result.plan)
    else:
        print("No plan found.")

with OneshotPlanner(problem_kind=problem.kind) as planner:
    result = planner.solve(problem)
    print("%s returned: %s" % (planner.name, result.plan))

with OneshotPlanner(names=['pyperplan']) as planner:
    plan = planner.solve(problem).plan
    print("%s returned: %s" % (planner.name, plan))