:- module(main, [main/0]).
:- set_current_prolog_flag(argv, main).

read_line(Line) :-
    read_line_to_codes(current_input, Cs),
    ( Cs == end_of_file -> Line = []
    ; Cs == [] -> Line = []
    ; append(Cs, [0'\n], Cs2), read_line_to_codes(current_input, Rest),
      append(Cs2, Rest, Line)
    ).

trim_trailing(Line, Str) :-
    append(Str, Tail, Line),
    ( Tail == [] ; Tail == [0'\n] ; Tail == [0'\r,0'\n] ; Tail == [0'\r] ),
    !.

main :-
    read_line_to_codes(current_input, S0),
    read_line_to_codes(current_input, T0),
    ( S0 == end_of_file -> S = [] ; S = S0 ),
    ( T0 == end_of_file -> T = [] ; T = T0 ),
    ( append(S, [0'\r], S1) -> true ; S1 = S ),
    ( append(T, [0'\r], T1) -> true ; T1 = T ),
    ( msort(S1, SS), msort(T1, TT), SS == TT -> R = 1 ; R = 0 ),
    format("~d~n", [R]).