from unified_planning.shortcuts import *

from axl import *
problem = create_data()

with OneshotPlanner(problem_kind=problem.kind) as planner:
    result = planner.solve(problem)
    print("%s returned: %s" % (planner.name, result.plan))