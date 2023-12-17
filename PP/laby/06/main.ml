(* def fibonacciImperative(n: Int): Int = {
     var firstFib = 1
     var secondFib = 1
     var i = 2
     while (i < n) {
       val newFib = firstFib + secondFib
       firstFib = secondFib
       secondFib = newFib
       i += 1
     }
     return secondFib
   }

   def imperacci(n: Int, m: Int): Array[Int] = {
     var result = Array.ofDim[Int](m);

     var helperIndex = 0

     var currentResultIndex = 0
     while (currentResultIndex < m) {
       if (helperIndex % 2 == 1) {
         result(currentResultIndex) = fibonacciImperative(helperIndex + n - 1);
         currentResultIndex += 1
       }
       helperIndex += 1
     }

     result
   } *)

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
