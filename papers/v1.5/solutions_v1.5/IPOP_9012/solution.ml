let is_valid s =
  let len = String.length s in
  let rec check idx bal =
    if bal < 0 then false
    else if idx = len then bal = 0
    else
      match s.[idx] with
      | '(' -> check (idx + 1) (bal + 1)
      | ')' -> check (idx + 1) (bal - 1)
      | _ -> check (idx + 1) bal
  in
  check 0 0

let () =
  try
    let t_line = input_line stdin in
    let t = int_of_string (String.trim t_line) in
    for _ = 1 to t do
      let line = String.trim (input_line stdin) in
      print_endline (if is_valid line then "YES" else "NO")
    done
  with End_of_file -> ()
