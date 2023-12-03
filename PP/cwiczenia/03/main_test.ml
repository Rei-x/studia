open OUnit2
open Cwiczenia03.Main

let tests =
  "cwiczenia 03 tests"
  >::: [
         ( "quicksort" >:: fun _ ->
           assert_equal (quicksort [ 4; 5; 7; 9; 3 ]) [ 3; 4; 5; 7; 9 ];
           assert_equal (quicksort2 [ 2; 1 ]) [ 1; 2 ] );
       ]

let () = run_test_tt_main tests
