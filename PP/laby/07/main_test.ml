open OUnit2
open Laby07.Main

let tests =
  "laby 07 tests"
  >::: [
         ( "stack" >:: fun _ ->
           let stack = Coprocessor.init () in
           Coprocessor.execute stack
             [
               Coprocessor.LoadI 2;
               Coprocessor.LoadF 4.;
               Coprocessor.LoadF 8.;
               Coprocessor.Add;
             ];
           assert_equal 12. (Coprocessor.result stack);
           Coprocessor.execute stack [ Coprocessor.Add ];
           assert_equal 14. (Coprocessor.result stack);
           Coprocessor.execute stack [ Coprocessor.Cpy; Coprocessor.Mul ];
           assert_equal 196. (Coprocessor.result stack);
           Coprocessor.execute stack [ Coprocessor.LoadI 200; Coprocessor.Sub ];
           assert_equal 4. (Coprocessor.result stack);
           Coprocessor.execute stack [ Coprocessor.LoadI 20; Coprocessor.Div ];
           assert_equal 5. (Coprocessor.result stack);
           assert_raises Coprocessor.Insufficient_number_of_arguments (fun () ->
               Coprocessor.execute stack [ Coprocessor.Rst; Coprocessor.Add ]);
           assert_raises Coprocessor.Division_by_zero (fun () ->
               Coprocessor.execute stack
                 [
                   Coprocessor.Rst;
                   Coprocessor.LoadI 0;
                   Coprocessor.LoadI 2;
                   Coprocessor.Div;
                 ]);
           assert_equal 2. (Coprocessor.result stack);
           assert_raises Coprocessor.Insufficient_number_of_arguments (fun () ->
               Coprocessor.execute stack [ Coprocessor.Rst ];
               Coprocessor.result stack) );
       ]

let () = run_test_tt_main tests
