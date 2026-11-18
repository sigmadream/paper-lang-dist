main :-
    (   read_line_to_string(user_input, S),
        S \== end_of_file
    ->  string_codes(S, Cs),
        reverse(Cs, Rs),
        (   Cs == Rs
        ->  R = 1
        ;   R = 0
        ),
        format("~w~n", [R])
    ;   true
    ).