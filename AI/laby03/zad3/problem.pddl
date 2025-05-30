(define (problem move-balls)
  (:domain ball-moving-robot)
  
  (:objects
    room1 room2 - room
    robot - robot
    ball1 ball2 ball3 ball4 - ball
    arm1 arm2 - arm
  )
  
  (:init
    (at robot room1)
    (inroom ball1 room1)
    (inroom ball2 room1)
    (inroom ball3 room1)
    (inroom ball4 room1)
    (arm-empty arm1)
    (arm-empty arm2)
  )
  
  (:goal
    (and
      (inroom ball1 room2)
      (inroom ball2 room2)
      (inroom ball3 room2)
      (inroom ball4 room2)
    )
  )
)