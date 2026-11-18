:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, TLine),
    ( TLine == end_of_file ->
        true
    ; number_codes(T, TLine),
      process(T)
    ).

process(0) :- !.
process(N) :-
    read_line_to_codes(user_input, Line),
    ( Line == end_of_file ->
        true
    ; check(Line, 0, Valid),
        ( Valid == true -> write('YES'), nl ; write('NO'), nl ),
        N1 is N - 1,
        process(N1)
    ).

check([], Bal, Valid) :-
    ( Bal == 0 -> Valid = true ; Valid = false ).
check([C|Cs], Bal, Valid) :-
    ( C == 40 -> Bal1 is Bal + 1
    ; Bal1 is Bal - 1
    ),
    ( Bal1 < 0 -> Valid = false
    ; check(Cs, Bal1, Valid)
    ).