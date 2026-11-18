main :-
    read_all_codes(Codes),
    parse_numbers(Codes, Nums),
    Nums = [A, B | _],
    my_gcd(A, B, G),
    L is (A // G) * B,
    write(G), nl,
    write(L), nl.

read_all_codes(Codes) :-
    get_code(C),
    read_all_codes_1(C, Codes).

read_all_codes_1(-1, []) :- !.
read_all_codes_1(C, [C | Rest]) :-
    read_all_codes(Rest).

parse_numbers(Codes, Nums) :-
    parse_numbers_1(Codes, [], RevNums),
    reverse(RevNums, Nums).

parse_numbers_1([], Acc, Acc).
parse_numbers_1([C | Cs], Acc, Nums) :-
    space_code(C), !,
    parse_numbers_1(Cs, Acc, Nums).
parse_numbers_1(Codes, Acc, Nums) :-
    take_digits(Codes, Digits, Rest),
    Digits = [_ | _],
    number_codes(N, Digits),
    parse_numbers_1(Rest, [N | Acc], Nums).

take_digits([C | Cs], [C | Ds], Rest) :-
    digit_code(C), !,
    take_digits(Cs, Ds, Rest).
take_digits(Cs, [], Cs).

space_code(32).
space_code(9).
space_code(10).
space_code(13).

digit_code(C) :-
    C >= 48,
    C =< 57.

my_gcd(A, 0, A) :- !.
my_gcd(A, B, G) :-
    R is A mod B,
    my_gcd(B, R, G).