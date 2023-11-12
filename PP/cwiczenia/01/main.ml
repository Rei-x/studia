let rec flatten1 arr =
  if arr = [] then [] else List.hd arr @ flatten1 (List.tl arr)

let rec count (x, xs) =
  if xs = [] then 0
  else (if List.hd xs = x then 1 else 0) + count (x, List.tl xs)

let rec replicate (x, n) = if n = 0 then [] else x :: replicate (x, n - 1)

let rec sqrList xs =
  if xs = [] then [] else (List.hd xs * List.hd xs) :: sqrList (List.tl xs)

let palindrome xs = List.rev xs = xs
let rec listLength xs = if xs = [] then 0 else 1 + listLength (List.tl xs)
