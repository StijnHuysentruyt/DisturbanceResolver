# wget https://raw.githubusercontent.com/aiplan4eu/unified-planning/master/unified_planning/test/pddl/counters/domain.pddl -O /tmp/counters_domain.pddl
# wget https://raw.githubusercontent.com/aiplan4eu/unified-planning/master/unified_planning/test/pddl/counters/problem.pddl -O /tmp/counters_problem.pddl

from unified_planning.shortcuts import *
from unified_planning.io import PDDLReader, PDDLWriter

reader = PDDLReader()
problem = reader.parse_problem(domain_filename='SEM2/domain.pddl', problem_filename='SEM2/problem.pddl')
#problem = reader.parse_problem(domain_filename='Hanoi/domain.pddl', problem_filename='Hanoi/problem.pddl')
print(problem)

with OneshotPlanner(names=['tamer', 'tamer'],
                    params=[{'heuristic': 'hadd'}, {'heuristic': 'hmax'}]) as planner:
    plan = planner.solve(problem).plan
    print("%s returned: %s" % (planner.name, plan))