main :-
    read_line_to_string(user_input, S),
    read_line_to_string(user_input, T),
    string_codes(S, SC),
    string_codes(T, TC),
    msort(SC, SS),
    msort(TC, TT),
    (   SS == TT
    ->  R = 1
    ;   R = 0
    ),
    format("~w~n", [R]).