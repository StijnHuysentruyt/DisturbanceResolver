from unified_planning.shortcuts import *

def create_data():

    Resource = UserType('Resource')


    Class = UserType('ResourceClass', Resource)
    rcCell = UserType('rc: cell', Class)
    rcAddon = UserType('rc: addon', Class)

    Definition = UserType('ResourceDefinition', Resource)




    Cell = UserType('Cell',Resource)
    
    Robot = UserType('Robot',Resource)
    ArticulatedRobot = UserType('ArticulatedRobot',Robot)
    Staubli = UserType('Staubli',ArticulatedRobot)

    Addon = UserType('Addon', Resource)
    TrayAddon = UserType('TrayAddon', Addon)
    ToolWarehouseAddon = UserType('ToolWarehouseAddon',Addon)

    CarrierPlate = UserType('CarrierPlate', Resource)
    
    Tray = UserType('Tray',Resource)
    Rotorhousing = UserType('Rotorhousing',Resource)
    Rotor2 = UserType('Rotor2',Resource)

    RobotGripper = UserType('Gripper',Resource)
    ThreeFingerGripper = UserType("ThreeFingerGripper",RobotGripper)
    ParallellGripper = UserType("ParallellGripper",RobotGripper)

    connected = unified_planning.model.Fluent('connected', BoolType(), l_from=Resource, l_to=Resource)


    isCell = Fluent('is-cell', BoolType(), r=Resource)
    isRobot = Fluent('is-robot', BoolType(), r=Resource)
    isGripper = Fluent('is-gripper', BoolType(), r=Resource)

    cnn_cell_addon = unified_planning.model.Fluent('cnn/cell/addon', BoolType(), l_from=Resource, l_to=Resource)
    cnn_cell_robot = unified_planning.model.Fluent('cnn/cell/robot', BoolType(), l_from=Resource, l_to=Resource)
    cnn_robot_gripper = unified_planning.model.Fluent('cnn/robot/gripper', BoolType(), l_from=Resource, l_to=Resource)
    cnn_twh_gripper = unified_planning.model.Fluent('cnn/twh/gripper', BoolType(), l_from=Resource, l_to=Resource)


    def pick_gripper_2():
        move = InstantaneousAction('pick-gripper', 
                                   pC=Resource, 
                                   pR=Resource,  
                                   pTwh=ToolWarehouseAddon, 
                                   pG=Resource)
           
        pC = move.parameter('pC')
        pR = move.parameter('pR')
        pTwh = move.parameter('pTwh')
        pG = move.parameter('pG')

        move.add_precondition(isCell(pC))
        move.add_precondition(isRobot(pR))
        move.add_precondition(isGripper(pG))

        move.add_precondition(cnn_cell_robot(pC, pR))
        move.add_precondition(cnn_cell_addon(pC, pTwh))
        move.add_precondition(cnn_twh_gripper(pTwh, pG))

        move.add_effect(cnn_twh_gripper(pTwh, pG), False)
        move.add_effect(cnn_robot_gripper(pR, pG), True)

        return move

    def create_init():

        objects = []

        oCell = Object('Cell1',Cell)
        objects.append(oCell)

        oStaubli = Object('Staubli1', Staubli)
        objects.append(oStaubli)

        oToolWarehouseAddon = Object('ToolWarehouseAddon1', ToolWarehouseAddon)
        objects.append(oToolWarehouseAddon)

    
        oThreeFingerGripper = Object('ThreeFingerGripper1', ThreeFingerGripper)
        objects.append(oThreeFingerGripper)

        inits = []
        inits.append(cnn_cell_robot(oCell, oStaubli))
        inits.append(cnn_cell_addon(oCell, oToolWarehouseAddon))
        inits.append(cnn_twh_gripper(oToolWarehouseAddon,oThreeFingerGripper))
        
        inits.append(isCell(oCell))
        inits.append(isRobot(oStaubli))
        inits.append(isGripper(oThreeFingerGripper))

        goals = []
        goals.append(cnn_robot_gripper(oStaubli, oThreeFingerGripper))
        #goals.append(cnn_rh_r2(oRotorhousing,oRotor2))

        return objects, inits, goals

    problem = Problem('robot')
    problem.add_fluent(isGripper, default_initial_value=False)
    problem.add_fluent(isCell, default_initial_value=False)
    problem.add_fluent(isRobot, default_initial_value=False)
    problem.add_fluent(connected, default_initial_value=False)
    problem.add_fluent(cnn_cell_robot, default_initial_value=False)
    problem.add_fluent(cnn_robot_gripper, default_initial_value=False)
    problem.add_fluent(cnn_twh_gripper, default_initial_value=False)
    problem.add_fluent(cnn_cell_addon, default_initial_value=False)

    problem.add_action(pick_gripper_2())

    objects, inits, goals = create_init()
    problem.add_objects(objects)
    for init in inits:
        problem.set_initial_value(init, True)
    for goal in goals:
        problem.add_goal(goal)

    return problem
