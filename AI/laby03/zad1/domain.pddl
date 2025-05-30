(define (domain transport-logistics)
  (:requirements 
    :strips 
    :typing 
    :negative-preconditions 
    :equality
  )

  (:types
    package
    location
    vehicle
    transport-mode - object

    university - location     ; University locations
    drone      - vehicle      ; Drone vehicles
    student    - vehicle      ; Student vehicles
  )

  (:constants
    road - transport-mode
    air  - transport-mode
  )

  (:predicates
    ; Object (package or vehicle) is at location
    (at ?obj - (either package vehicle) ?loc - location)
    
    ; Package is loaded in vehicle
    (in ?pkg - package ?veh - vehicle)
    
    ; Locations are connected by transport mode
    (connected ?loc1 - location ?loc2 - location ?mode - transport-mode)
    
    ; Vehicle can use transport mode
    (can-use ?veh - vehicle ?mode - transport-mode)
  )

  ; ================================
  ; ACTIONS
  ; ================================

  (:action load-package
    :parameters (?pkg - package 
                 ?veh - vehicle 
                 ?loc - location)
    :precondition (and
      (at ?pkg ?loc)
      (at ?veh ?loc)
    )
    :effect (and
      (in ?pkg ?veh)
      (not (at ?pkg ?loc))
    )
  )

  (:action unload-package
    :parameters (?pkg - package 
                 ?veh - vehicle 
                 ?loc - location)
    :precondition (and
      (in ?pkg ?veh)
      (at ?veh ?loc)
    )
    :effect (and
      (at ?pkg ?loc)
      (not (in ?pkg ?veh))
    )
  )

  (:action move-vehicle
    :parameters (?veh - vehicle 
                 ?from - location 
                 ?to - location 
                 ?mode - transport-mode)
    :precondition (and
      (at ?veh ?from)
      (connected ?from ?to ?mode)
      (can-use ?veh ?mode)
      (not (= ?from ?to))
    )
    :effect (and
      (at ?veh ?to)
      (not (at ?veh ?from))
    )
  )
)