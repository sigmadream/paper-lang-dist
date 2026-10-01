let split_whitespace s =
  let len = String.length s in
  let rec aux i acc =
    if i >= len then List.rev acc
    else if s.[i] = ' ' || s.[i] = '\t' || s.[i] = '\r' || s.[i] = '\n' then
      aux (i + 1) acc
    else
      let j = ref i in
      while !j < len && s.[!j] <> ' ' && s.[!j] <> '\t' && s.[!j] <> '\r' && s.[!j] <> '\n' do
        incr j
      done;
      aux !j (String.sub s i (!j - i) :: acc)
  in
  aux 0 []

let () =
  let tokens =
    let rec read_tokens acc =
      try
        let line = input_line stdin in
        let parts = split_whitespace line in
        read_tokens (List.rev_append parts acc)
      with End_of_file -> List.rev acc
    in
    read_tokens []
  in
  match tokens with
  | [] -> ()
  | n_str :: matrix_strs ->
      let n = int_of_string n_str in
      let g = Array.make_matrix n n 0 in
      let arr = Array.of_list (List.map int_of_string matrix_strs) in
      for i = 0 to n - 1 do
        for j = 0 to n - 1 do
          g.(i).(j) <- arr.(i * n + j)
        done
      done;
      let seen = Array.make n false in
      let components = ref 0 in
      for i = 0 to n - 1 do
        if not seen.(i) then begin
          incr components;
          let stack = ref [i] in
          seen.(i) <- true;
          while !stack <> [] do
            match !stack with
            | [] -> ()
            | u :: rest ->
                stack := rest;
                for v = 0 to n - 1 do
                  if g.(u).(v) = 1 && not seen.(v) then begin
                    seen.(v) <- true;
                    stack := v :: !stack
                  end
                done
          done
        end
      done;
      print_int !components;
      print_newline ()
