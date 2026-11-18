:- module(main, [main/0]).
:- use_module(library(clpfd)).

main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " ", " ", Parts),
    maplist(number_string, [M, N], Parts),
    unique_paths(M, N, Answer),
    format("~d~n", [Answer]).

unique_paths(1, _, 1) :- !.
unique_paths(_, 1, 1) :- !.
unique_paths(M, N, R) :-
    MM is M - 1, NN is N - 1,
    findall(dp, (true, false), _), % placeholder removed below
    dp_loop(MM, NN, R).

dp_loop(1, _, R) :- !, R = 1.
dp_loop(_, 0, R) :- !, R = 1.
dp_loop(M, N, R) :-
    length(Row, N),
    maplist(=(1), Row),
    M1 is M - 1,
    iterate(M1, Row, Final),
    last(Final, R).

iterate(0, Row, Row) :- !.
iterate(I, Row, Out) :-
    I > 0,
    prefix_sum(Row, NewRow),
    I1 is I - 1,
    iterate(I1, NewRow, Out).

prefix_sum(Row, NewRow) :-
    prefix_sum_(Row, 0, NewRow).

prefix_sum_([], _, []).
prefix_sum_([H|T], Acc, [H2|T2]) :-
    Acc2 is Acc + H,
    H2 = Acc2,
    prefix_sum_(T, Acc2, T2).