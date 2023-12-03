open OUnit2
open Laby04.Main

let tests =
  "laby 04 tests"
  >::: [
         ( "multipleee" >:: fun _ ->
           let tree4 = Node (4, Node (2, None, None, None), None, None) in
           assert_equal
             (mapTree3 tree4 (fun x -> x * 2))
             (Node (8, Node (4, None, None, None), None, None)) );
       ]

let () = run_test_tt_main tests
