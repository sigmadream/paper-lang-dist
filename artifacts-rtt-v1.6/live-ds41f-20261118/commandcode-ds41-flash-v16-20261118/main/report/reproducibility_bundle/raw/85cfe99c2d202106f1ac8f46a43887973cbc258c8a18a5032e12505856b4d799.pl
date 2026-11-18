:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, S),
    read_line_to_string(user_input, T),
    string_codes(S, Cs0),
    string_codes(T, Ts0),
    exclude(is_line_break, Cs0, Cs),
    exclude(is_line_break, Ts0, Ts),
    msort(Cs, SortedS),
    msort(Ts, SortedT),
    ( SortedS == SortedT -> writeln(1) ; writeln(0) ).

is_line_break(10).
is_line_break(13).