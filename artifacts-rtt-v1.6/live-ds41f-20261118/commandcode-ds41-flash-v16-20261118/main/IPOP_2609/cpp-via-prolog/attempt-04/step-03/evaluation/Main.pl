is_ws(' ').
is_ws('\t').
is_ws('\n').
is_ws('\r').
is_ws('\f').

read_nat(N) :-
    get_char(C),
    (   C == end_of_file
    ->  N = none
    ;   is_ws(C)
    ->  read_nat(N)
    ;   char_type(C, digit)
    ->  read_digits([C], N)
    ;   read_nat(N)
    ).

read_digits(Rev, N) :-
    get_char(C),
    (   C == end_of_file
    ->  reverse(Rev, Chars),
        number_chars(N, Chars)
    ;   char_type(C, digit)
    ->  read_digits([C|Rev], N)
    ;   reverse(Rev, Chars),
        number_chars(N, Chars)
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