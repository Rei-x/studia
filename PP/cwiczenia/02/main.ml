(* evenR dla ocamla będzie 1 wywołanie, dla scali 4 *)

let rec fib n = if n = 0 || n = 1 then n else fib (n - 1) + fib (n - 2)

let fib_tail n =
  let rec fib_tail_rec n a b =
    if n = 0 then a else fib_tail_rec (n - 1) b (a + b)
  in
  fib_tail_rec n 0 1

let rec replace_nth (xs, n, x) =
  match xs with
  | [] -> []
  | _ :: next when n = 0 -> x :: next
  | head :: next -> head :: replace_nth (next, n - 1, x)

let zwiaznie1 = match [ -2; -1; 0; 1; 2 ] with _ :: _ :: x :: _ -> x | _ -> 0
let zwiazanie2 = match [ (1, 2); (0, 1) ] with _ :: (x, _) :: _ -> x | _ -> 0

let rec initSegment (startList, endList) =
  match (startList, endList) with
  | [], _ -> true
  | _, [] -> false
  | x :: xs, y :: ys -> x = y && initSegment (xs, ys)
