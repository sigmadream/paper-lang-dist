main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Parts),
    Parts = [AStr, BStr | _],
    number_string(A, AStr),
    number_string(B, BStr),
    gcd_euclid(A, B, G),
    L is (A // G) * B,
    format("~d~n~d~n", [G, L]).

gcd_euclid(A, 0, A) :- !.
gcd_euclid(A, B, G) :-
    R is A mod B,
    gcd_euclid(B, R, G).