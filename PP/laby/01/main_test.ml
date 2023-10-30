open OUnit2
open Laby01.Main

let tests =
  "laby 01 tests"
  >::: [
         ( "reverse4" >:: fun _ ->
           assert_equal (reverse4 (1, "mario", 1, [ 1 ])) ([ 1 ], 1, "mario", 1)
         );
         ( "isPerfect" >:: fun _ ->
           assert_bool "6 should be perfect" (isPerfect 6);
           assert_bool "5 should not be perfect" (not (isPerfect 5)) );
         ( "sumProd" >:: fun _ ->
           assert_equal (sumProd (2, 6)) (14, 120);
           assert_equal (sumProd (-6, 4)) (-15, 0) );
         ( "insert" >:: fun _ ->
           assert_equal (insert ([ 1; 3; 4; 5 ], 2, 1)) [ 1; 2; 3; 4; 5 ];
           assert_equal (insert ([ 1; 2; 3; 4 ], 5, 999)) [ 1; 2; 3; 4; 5 ] );
         ("argMax" >:: fun _ -> assert_equal (argMax [ 1; 2; 3; 4 ]) [ 3 ]);
       ]

let () = run_test_tt_main tests
