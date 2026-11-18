main :-
    read_int(N),
    ( N >= 0 ->
        print_counts(0, N)
    ;   nl
    ).

read_int(N) :-
    get_code(C),
    skip_ws(C, C1),
    ( C1 = -1 ->
        N = 0
    ;   read_digits(C1, 0, N)
    ).

skip_ws(-1, -1) :- !.
skip_ws(C, C1) :-
    ( C = 32 ; C = 9 ; C = 10 ; C = 13 ), !,
    get_code(C2),
    skip_ws(C2, C1).
skip_ws(C, C) :-
    C \= -1.

read_digits(C, Acc, N) :-
    C >= 48, C =< 57, !,
    Acc1 is Acc * 10 + (C - 48),
    get_code(C2),
    read_digits(C2, Acc1, N).
read_digits(_, N, N).

print_counts(I, N) :-
    I > N, !,
    nl.
print_counts(I, N) :-
    ( I > 0 -> write(' ') ; true ),
    popcount(I, C),
    write(C),
    I1 is I + 1,
    print_counts(I1, N).

popcount(0, 0) :- !.
popcount(X, C) :-
    X > 0,
    X1 is X >> 1,
    R is X /\ 1,
    popcount(X1, C1),
    C is C1 + R.