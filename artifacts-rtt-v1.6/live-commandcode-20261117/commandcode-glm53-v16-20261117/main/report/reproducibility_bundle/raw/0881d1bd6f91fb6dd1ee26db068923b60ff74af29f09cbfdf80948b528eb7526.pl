:- use_module(library(readutil)).

fact(0, 1) :- !.
fact(N, F) :- N1 is N - 1, fact(N1, F1), F is N * F1.

comb(K, R, C) :-
    R1 is K - R,
    (   R1 < R
    ->  comb(K, R1, C)
    ;   fact(K, FK),
        fact(R, FR),
        fact(R1, FR1),
        C is FK // (FR * FR1)
    ).

parse_ints([], [], []) :- !.
parse_ints([32|T], Ns, Rest) :- !, parse_ints(T, Ns, Rest).
parse_ints(Codes, [N|Ns], Rest) :-
    (   number_codes(N, Digs),
        append(Digs, Rest0, Codes)
    ->  parse_ints(Rest0, Ns, Rest)
    ;   Ns = [], Rest = Codes
    ).

main :-
    read_line_to_codes(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   parse_ints(Line, [M, N], _),
        K is M + N - 2,
        R1 is M - 1,
        R2 is N - 1,
        (   R2 < R1
        ->  R = R2
        ;   R = R1
        ),
        comb(K, R, C),
        number_codes(C, Out),
        format("~s~n", [Out])
    ).