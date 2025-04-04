(define (domain hanoi)
    (:requirements :strips)
    (:predicates 
        (cp ?x)
        (tray ?x)
        (rotorhousing ?x)
        (rotor2 ?x)
        (rotor1 ?x)
        (cnn ?a ?b)
    )
    
    (:action insertRotor2
        :parameters (?cp ?t ?rh ?r)
        :precondition (
            and 
            (cp ?cp)
            (tray ?t)
            (rotorhousing ?rh)
            (rotor2 ?r)
            (cnn ?cp ?t)
            (cnn ?t ?rh)
            (cnn ?t ?r)
        )
        :effect  (
            and 
                (cnn ?rh ?r)
                (not (cnn ?t ?r))
        )
    )
    
    (:action insertRotor1
        :parameters (?cp ?t ?rh ?r2 ?r1)
        :precondition (
            and 
            (cp ?cp)
            (tray ?t)
            (rotorhousing ?rh)
            (rotor2 ?r2)
            (rotor1 ?r1)
            (cnn ?cp ?t)
            (cnn ?t ?rh)
            (cnn ?rh ?r2)
            (cnn ?t ?r1)
        )
        :effect  (
            and 
                (cnn ?rh ?r1)
                (not (cnn ?t ?r1))
        )
    )
)