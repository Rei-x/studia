(define (problem robot-move-problem)
    (:domain robot-world)
    (:objects
        pokoj1 pokoj2 pokoj3 - room
        robby - robot
    )
    (:init
        (at robby pokoj1)
        (dirty pokoj1)
        (dirty pokoj2)
        (dirty pokoj3)
    )
    (:goal (and (clean pokoj1) (clean pokoj2) (clean
pokoj3)))
)