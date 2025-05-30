(define (domain ball-moving-robot)
  
  (:requirements :strips :typing)
  
  (:types 
    robot room ball arm
  )
  
  (:predicates
    (at ?r - robot ?room - room)
    (inroom ?b - ball ?room - room)
    (holding ?a - arm ?b - ball)
    (arm-empty ?a - arm)
  )
  
  (:action move
    :parameters (?r - robot ?from - room ?to - room)
    :precondition (at ?r ?from)
    :effect (and 
      (not (at ?r ?from)) 
      (at ?r ?to)
    )
  )
  
  (:action pick-up
    :parameters (?r - robot ?a - arm ?b - ball ?room - room)
    :precondition (and 
      (at ?r ?room) 
      (inroom ?b ?room) 
      (arm-empty ?a)
    )
    :effect (and 
      (holding ?a ?b) 
      (not (arm-empty ?a)) 
      (not (inroom ?b ?room))
    )
  )
  
  (:action put-down
    :parameters (?r - robot ?a - arm ?b - ball ?room - room)
    :precondition (and 
      (at ?r ?room) 
      (holding ?a ?b)
    )
    :effect (and 
      (inroom ?b ?room) 
      (arm-empty ?a) 
      (not (holding ?a ?b))
    )
  )
)