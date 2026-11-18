:- module(main, [main/0]).
:- use_module(library(dcgs)).

reverse_s([], []).
reverse_s([H|T], R) :- reverse_s(T, RT), append(RT, [H], R).

main :-
    read_line_to_string(user_input, S),
    ( string_length(S, L), L > 0,
      sub_string(S, L-1, 1, _, "\r") ->
        SL is L - 1, sub_string(S, 0, SL, _, S2)
    ; S2 = S
    ),
    string_codes(S2, Cs),
    reverse_s(Cs, R),
    ( Cs == R -> Rslt = 1 ; Rslt = 0 ),
    format("~d~n", [Rslt]).