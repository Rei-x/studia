open OUnit2
open Laby03.Main

let rec list_to_string = function
  | [] -> ""
  | e :: l -> string_of_int e ^ " " ^ list_to_string l

let tests =
  "laby 03 tests"
  >::: [
         ( "multipleee" >:: fun _ ->
           let multiply_by_two x = x * 2 in

           assert_equal [ 16; 8; 4; 2 ]
             ((multiply_by_two >> 3) 2)
             ~printer:list_to_string;
           assert_equal []
             (((fun x -> x + 2) >> -1) 100)
             ~printer:list_to_string;
           assert_equal []
             (((fun x -> x + 2) >> -1) 100)
             ~printer:list_to_string;
           assert_equal [] (((fun x -> x + 2) >> 0) 2) ~printer:list_to_string
         );
       ]

let () = run_test_tt_main tests
