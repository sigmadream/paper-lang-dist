main :-
    read_all_codes(Codes),
    numbers(Codes, Nums),
    Nums = [A, B | _],
    gcd(A, B, G),
    L is (A // G) * B,
    format("~w~n~w~n", [G, L]).

read_all_codes(Codes) :-
    get_code(C),
    read_all_codes_(C, [], Rev),
    reverse(Rev, Codes).

read_all_codes_(-1, Acc, Acc).
read_all_codes_(C, Acc, Codes) :-
    C =\= -1,
    get_code(C1),
    read_all_codes_(C1, [C | Acc], Codes).

numbers([], []).
numbers([C | Cs], Nums) :-
    C >= 48,
    C =< 57,
    !,
    take_digits([C | Cs], Value, Rest),
    Nums = [Value | RestNums],
    numbers(Rest, RestNums).
numbers([_ | Cs], Nums) :-
    numbers(Cs, Nums).

take_digits(Cs, Value, Rest) :-
    take_digits_(Cs, 0, Value, Rest).

take_digits_([C | Cs], Acc, Value, Rest) :-
    C >= 48,
    C =< 57,
    !,
    Acc1 is Acc * 10 + (C - 48),
    take_digits_(Cs, Acc1, Value, Rest).
take_digits_(Rest, Acc, Acc, Rest).

gcd(A, 0, A) :- !.
gcd(A, B, G) :-
    B > 0,
    R is A mod B,
    gcd(B, R, G).