:- module(main, [main/0]).

main :-
    read_line_to_string(user_input, S),
    ( S == end_of_file -> true
    ; reverse(S, R),
      ( S == R -> format("1~n") ; format("0~n") )
    ).