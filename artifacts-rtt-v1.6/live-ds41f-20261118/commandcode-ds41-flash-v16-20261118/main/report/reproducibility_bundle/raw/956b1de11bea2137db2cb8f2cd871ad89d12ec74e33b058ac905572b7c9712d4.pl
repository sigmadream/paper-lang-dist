:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, Codes),
    parse_two(Codes, A, B),
    gcd(A, B, G),
    L is (A // G) * B,
    write(G), nl,
    write(L), nl.

parse_two(Codes, A, B) :-
    skip_ws(Codes, Rest),
    parse_num(Rest, A, Rest1),
    skip_ws(Rest1, Rest2),
    parse_num(Rest2, B, _).

skip_ws([C|Cs], Rest) :-
    code_type(C, space),
    !,
    skip_ws(Cs, Rest).
skip_ws(Cs, Cs).

parse_num(Codes, N, Rest) :-
    parse_digits(Codes, Digits, Rest),
    Digits \= [],
    number_codes(N, Digits).

parse_digits([C|Cs], [C|Ds], Rest) :-
    code_type(C, digit),
    !,
    parse_digits(Cs, Ds, Rest).
parse_digits(Rest, [], Rest).

gcd(A, 0, A) :-
    A > 0.
gcd(A, B, G) :-
    B > 0,
    R is A mod B,
    gcd(B, R, G).