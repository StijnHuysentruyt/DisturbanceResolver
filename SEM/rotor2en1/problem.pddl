(define (problem hanoi4)
  (:domain hanoi)
  (:objects 
    cp1
    tray1
    rh
    r2
    r1
  )
  (:init 
    (cp cp1)
    (tray tray1)
    (rotorhousing rh)
    (rotor2 r2)
    (rotor1 r1)
    (cnn cp1 tray1)
    (cnn tray1 rh)
    (cnn tray1 r2)
    (cnn tray1 r1)
  )
  
  (:goal 
    (and 
      (cnn rh r2)
      (cnn rh r1)
    )
  )
  
)