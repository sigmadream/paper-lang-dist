:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, Codes),
    (   Codes == end_of_file
    ->  true
    ;   parse_first_two(Codes, M, N),
        Total is M + N - 2,
        K is M - 1,
        comb(Total, K, Ans),
        write(Ans), nl
    ).

parse_first_two(Codes, M, N) :-
    skip_ws(Codes, C1),
    parse_number(C1, M, Rest),
    skip_ws(Rest, C2),
    parse_number(C2, N, _).

skip_ws([C|Cs], Rest) :-
    ( C =:= 32 ; C =:= 9 ; C =:= 10 ; C =:= 13 ),
    !,
    skip_ws(Cs, Rest).
skip_ws(Cs, Cs).

parse_number(Codes, Num, Rest) :-
    parse_digits(Codes, Digits, Rest),
    number_codes(Num, Digits).

parse_digits([C|Cs], [C|Ds], Rest) :-
    C >= 48,
    C =< 57,
    !,
    parse_digits(Cs, Ds, Rest).
parse_digits(Rest, [], Rest).

comb(N, K, R) :-
    NK is N - K,
    (   K =< NK
    ->  K0 = K
    ;   K0 = NK
    ),
    comb_iter(N, K0, 1, 1, R).

comb_iter(N, K, I, Acc, R) :-
    (   I > K
    ->  R = Acc
    ;   Acc1 is Acc * (N - K + I) // I,
        I1 is I + 1,
        comb_iter(N, K, I1, Acc1, R)
    ).