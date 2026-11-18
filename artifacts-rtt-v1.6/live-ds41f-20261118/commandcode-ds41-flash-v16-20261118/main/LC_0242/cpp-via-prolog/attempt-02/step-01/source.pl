main :-
    read_line_to_string(user_input, S0),
    read_line_to_string(user_input, T0),
    strip(S0, S),
    strip(T0, T),
    ( anagram(S, T) -> writeln(1) ; writeln(0) ).

strip(S0, S) :-
    string_codes(S0, Cs),
    exclude(is_space, Cs, Cs1),
    string_codes(S, Cs1).

is_space(C) :-
    code_type(C, space).

anagram(S, T) :-
    string_codes(S, Cs),
    string_codes(T, Ct),
    msort(Cs, Ss),
    msort(Ct, St),
    Ss == St.