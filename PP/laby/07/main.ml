module StackMachine = struct
  type stack = float list

  exception Division_by_zero
  exception Insufficient_number_of_arguments

  type instruction =
    | Rst
    | LoadF of float
    | LoadI of int
    | Cpy
    | Add
    | Sub
    | Mul
    | Div

  type t = { mutable stack : stack }

  let init () = { stack = [] }

  let result m =
    match m.stack with
    | [] -> raise Insufficient_number_of_arguments
    | x :: _ -> x

  let execute m l =
    let rec executeRest machine instructionList =
      match instructionList with
      | [] -> ()
      | Rst :: t ->
          machine.stack <- [];
          executeRest machine t
      | LoadF f :: t ->
          machine.stack <- f :: machine.stack;
          executeRest machine t
      | LoadI i :: t ->
          machine.stack <- float_of_int i :: machine.stack;
          executeRest machine t
      | Cpy :: t -> (
          match machine.stack with
          | [] -> raise Insufficient_number_of_arguments
          | x :: _ ->
              machine.stack <- x :: machine.stack;
              executeRest machine t)
      | Add :: t -> (
          match machine.stack with
          | [] | [ _ ] -> raise Insufficient_number_of_arguments
          | x :: y :: s ->
              machine.stack <- (x +. y) :: s;
              executeRest machine t)
      | Sub :: t -> (
          match machine.stack with
          | [] | [ _ ] -> raise Insufficient_number_of_arguments
          | x :: y :: s ->
              machine.stack <- (x -. y) :: s;
              executeRest machine t)
      | Mul :: t -> (
          match machine.stack with
          | [] | [ _ ] -> raise Insufficient_number_of_arguments
          | x :: y :: s ->
              machine.stack <- (x *. y) :: s;
              executeRest machine t)
      | Div :: t -> (
          match machine.stack with
          | [] | [ _ ] -> raise Insufficient_number_of_arguments
          | x :: y :: s ->
              if y = 0. then raise Division_by_zero
              else machine.stack <- (x /. y) :: s;
              executeRest machine t)
    in
    executeRest m l
end

module type COPROCESSOR = sig
  type t

  exception Division_by_zero
  exception Insufficient_number_of_arguments

  type instruction =
    | Rst
    | LoadF of float
    | LoadI of int
    | Cpy
    | Add
    | Sub
    | Mul
    | Div

  val init : unit -> t
  val execute : t -> instruction list -> unit
  val result : t -> float
end

module Coprocessor : COPROCESSOR = StackMachine
