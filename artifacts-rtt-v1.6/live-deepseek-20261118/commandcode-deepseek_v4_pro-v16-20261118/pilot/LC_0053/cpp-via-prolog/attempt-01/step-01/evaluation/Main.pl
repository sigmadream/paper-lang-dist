main :-
    read(N),
    read_n_ints(N, Ints),
    max_subarray(Ints, Result),
    writeln(Result).

read_n_ints(0, []) :- !.
read_n_ints(N, [X|Xs]) :-
    N > 0,
    read(X),
    N1 is N - 1,
    read_n_ints(N1, Xs).

max_subarray([First|Rest], Best) :-
    max_subarray_loop(Rest, First, First, Best).

max_subarray_loop([], _, Best, Best).
max_subarray_loop([X|Rest], Cur, Best0, Best) :-
    Sum is Cur + X,
    (   X > Sum
    ->  Cur1 = X
    ;   Cur1 = Sum
    ),
    (   Cur1 > Best0
    ->  Best1 = Cur1
    ;   Best1 = Best0
    ),
    max_subarray_loop(Rest, Cur1, Best1, Best).