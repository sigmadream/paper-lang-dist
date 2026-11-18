my_gcd(A, 0, A) :-
    A > 0.
my_gcd(A, B, G) :-
    B > 0,
    R is A mod B,
    my_gcd(B, R, G).

main :-
    read(A),
    read(B),
    my_gcd(A, B, G),
    L is (A // G) * B,
    format('~w~n~w~n', [G, L]).