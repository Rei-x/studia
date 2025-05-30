(define (problem transport-task-politechniki)
  (:domain transport-logistics)

  (:objects
    ; Universities
    pwr - university          ; Politechnika Wrocławska
    agh - university          ; AGH Kraków  
    pw  - university          ; Politechnika Warszawska
    
    ; Packages to transport
    gpu1 - package            ; Graphics card 1
    gpu2 - package            ; Graphics card 2

    ; Vehicles
    dron_pwr    - drone       ; Drone from Wrocław
    student_agh - student     ; Student from AGH
  )

  (:init
    ; ================================
    ; INITIAL LOCATIONS
    ; ================================
    
    ; Package locations
    (at gpu1 pwr)             ; GPU 1 starts at Wrocław Tech
    (at gpu2 pwr)             ; GPU 2 starts at Wrocław Tech

    ; Vehicle locations  
    (at dron_pwr pwr)         ; Drone starts at Wrocław
    (at student_agh agh)      ; Student starts at AGH

    ; ================================
    ; LOCATION CONNECTIONS
    ; ================================
    
    ; Road connections (bidirectional)
    (connected pwr agh road)
    (connected agh pwr road)
    (connected agh pw road)
    (connected pw agh road)
    (connected pwr pw road)
    (connected pw pwr road)

    ; Air connections (bidirectional)
    (connected pwr agh air)
    (connected agh pwr air)
    (connected agh pw air)
    (connected pw agh air)
    (connected pwr pw air)
    (connected pw pwr air)

    ; ================================
    ; VEHICLE CAPABILITIES
    ; ================================
    
    (can-use dron_pwr air)     ; Drone can fly
    (can-use student_agh road) ; Student travels by road
  )

  (:goal
    (and
      (at gpu1 pw)           ; Graphics card 1 → Warsaw Tech
      (at gpu2 agh)          ; Graphics card 2 → AGH Kraków
    )
  )
)