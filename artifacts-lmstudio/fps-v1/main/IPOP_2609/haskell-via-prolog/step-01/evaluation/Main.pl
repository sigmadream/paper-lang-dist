gcd(A, 0, A).
gcd(A, B, GCD) :-
    R is A mod B,
    gcd(B, R, GCD).

lcm(A, B, LCM) :-
    GCD is gcd(A, B),
    LCM is (A * B) div GCD.

main :-
    read_line(Input),
    split_string(Input, ' ', _, [A, B]),
    number_string(A1, A),
    number_string(B1, B),
    atom_number(A2, A1),
    atom_number(B2, B1),
    gcd(A2, B2, GCD),
    format('~d\n', [GCD]),
    lcm(A2, B2, LCM),
    format('~d\n', [LCM]).