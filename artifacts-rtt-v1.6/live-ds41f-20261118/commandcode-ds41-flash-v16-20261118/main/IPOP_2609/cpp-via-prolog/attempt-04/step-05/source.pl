read_nat(N) :-
    get_char(C),
    (   C == end_of_file
    ->  N = none
    ;   char_type(C, digit)
    ->  char_code(C, Code),
        D is Code - 48,
        read_digits(D, N)
    ;   read_nat(N)
    ).

read_digits(Acc, N) :-
    peek_char(P),
    (   P == end_of_file
    ->  N = Acc
    ;   char_type(P, digit)
    ->  get_char(C),
        char_code(C, Code),
        D is Code - 48,
        Acc1 is Acc * 10 + D,
        read_digits(Acc1, N)
    ;   N = Acc
    ).

gcd(A, 0, A) :- !.
gcd(A, B, G) :-
    B > 0,
    R is A mod B,
    gcd(B, R, G).

main :-
    read_nat(A),
    (   A == none
    ->  true
    ;   read_nat(B),
        (   B == none
        ->  true
        ;   gcd(A, B, G),
            L is (A // G) * B,
            format("~w~n~w~n", [G, L])
        )
    ).