type 'a llist = LNil | LCons of 'a * (unit -> 'a llist)

let rec lfrom k = LCons (k, function () -> lfrom (k + 1))

let rec toLazyList xs =
  match xs with [] -> LNil | h :: t -> LCons (h, function () -> toLazyList t)

type price = Price of string | HiddenPrice of (unit -> string)

let rec buyTicket prices n =
  match prices with
  | [] -> []
  | HiddenPrice p :: t ->
      if n = 0 then Price (p ()) :: t else HiddenPrice p :: buyTicket t (n - 1)
  | Price p :: t -> Price p :: buyTicket t (n - 1)
;;

let prices =
  [
    HiddenPrice (fun () -> "Komputer");
    HiddenPrice (fun () -> "Klocki lego");
    HiddenPrice (fun () -> "Sanki Zawiszy");
  ]
in
buyTicket prices 2
