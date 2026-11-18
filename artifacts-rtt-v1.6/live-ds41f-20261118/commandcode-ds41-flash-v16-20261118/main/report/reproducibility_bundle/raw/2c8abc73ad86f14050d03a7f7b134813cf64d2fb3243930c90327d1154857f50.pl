main :-
    read_line_to_string(user_input, S0),
    (   S0 == end_of_file
    ->  true
    ;   normalize_space(string(S), S0),
        (   S == ""
        ->  true
        ;   (   palindrome(S)
            ->  writeln(1)
            ;   writeln(0)
            )
        )
    ).

palindrome(S) :-
    string_codes(S, C),
    reverse(C, C).