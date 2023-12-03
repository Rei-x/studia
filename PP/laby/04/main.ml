type 'a tree3 = None | Node of 'a * 'a tree3 * 'a tree3 * 'a tree3

let rec mapTree3 t f =
  match t with
  | None -> None
  | Node (x, l, m, r) -> Node (f x, mapTree3 l f, mapTree3 m f, mapTree3 r f)

type 'a fileOrDir = File of string * 'a | Dir of string * 'a fileOrDir list
type 'a disk = Disk of string * 'a fileOrDir list

let disk2 = Disk ("C", [ Dir ("Users", [ File ("me.txt", 2) ]) ])
