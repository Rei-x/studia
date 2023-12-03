let f1 x y z = x y z

type 'a bt = Empty | Node of 'a * 'a bt * 'a bt

let breadthBT tree =
  let rec breadthBTAux internalTree =
    match internalTree with
    | [] -> []
    | Empty :: tail -> breadthBTAux tail
    | Node (value, left, right) :: tail ->
        value :: breadthBTAux (tail @ [ left; right ])
  in
  breadthBTAux [ tree ]

let internalBT tree =
  let rec internalBTAux t acc =
    match t with
    | Empty -> 0
    | Node (_, Empty, Empty) -> acc
    | Node (_, left, Empty) -> acc + internalBTAux left (acc + 1)
    | Node (_, Empty, right) -> acc + internalBTAux right (acc + 1)
    | Node (_, right, left) ->
        acc + internalBTAux right (acc + 1) + internalBTAux left (acc + 1)
  in
  internalBTAux tree 0

let externalBT tree =
  let rec externalBTAux t acc =
    match t with
    | Empty -> acc
    | Node (_, Empty, Empty) -> 2 * (acc + 1)
    | Node (_, left, Empty) -> externalBTAux left (acc + 1) + acc + 1
    | Node (_, Empty, right) -> acc + 1 + externalBTAux right (acc + 1)
    | Node (_, left, right) ->
        externalBTAux left (acc + 1) + externalBTAux right (acc + 1)
  in
  externalBTAux tree 0

type 'a graph = Graph of ('a -> 'a list)

let depthSearch (Graph graph) n =
  let rec depthSearchAux visited = function
    | [] -> []
    | head :: tail ->
        if List.mem head visited then depthSearchAux visited tail
        else head :: depthSearchAux (head :: visited) (graph head @ tail)
  in
  depthSearchAux [] [ n ]
