let () =
  let n = Scanf.scanf " %d" (fun x -> x) in
  let dp = Array.make (n + 1) 0 in
  for i = 1 to n do
    dp.(i) <- dp.(i lsr 1) + (i land 1)
  done;
  for i = 0 to n do
    if i > 0 then print_char ' ';
    print_int dp.(i)
  done;
  print_newline ()
