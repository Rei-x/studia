let ( >> ) f n x =
  if n <= 0 then []
  else
    let rec compose_n_times innerN innerX acc =
      let result = f innerX in
      if innerN < 0 then []
      else if innerN = 0 then acc
      else compose_n_times (innerN - 1) result (result :: acc)
    in
    compose_n_times n x [ x ]
