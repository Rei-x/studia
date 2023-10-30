let reverse4 (a, b, c, d) = (d, c, b, a)

let rec sumProd (s, e) =
  if s >= e then (0, 1)
  else
    let sum, prod = sumProd (s + 1, e) in
    (sum + s, prod * s)

let rec sumDivisors (checkedNumber, currentNumber) =
  if currentNumber = 0 then 0
  else if checkedNumber mod currentNumber = 0 then
    currentNumber + sumDivisors (checkedNumber, currentNumber - 1)
  else sumDivisors (checkedNumber, currentNumber - 1)

let isPerfect n = if n <= 1 then false else sumDivisors (n, n / 2) = n

let rec insert (arr, element, index) =
  if index = 0 then element :: arr
  else if arr = [] then [ element ]
  else List.hd arr :: insert (List.tl arr, element, index - 1)

(* def findmax(
       xs: List[Int],
       currentMax: Int,
       currentIndex: Int
   ): (List[Int], Int) = {
     if (xs.length == 0) then (List(), currentMax)
     else {
       val (indexes, max) = findmax(xs.tail, currentMax, currentIndex + 1)
       if (xs.head > max) then (List(currentIndex), xs.head)
       else if (xs.head == max) then (currentIndex :: indexes, max)
       else (indexes, max)
     }
   }

   def argmax(xs: List[Int]): List[Int] = {
     findmax(xs, xs.head, 0)._1
   } *)

let rec findMax (xs, currentMax, currentIndex) =
  if xs = [] then ([], currentMax)
  else
    let indexes, max = findMax (List.tl xs, currentMax, currentIndex + 1) in
    if List.hd xs > max then ([ currentIndex ], List.hd xs)
    else if List.hd xs = max then (currentIndex :: indexes, max)
    else (indexes, max)

let argMax xs = if xs = [] then [] else findMax (xs, List.hd xs, 0) |> fst
