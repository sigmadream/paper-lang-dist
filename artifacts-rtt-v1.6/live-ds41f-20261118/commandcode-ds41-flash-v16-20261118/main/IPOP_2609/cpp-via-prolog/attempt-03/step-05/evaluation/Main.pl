main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Parts),
    Parts = [AStr, BStr],
    number_string(A, AStr),
    number_string(B, BStr),
    gcd_euclid(A, B, G),
    L is (A // G) * B,
    format("~w~n~w~n", [G, L]).

gcd_euclid(X, 0, X) :-
    X > 0.
gcd_euclid(X, Y, G) :-
    Y > 0,
    R is X mod Y,
    gcd_euclid(Y, R, G).