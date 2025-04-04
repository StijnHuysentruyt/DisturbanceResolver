from unified_planning.shortcuts import *

def create_data():

    Resource = UserType('Resource')

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

    cnn_cell_robot = unified_planning.model.Fluent('cnn/cell/robot', BoolType(), l_from=Cell, l_to=Robot)
    cnn_robot_gripper = unified_planning.model.Fluent('cnn/robot/gripper', BoolType(), l_from=Robot, l_to=RobotGripper)
    cnn_twh_gripper = unified_planning.model.Fluent('cnn/twh/gripper', BoolType(), l_from=ToolWarehouseAddon, l_to=RobotGripper)
    cnn_cell_addon = unified_planning.model.Fluent('cnn/cell/addon', BoolType(), l_from=Cell, l_to=Addon)
    cnn_trayaddon_cp = unified_planning.model.Fluent('cnn/trayaddon/cp', BoolType(), l_from=TrayAddon, l_to=CarrierPlate)
    cnn_cp_tray = unified_planning.model.Fluent('cnn/cp/tray', BoolType(), l_from=CarrierPlate, l_to=Tray)
    cnn_tray_rh = unified_planning.model.Fluent('cnn/tray/rh', BoolType(), l_from=Tray, l_to=Rotorhousing)
    cnn_tray_r2 = unified_planning.model.Fluent('cnn/tray/r2', BoolType(), l_from=Tray, l_to=Rotor2)
    cnn_rh_r2 = unified_planning.model.Fluent('cnn/rh/r2', BoolType(), l_from=Rotorhousing, l_to=Rotor2)

    def pick_gripper():
        move = InstantaneousAction('pick-gripper', 
                                   pC=Cell, 
                                   pR=Robot,  
                                   pTwh=ToolWarehouseAddon, 
                                   pG=RobotGripper)
           
        
        pC = move.parameter('pC')
        pR = move.parameter('pR')
        pTwh = move.parameter('pTwh')
        pG = move.parameter('pG')

        move.add_precondition(cnn_cell_robot(pC, pR))
        move.add_precondition(cnn_cell_addon(pC, pTwh))
        move.add_precondition(cnn_twh_gripper(pTwh, pG))

        move.add_effect(cnn_twh_gripper(pTwh, pG), False)
        move.add_effect(cnn_robot_gripper(pR, pG), True)

        return move

    def move():
        move = InstantaneousAction('move', 
            pC=Cell, 
            pR=Robot,  
            pG=RobotGripper,
            pA=TrayAddon, 
            pCP = CarrierPlate,
            pT=Tray, 
            pRh=Rotorhousing, 
            pR2=Rotor2)
        
        pC = move.parameter('pC')
        pR = move.parameter('pR')
        pG = move.parameter('pG')
        pA = move.parameter('pA')
        pCP = move.parameter('pCP')
        pT = move.parameter('pT')
        pRh = move.parameter('pRh')
        pR2 = move.parameter('pR2')


        
        move.add_precondition(cnn_cell_robot(pC, pR))
        move.add_precondition(cnn_robot_gripper(pR, pG))
        move.add_precondition(cnn_cell_addon(pC, pA))
        move.add_precondition(cnn_trayaddon_cp(pA, pCP))
        move.add_precondition(cnn_cp_tray(pCP, pT))
        move.add_precondition(cnn_tray_rh(pT, pRh))
        move.add_precondition(cnn_tray_r2(pT, pR2))

        move.add_effect(cnn_tray_r2(pT, pR2), False)
        move.add_effect(cnn_rh_r2(pRh, pR2), True)

        return move

    def create_init():

        objects = []

        oCell = Object('Cell1',Cell)
        objects.append(oCell)

        oStaubli = Object('Staubli1', Staubli)
        objects.append(oStaubli)

        oToolWarehouseAddon = Object('ToolWarehouseAddon1', ToolWarehouseAddon)
        objects.append(oToolWarehouseAddon)
        oTrayAddon = Object('TrayAddon1', TrayAddon)
        objects.append(oTrayAddon)

        oCarrierPlate = Object('CarrierPlate1', CarrierPlate)
        objects.append(oCarrierPlate)

        oTray = Object('Tray1', Tray)
        objects.append(oTray)

        oRotorhousing = Object('Rotorhousing1', Rotorhousing)
        objects.append(oRotorhousing)

        oRotor2 = Object('Rotor21', Rotor2)
        objects.append(oRotor2)

        oThreeFingerGripper = Object('ThreeFingerGripper1', ThreeFingerGripper)
        objects.append(oThreeFingerGripper)

        inits = []
        inits.append(cnn_cell_robot(oCell, oStaubli))
        inits.append(cnn_cell_addon(oCell, oToolWarehouseAddon))
        inits.append(cnn_twh_gripper(oToolWarehouseAddon,oThreeFingerGripper))
        
        inits.append(cnn_cell_addon(oCell, oTrayAddon))
        inits.append(cnn_trayaddon_cp(oTrayAddon, oCarrierPlate))
        inits.append(cnn_cp_tray(oCarrierPlate, oTray))
        inits.append(cnn_tray_rh(oTray,oRotorhousing))
        inits.append(cnn_tray_r2(oTray,oRotor2))

        goals = []
        #goals.append(cnn_robot_gripper(oStaubli, oThreeFingerGripper))
        goals.append(cnn_rh_r2(oRotorhousing,oRotor2))

        return objects, inits, goals

    problem = Problem('robot')
    problem.add_fluent(connected, default_initial_value=False)
    problem.add_fluent(cnn_cell_robot, default_initial_value=False)
    problem.add_fluent(cnn_robot_gripper, default_initial_value=False)
    problem.add_fluent(cnn_twh_gripper, default_initial_value=False)
    problem.add_fluent(cnn_cell_addon, default_initial_value=False)
    problem.add_fluent(cnn_trayaddon_cp, default_initial_value=False)
    problem.add_fluent(cnn_cp_tray, default_initial_value=False)
    problem.add_fluent(cnn_tray_rh, default_initial_value=False)
    problem.add_fluent(cnn_tray_r2, default_initial_value=False)
    problem.add_fluent(cnn_rh_r2, default_initial_value=False)

    problem.add_action(move())
    problem.add_action(pick_gripper())

    objects, inits, goals = create_init()
    problem.add_objects(objects)
    for init in inits:
        problem.set_initial_value(init, True)
    for goal in goals:
        problem.add_goal(goal)

    return problem
