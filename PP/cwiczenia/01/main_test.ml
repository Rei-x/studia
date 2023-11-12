open OUnit2
open Cwiczenia01.Main

let tests =
  "cwiczenia 01 tests"
  >::: [
         ( "flatten1" >:: fun _ ->
           assert_equal [ 1; 2; 3; 4; 5 ]
             (flatten1 [ [ 1; 2 ]; [ 3; 4 ]; [ 5 ] ]) );
         ("count" >:: fun _ -> assert_equal 3 (count (1, [ 1; 1; 3; 4; 1 ])));
         ( "replicate" >:: fun _ ->
           assert_equal [ "a"; "a"; "a" ] (replicate ("a", 3)) );
         ( "sqrList" >:: fun _ ->
           assert_equal [ 1; 4; 9; 16 ] (sqrList [ 1; 2; 3; 4 ]) );
         ( "palindrom" >:: fun _ ->
           assert_equal true (palindrome [ 1; 2; 3; 2; 1 ]);
           assert_equal true (palindrome []) );
         ("listLength" >:: fun _ -> assert_equal 3 (listLength [ 1; 2; 3 ]));
       ]

let () = run_test_tt_main tests
