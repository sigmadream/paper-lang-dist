pow2(0, 1) :- !.
pow2(N, P) :-
    N > 0,
    N1 is N - 1,
    pow2(N1, P0),
    P is P0 * 2.

hanoi(1, S, _, E) :- !,
    format('~d ~d~n', [S, E]).
hanoi(N, S, M, E) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, S, E, M),
    format('~d ~d~n', [S, E]),
    hanoi(N1, M, S, E).

main :-
    read_token(user_input, N),
    integer(N),
    pow2(N, P),
    Count is P - 1,
    format('~d~n', [Count]),
    hanoi(N, 1, 2, 3).