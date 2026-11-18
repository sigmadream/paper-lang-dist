main :-
    read_line_to_string(user_input, S),
    string_codes(S, Cs),
    reverse(Cs, Rs),
    (   Cs == Rs
    ->  writeln(1)
    ;   writeln(0)
    ).