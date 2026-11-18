main :-
    read_line_to_string(user_input, S),
    (   palindrome(S)
    ->  writeln(1)
    ;   writeln(0)
    ).

palindrome(S) :-
    string_chars(S, Cs),
    reverse(Cs, Rs),
    Cs == Rs.