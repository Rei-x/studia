let fibonacciImperative n =
  let firstFib = ref 1 in
  let secondFib = ref 1 in
  let i = ref 2 in
  while !i < n do
    let newFib = !firstFib + !secondFib in
    firstFib := !secondFib;
    secondFib := newFib;
    i := !i + 1
  done;
  !secondFib

let imperacci n m =
  let result = Array.make m 0 in
  let helperIndex = ref 0 in
  let currentResultIndex = ref 0 in
  while !currentResultIndex < m do
    if !helperIndex mod 2 = 1 then (
      result.(!currentResultIndex) <- fibonacciImperative (!helperIndex + n - 1);
      currentResultIndex := !currentResultIndex + 1);
    helperIndex := !helperIndex + 1
  done;
  result

let composites n =
  let numberOfComposites = ref 0 in
  let primes = Array.make (n + 1) true in
  primes.(0) <- false;
  primes.(1) <- false;
  for p = 2 to int_of_float (sqrt (float_of_int n)) do
    if primes.(p) then
      for i = 2 to n / p do
        primes.(i * p) <- false
      done
  done;
  for i = 2 to n do
    if not primes.(i) then numberOfComposites := !numberOfComposites + 1
  done;
  let result = Array.make !numberOfComposites 0 in
  let resultIndex = ref 0 in
  for i = 2 to n do
    if not primes.(i) then (
      result.(!resultIndex) <- i;
      resultIndex := !resultIndex + 1)
  done;
  result
;;

composites 10
