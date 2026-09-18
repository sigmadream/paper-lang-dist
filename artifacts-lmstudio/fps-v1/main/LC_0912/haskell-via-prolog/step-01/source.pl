:- use_module(library(lists)).

merge([], Ys, Ys).
merge(Xs, [], Xs).
merge([X|Xs], [Y|Ys], [X|Z]) :-
    X =< Y,
    merge(Xs, [Y|Ys], Z).
merge([X|Xs], [Y|Ys], [Y|Z]) :-
    X > Y,
    merge([X|Xs], Ys, Z).

mergesort([], []).
mergesort([X], [X]).
mergesort(Xs, Z) :-
    length(Xs, N),
    N2 is N // 2,
    split_at(N2, Xs, A, B),
    mergesort(A, LA),
    mergesort(B, LB),
    merge(LA, LB, Z).

main :-
    read_line_to_string(_, Input),
    string_split(Input, ' ', Values),
    maplist(atom_number, Values, Integers),
    length(Integers, N),
    take(N, Integers, SubList),
    mergesort(SubList, Sorted),
    maplist(write, Sorted),
    nl.