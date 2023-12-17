open OUnit2
(* open Laby05.Main *)

let tests =
  "laby 05 tests"
  >::: [ (* ( "buyTicket" >:: fun _ ->
              let prices =
                [
                  Ticket (lazy (Price "Komputer"));
                  Ticket (lazy (Ticket (lazy (Price "Klocki lego"))));
                  Ticket (lazy (Price "Sanki Zawiszy"));
                ]
              in
              assert_equal (List.nth (buyTicket prices 1) 1) (Price "Klocki lego")
            ); *) ]

let () = run_test_tt_main tests
