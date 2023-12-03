let f1 x = x 2 2
let f2 x y z = x (y ^ z)
let curry3 f a b c = f (a, b, c)
let uncurry3 f (a, b, c) = f a b c

let rec quicksort = function
  | [] -> []
  | [ x ] -> [ x ]
  | xs ->
      let small = List.filter (fun y -> y < List.hd xs) xs
      and pivot = List.hd xs
      and large = List.filter (fun y -> y > List.hd xs) xs in
      quicksort small @ (pivot :: quicksort large)

let rec quicksort2 = function
  | [] -> []
  | x :: xs ->
      let small = List.filter (fun y -> y < x) xs
      and large = List.filter (fun y -> y > x) xs in
      quicksort2 small @ (x :: quicksort2 large)

let rec insertionsort f arr =
  match arr with
  | [] -> []
  | x :: xs ->
      let rec insert x = function
        | [] -> [ x ]
        | y :: ys -> if f x y then x :: y :: ys else y :: insert x ys
      in
      insert x (insertionsort f xs)
