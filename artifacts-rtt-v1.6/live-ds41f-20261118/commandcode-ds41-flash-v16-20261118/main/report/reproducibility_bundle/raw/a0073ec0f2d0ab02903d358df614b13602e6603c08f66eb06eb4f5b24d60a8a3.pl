main :-
    (   read_line_to_string(user_input, Line)
    ->  split_string(Line, "", " \t\r\n", Parts),
        (   Parts = [Token|_]
        ->  string_chars(Token, Chars),
            (   reverse(Chars, Chars)
            ->  writeln(1)
            ;   writeln(0)
            )
        ;   writeln(0)
        )
    ;   writeln(0)
    ).