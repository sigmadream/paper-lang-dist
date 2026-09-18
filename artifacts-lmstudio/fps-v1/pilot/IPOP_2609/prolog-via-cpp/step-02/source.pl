gcd(X, Y, GCD) :-
    X mod Y =:= 0,
    GCD = Y.
gcd(X, Y, GCD) :-
    X mod Y \= 0,
    Z is X mod Y,
    gcd(Y, Z, GCD).

lcm(X, Y, LCM) :-
    GCD is gcd(X, Y),
    LCM is (X / GCD) * Y.

main :-
    read_line_to_string(_, Input),
    split_string(Input, " ", "", Parts),
    maplist(string_to_integer, Parts, [A, B]),
    gcd(A, B, GCD),
    lcm(A, B, LCM),
    write(GCD), nl,
    write(LCM), nl.