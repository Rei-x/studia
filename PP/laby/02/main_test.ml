open OUnit2
open Laby02.Main

let tests =
  "laby 02 tests"
  >::: [
         ( "cutAndMend" >:: fun _ ->
           let cutAndMend15 = cutAndMend (1, 5) in
           assert_equal [ 1; 7; 8 ] (cutAndMend15 [ 1; 2; 3; 4; 5; 6; 7; 8 ]);
           let cutAndMendLol = cutAndMend (-100, 0) in
           assert_equal [ 2 ] (cutAndMendLol [ 1; 2 ]);
           assert_equal [] (cutAndMendLol []) );
         ( "split2Rec" >:: fun _ ->
           assert_equal ([], []) (split2Rec []);
           assert_equal ([ 1 ], [ 2 ]) (split2Rec [ 1; 2 ]);
           assert_equal ([], []) (split2Rec [ 1 ]);
           assert_equal ([ 1; 3 ], [ 2; 4 ]) (split2Rec [ 1; 2; 3; 4; 5 ]) );
         ( "split2Tail" >:: fun _ ->
           assert_equal ([], []) (split2Tail []);
           assert_equal ([ 1 ], [ 2 ]) (split2Tail [ 1; 2 ]);
           assert_equal ([], []) (split2Tail [ 1 ]);
           assert_equal ([ 3; 1 ], [ 4; 2 ]) (split2Tail [ 1; 2; 3; 4; 5 ]) );
       ]

let () = run_test_tt_main tests
