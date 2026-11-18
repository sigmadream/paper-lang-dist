:- module(Main, [main/0]).

main :-
    read(N),
    read_numbers(N, Nums),
    max_subarray(Nums, Result),
    format("~d~n", [Result]).

read_numbers(0, []).
read_numbers(N, [X|Xs]) :-
    N > 0,
    read(X),
    N1 is N - 1,
    read_numbers(N1, Xs).

max_subarray([X], X).
max_subarray([H|T], Best) :-
    kadane(T, H, H, Best).

kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best, FinalBest) :-
    Cur1 is max(X, Cur + X),
    Best1 is max(Best, Cur1),
    kadane(Xs, Cur1, Best1, FinalBest).