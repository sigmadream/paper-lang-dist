gcd(A, B, G) :-
    (   B =:= 0
    ->  G = A
    ;   R is A mod B,
        gcd(B, R, G)
    ).

main :-
    read_line_to_codes(user_input, Codes),
    split_string(Codes, " \t\r\n", " \t\r\n", [AStr, BStr]),
    number_string(A, AStr),
    number_string(B, BStr),
    gcd(A, B, G),
    L is (A // G) * B,
    format("~w~n~w~n", [G, L]).