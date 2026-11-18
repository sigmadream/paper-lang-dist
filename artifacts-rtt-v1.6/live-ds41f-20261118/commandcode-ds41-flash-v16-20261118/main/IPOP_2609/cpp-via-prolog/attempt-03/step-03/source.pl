main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Parts),
    maplist(number_string, [A, B], Parts),
    gcd(A, B, G),
    L is (A // G) * B,
    format("~w~n~w~n", [G, L]).

gcd(A, 0, A) :-
    A > 0.
gcd(A, B, G) :-
    B > 0,
    R is A mod B,
    gcd(B, R, G).