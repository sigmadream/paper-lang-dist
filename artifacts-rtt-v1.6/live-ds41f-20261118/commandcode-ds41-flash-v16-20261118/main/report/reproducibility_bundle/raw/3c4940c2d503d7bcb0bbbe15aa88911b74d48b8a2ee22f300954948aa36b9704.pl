:- use_module(library(readutil)).

is_ws(0' ).
is_ws(0'\t).
is_ws(0'\n).
is_ws(0'\r).

main :-
    read_line_to_string(user_input, S0),
    read_line_to_string(user_input, T0),
    ( S0 == end_of_file -> S = "" ; S = S0 ),
    ( T0 == end_of_file -> T = "" ; T = T0 ),
    string_codes(S, SC0),
    string_codes(T, TC0),
    exclude(is_ws, SC0, SC),
    exclude(is_ws, TC0, TC),
    msort(SC, S1),
    msort(TC, T1),
    ( S1 == T1 -> R = 1 ; R = 0 ),
    writeln(R).