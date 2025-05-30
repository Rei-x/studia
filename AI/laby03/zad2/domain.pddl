(define (domain robot-world)
    (:requirements :strips :typing)
    (:types room robot)
    (:predicates
        (at ?r - robot ?p - room)
        (dirty ?p - room)
        (clean ?p - room)
    )
    (:action move
        :parameters (?r - robot ?from ?to - room)
        :precondition (at ?r ?from)
        :effect (and (not (at ?r ?from)) (at ?r ?to))
    )
    (:action clean
        :parameters (?r - robot ?p - room)
        :precondition (and (dirty ?p) (at ?r ?p))
        :effect (and (not (dirty ?p)) (clean ?p))
    )
)