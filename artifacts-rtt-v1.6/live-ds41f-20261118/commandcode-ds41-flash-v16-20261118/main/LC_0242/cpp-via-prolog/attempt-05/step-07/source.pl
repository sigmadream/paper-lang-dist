:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, S0),
    read_line_to_string(user_input, T0),
    strip_cr(S0, S),
    strip_cr(T0, T),
    string_codes(S, SC),
    string_codes(T, TC),
    msort(SC, SS),
    msort(TC, TT),
    ( SS == TT -> R = 1 ; R = 0 ),
    format('~w~n', [R]).

strip_cr(S0, S) :-
    string_codes(S0, Cs0),
    remove_cr(Cs0, Cs),
    string_codes(S, Cs).

remove_cr([], []).
remove_cr([13|T], R) :-
    !,
    remove_cr(T, R).
remove_cr([H|T], [H|R]) :-
    remove_cr(T, R).