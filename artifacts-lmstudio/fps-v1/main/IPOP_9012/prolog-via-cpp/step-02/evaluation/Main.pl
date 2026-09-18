:- use_module(library(readutil)).

main :-
    read_line_to_string(_, T),
    string_to_integer(T, N),
    process(N).

process(0) :- !.
process(N) :-
    read_line_to_string(_, S),
    is_balanced(S),
    write('YES'), nl,
    M is N - 1,
    process(M).

is_balanced([]) :- !.
is_balanced([')'|T]) :- !, fail.
is_balanced(['('|T]) :-
    count_balance(T, 1, 0).

count_balance([], 0, _) :- !.
count_balance([')'|T], Depth, Count) :-
    Depth > 0,
    NewCount is Count - 1,
    NewDepth is Depth - 1,
    count_balance(T, NewDepth, NewCount).
count_balance(['('|T], Depth, Count) :-
    NewDepth is Depth + 1,
    NewCount is Count + 1,
    count_balance(T, NewDepth, NewCount).