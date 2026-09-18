gcd(A, B, GCD) :-
    A mod B =:= 0,
    GCD = B.
gcd(A, B, GCD) :-
    A mod B \= 0,
    C is A mod B,
    gcd(B, C, GCD).

lcm(A, B, LCM) :-
    GCD is gcd(A, B),
    LCM is (A * B) div GCD.

main :-
    read_line_to_string(_, Input),
    split_string(Input, " ", "", Parts),
    maplist(string_to_integer, Parts, [A, B]),
    gcd(A, B, GCD),
    lcm(A, B, LCM),
    write(GCD), nl,
    write(LCM), nl.