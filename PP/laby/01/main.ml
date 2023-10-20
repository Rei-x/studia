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
