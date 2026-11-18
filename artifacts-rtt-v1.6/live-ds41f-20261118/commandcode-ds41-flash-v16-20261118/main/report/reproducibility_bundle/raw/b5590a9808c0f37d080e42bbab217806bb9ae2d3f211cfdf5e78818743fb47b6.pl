main :-
    ( read(N) -> true ; N = 1 ),
    ( read(M) -> true ; M = 0 ),
    N1 is N + 1,
    make_empty(N1, Empty),
    build_edges(M, Empty, Adj),
    get_nth0(1, Adj, Direct),
    sort(Direct, DirectSorted),
    collect_neighbors(DirectSorted, Adj, [], All0),
    sort(All0, AllSorted),
    subtract_list(AllSorted, DirectSorted, S1),
    subtract_list(S1, [1], S2),
    length(DirectSorted, C1),
    length(S2, C2),
    Ans is C1 + C2,
    write(Ans), nl.

make_empty(0, []) :- !.
make_empty(K, [[]|T]) :-
    K > 0,
    K1 is K - 1,
    make_empty(K1, T).

build_edges(0, A, A) :- !.
build_edges(K, A0, A) :-
    K > 0,
    read(U),
    read(V),
    add_neighbor(U, V, A0, A1),
    add_neighbor(V, U, A1, A2),
    K1 is K - 1,
    build_edges(K1, A2, A).

add_neighbor(V, U, A0, A) :-
    get_nth0(V, A0, Old),
    New = [U|Old],
    replace_nth0(V, A0, New, A).

get_nth0(0, [X|_], X) :- !.
get_nth0(I, [_|T], X) :-
    I > 0,
    I1 is I - 1,
    get_nth0(I1, T, X).

replace_nth0(0, [_|T], X, [X|T]) :- !.
replace_nth0(I, [H|T], X, [H|R]) :-
    I > 0,
    I1 is I - 1,
    replace_nth0(I1, T, X, R).

collect_neighbors([], _, Acc, Acc).
collect_neighbors([X|Xs], Adj, Acc, Out) :-
    get_nth0(X, Adj, L),
    append_list(L, Acc, Acc1),
    collect_neighbors(Xs, Adj, Acc1, Out).

append_list([], L, L).
append_list([H|T], L, [H|R]) :-
    append_list(T, L, R).

subtract_list([], _, []).
subtract_list([H|T], L, R) :-
    ( member_list(H, L) ->
        subtract_list(T, L, R)
    ;
        R = [H|R1],
        subtract_list(T, L, R1)
    ).

member_list(H, [H|_]) :- !.
member_list(H, [_|T]) :-
    member_list(H, T).