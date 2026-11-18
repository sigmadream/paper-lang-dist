:- use_module(library(readutil)).

main :-
    read_line_codes(S0),
    read_line_codes(T0),
    msort(S0, S),
    msort(T0, T),
    ( S == T -> R = 1 ; R = 0 ),
    format("~w~n", [R]).

read_line_codes(Codes) :-
    read_line_to_codes(user_input, Line),
    ( Line == end_of_file ->
        Codes = []
    ; strip_cr(Line, Codes)
    ).

strip_cr(Codes0, Codes) :-
    reverse(Codes0, Rev),
    ( Rev = [13|Rest] ->
        reverse(Rest, Codes)
    ; Codes = Codes0
    ).