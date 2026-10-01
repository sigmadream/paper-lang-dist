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
  | _n_str :: num_strs ->
      let non_zeros = List.filter (fun s -> s <> "0") num_strs in
      let zeros = List.filter (fun s -> s = "0") num_strs in
      let result = non_zeros @ zeros in
      print_endline (String.concat " " result)
