main :-
    read_line_to_string(current_input, S0),
    (   S0 == end_of_file
    ->  true
    ;   strip_cr(S0, S),
        string_codes(S, Codes),
        reverse(Codes, Reversed),
        (   Codes = Reversed
        ->  writeln(1)
        ;   writeln(0)
        )
    ).

strip_cr(S0, S) :-
    string_codes(S0, Codes0),
    (   append(Codes, [13], Codes0)
    ->  string_codes(S, Codes)
    ;   S = S0
    ).