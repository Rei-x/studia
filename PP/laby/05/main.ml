type 'a price = Prize of 'a | Ticket of (unit -> 'a price)

let rec buyTicket prices n =
  match prices with
  | [] -> []
  | Ticket p :: t -> if n = 1 then p () :: t else Ticket p :: buyTicket t (n - 1)
  | Prize p :: t -> Prize p :: buyTicket t (n - 1)
;;

let prices =
  [
    Ticket (fun () -> Prize "Komputer");
    Ticket (fun () -> Prize "Klocki lego");
    Ticket (fun () -> Prize "Sanki Zawiszy");
  ]
in
buyTicket prices 2

type 'a lazyPrice = Price of 'a | Ticket of 'a lazyPrice Lazy.t

let rec buyTicketLazy prices n =
  match prices with
  | [] -> []
  | Ticket p :: t ->
      if n = 1 then Lazy.force p :: t else Ticket p :: buyTicketLazy t (n - 1)
  | p :: t -> p :: buyTicketLazy t (n - 1)

let lazyPrices =
  [
    Ticket (lazy (Price "Komputer"));
    Ticket (lazy (Ticket (lazy (Price "Klocki lego"))));
    Ticket (lazy (Price "Sanki Zawiszy"));
  ]
;;

buyTicketLazy lazyPrices 3
