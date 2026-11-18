main :-
    (   read_line_to_string(user_input, S0) ->
        (   S0 == end_of_file ->
            true
        ;   trim_string(S0, S),
            (   S == "" ->
                true
            ;   string_codes(S, Codes),
                reverse(Codes, Codes),
                format("1~n", [])
            ;   format("0~n", [])
            )
        )
    ;   true
    ).

trim_string(S, T) :-
    string_codes(S, Cs),
    trim_left(Cs, L),
    reverse(L, Rev),
    trim_left(Rev, Rev2),
    reverse(Rev2, R),
    string_codes(T, R).

trim_left([C|Cs], R) :-
    is_whitespace(C), !,
    trim_left(Cs, R).
trim_left(Cs, Cs).

is_whitespace(32).
is_whitespace(9).
is_whitespace(10).
is_whitespace(11).
is_whitespace(12).
is_whitespace(13).