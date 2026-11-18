:- module(main, [main/0]).
:- use_module(library(lists)).

main :-
    read_line_to_string(user_input, S),
    ( S == end_of_file -> true
    ; reverse_string(S, R),
      ( S == R -> writeln(1) ; writeln(0))
    ).

reverse_string(S, R) :-
    atom_codes(S, L),
    reverse(L, RL),
    atom_codes(R, RL).