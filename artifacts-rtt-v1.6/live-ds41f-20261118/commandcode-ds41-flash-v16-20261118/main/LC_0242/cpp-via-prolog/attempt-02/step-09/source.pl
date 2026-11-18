main :-
    get_line(S),
    get_line(T),
    filter_ws(S, A),
    filter_ws(T, B),
    msort(A, SA),
    msort(B, SB),
    ( SA == SB -> R = 1 ; R = 0 ),
    writeln(R).

get_line(S) :-
    read_line_to_string(user_input, X),
    ( X == end_of_file -> S = ""
    ; S = X
    ).

filter_ws(S, Codes) :-
    string_codes(S, All),
    exclude(is_ws, All, Codes).

is_ws(32).
is_ws(9).
is_ws(10).
is_ws(13).