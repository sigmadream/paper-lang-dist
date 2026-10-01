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
  | _n_str :: first_str :: rest_strs ->
      let first = int_of_string first_str in
      let rec kadane cur best = function
        | [] -> best
        | s :: tl ->
            let x = int_of_string s in
            let new_cur = max x (cur + x) in
            let new_best = max best new_cur in
            kadane new_cur new_best tl
      in
      let ans = kadane first first rest_strs in
      print_int ans;
      print_newline ()
  | _ -> ()
