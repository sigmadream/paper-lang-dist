main :-
    read_line_to_string(user_input, S),
    (   S == end_of_file
    ->  true
    ;   string_chars(S, Chars),
        reverse(Chars, Reversed),
        (   Chars == Reversed
        ->  writeln(1)
        ;   writeln(0)
        )
    ).