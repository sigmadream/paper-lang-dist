gcd(0, A, A).
gcd(A, 0, A).
gcd(A, B, GCD) :-
    A > B,
    R is A mod B,
    gcd(B, R, GCD).
gcd(A, B, GCD) :-
    A < B,
    R is B mod A,
    gcd(A, R, GCD).

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
    lcm(A2, B2, LCM),
    write(GCD), nl,
    write(LCM), nl.

read_line(Input) :-
    read_string(user_input, "\n", Input).

split_string(String, Delimiter, _, [Head|Tail]) :-
    string_concat(Head, Delimiter, Concatenated),
    string_concat(Concatenated, Tail, String).