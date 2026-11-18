main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   split_string(Line, " \t\r\n", " \t\r\n", [S|_]),
        string_chars(S, Chars),
        reverse(Chars, Chars),
        writeln(1)
    ;   writeln(0)
    ).