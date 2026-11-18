:- module(main, []).
:- use_module(library(dcg/basics)).

main :-
    current_input(In),
    read_line_to_codes(In, S),
    read_line_to_codes(In, T),
    ( S \== end_of_file, T \== end_of_file ->
        msort(S, SS),
        msort(T, TS),
        ( SS == TS -> R = 1 ; R = 0 ),
        format("~d~n", [R])
    ; true ).