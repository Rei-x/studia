let cutAndMend (a, b) xs =
  let rec cutAndMendAux xs current =
    match (xs, current) with
    | _ :: xs, index when index >= a && index <= b ->
        cutAndMendAux xs (current + 1)
    | x :: xs, _ -> x :: cutAndMendAux xs (current + 1)
    | [], _ -> []
  in
  cutAndMendAux xs 0

let rec split2Rec xs =
  match xs with
  | x :: y :: xs ->
      let xs1, xs2 = split2Rec xs in
      (x :: xs1, y :: xs2)
  | _ -> ([], [])

let split2Tail xs =
  let rec split2TailAux xs xs1 xs2 =
    match xs with
    | x :: y :: xs -> split2TailAux xs (x :: xs1) (y :: xs2)
    | _ -> (xs1, xs2)
  in
  split2TailAux xs [] []
