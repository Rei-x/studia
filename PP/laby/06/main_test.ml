open OUnit2
open Laby06.Main

let tests =
  "laby 06 tests"
  >::: [
         ( "imperacci" >:: fun _ ->
           assert_equal (imperacci 2 10)
             [| 1; 3; 8; 21; 55; 144; 377; 987; 2584; 6765 |];
           assert_equal (imperacci 1 10)
             [| 1; 2; 5; 13; 34; 89; 233; 610; 1597; 4181 |] );
       ]

let () = run_test_tt_main tests
