main :-
    current_input(Stream),
    read_string(Stream, end_of_file, Input),
    string_codes(Input, Codes),
    parse_n(Codes, N),
    ( N < 0 ->
        nl
    ;
        output_range(0, N)
    ).

parse_n(Codes, N) :-
    skip_ws(Codes, Rest),
    parse_digits(Rest, 0, N).

skip_ws([C|T], R) :-
    ws(C),
    skip_ws(T, R).
skip_ws(L, L).

ws(32).
ws(9).
ws(10).
ws(13).

parse_digits([C|T], Acc, N) :-
    C >= 48,
    C =< 57,
    !,
    Acc1 is Acc * 10 + (C - 48),
    parse_digits(T, Acc1, N).
parse_digits(_, Acc, Acc).

output_range(I, N) :-
    I > N,
    !,
    nl.
output_range(I, N) :-
    ( I > 0 ->
        write(' ')
    ;
        true
    ),
    popcount(I, P),
    write(P),
    I1 is I + 1,
    output_range(I1, N).

popcount(X, C) :-
    X =:= 0,
    !,
    C = 0.
popcount(X, C) :-
    X > 0,
    X1 is X >> 1,
    popcount(X1, C1),
    C is (X mod 2) + C1.