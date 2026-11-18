main :-
    read_string(user_input, "\n", " \t", _, Line),
    split_string(Line, " \t\r\n", " \t\r\n", [P1, P2 | _]),
    number_string(A, P1),
    number_string(B, P2),
    my_gcd(A, B, G),
    L is (A // G) * B,
    format("~w~n~w~n", [G, L]).

my_gcd(A, 0, A) :-
    A > 0.
my_gcd(A, B, G) :-
    B > 0,
    C is A mod B,
    my_gcd(B, C, G).