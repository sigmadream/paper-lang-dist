main :-
    read_stream_to_codes(user_input, Codes),
    string_codes(Str, Codes),
    split_string(Str, " \n\r\t", " \n\r\t", Parts),
    maplist(number_string, Nums, Parts),
    solve(Nums).

solve([]).
solve([_]).
solve([N, M | Rest]) :-
    M >= 0,
    Need is 2 * M,
    length(Prefix, Need),
    append(Prefix, _, Rest),
    collect_edges(M, Prefix, Edges),
    solve_edges(N, Edges).

collect_edges(0, _, []).
collect_edges(K, [A, B | T], [A-B | Es]) :-
    K > 0,
    K1 is K - 1,
    collect_edges(K1, T, Es).

solve_edges(N, Edges) :-
    MaxV0 is max(1, N),
    max_endpoints(Edges, MaxV0, _MaxV),
    neighbors_of(1, Edges, Ns0),
    sort(Ns0, Ns1),
    remove_all(Ns1, 1, N1),
    findall(U,
            (member(V, N1),
             neighbors_of(V, Edges, Us),
             member(U, Us)),
            All2_0),
    sort(All2_0, All2_1),
    remove_all(All2_1, 1, All2_2),
    subtract_list(All2_2, N1, D2),
    length(N1, C1),
    length(D2, C2),
    Ans is C1 + C2,
    format('~w~n', [Ans]).

max_endpoints([], Max, Max).
max_endpoints([A-B | T], Cur, Max) :-
    C1 is max(Cur, A),
    C2 is max(C1, B),
    max_endpoints(T, C2, Max).

neighbors_of(V, Edges, Ns) :-
    findall(U,
            (member(A-B, Edges),
             ((A =:= V, U = B) ; (B =:= V, U = A))),
            Ns).

remove_all([], _, []).
remove_all([H | T], X, R) :-
    (   H =:= X
    ->  remove_all(T, X, R)
    ;   R = [H | R1],
        remove_all(T, X, R1)
    ).

subtract_list([], _, []).
subtract_list([H | T], L, R) :-
    (   memberchk(H, L)
    ->  subtract_list(T, L, R)
    ;   R = [H | R1],
        subtract_list(T, L, R1)
    ).