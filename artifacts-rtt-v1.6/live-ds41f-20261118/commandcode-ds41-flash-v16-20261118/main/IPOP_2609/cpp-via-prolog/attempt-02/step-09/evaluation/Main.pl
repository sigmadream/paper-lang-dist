main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   split_string(Line, " \t\r\n", " \t\r\n", [SA, SB | _]),
        number_string(A, SA),
        number_string(B, SB),
        my_gcd(A, B, G),
        L is (A // G) * B,
        format("~w~n~w~n", [G, L])
    ).

my_gcd(X, 0, X) :-
    X > 0,
    !.
my_gcd(X, Y, G) :-
    Y > 0,
    R is X mod Y,
    my_gcd(Y, R, G).