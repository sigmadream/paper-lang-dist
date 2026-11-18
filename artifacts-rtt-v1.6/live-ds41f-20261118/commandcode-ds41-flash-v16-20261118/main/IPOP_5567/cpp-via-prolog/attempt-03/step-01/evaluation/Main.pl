main :-
    catch(read_string(user_input, end_of_file, Str), _, Str = ""),
    split_string(Str, " \t\r\n", " \t\r\n", Tokens0),
    parse_ints(Tokens0, Nums),
    (   Nums = [N, M | Rest] ->
        Len is 2 * M,
        take(Len, Rest, EdgeNums),
        pair_edges(EdgeNums, Edges),
        solve(N, Edges)
    ;   true
    ).

parse_ints([], []).
parse_ints([T|Ts], Ns) :-
    (   T == "" ->
        Ns = Rs
    ;   catch(number_string(N, T), _, fail) ->
        Ns = [N|Rs]
    ;   Ns = Rs
    ),
    parse_ints(Ts, Rs).

take(0, _, []) :- !.
take(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take(N1, Xs, Ys).

pair_edges([], []).
pair_edges([A, B | T], [A-B | Es]) :-
    pair_edges(T, Es).
pair_edges([_], []).

solve(_, Edges) :-
    neighbors(1, Edges, L1),
    sort(L1, S1),
    gather_neighbors(S1, Edges, L2),
    filter_vertices(L2, S1, L2Filtered),
    sort(L2Filtered, S2),
    length(S1, C1),
    length(S2, C2),
    Ans is C1 + C2,
    format("~d~n", [Ans]).

neighbors(V, Edges, Ns) :-
    findall(U,
            (member(A-B, Edges),
             (V =:= A, U = B ; V =:= B, U = A)),
            Ns).

gather_neighbors([], _, []).
gather_neighbors([V|Vs], Edges, Ns) :-
    neighbors(V, Edges, NsV),
    gather_neighbors(Vs, Edges, NsRest),
    append(NsV, NsRest, Ns).

filter_vertices([], _, []).
filter_vertices([V|Vs], S1, Out) :-
    (   V =:= 1 ->
        Out = Rest
    ;   memberchk(V, S1) ->
        Out = Rest
    ;   Out = [V|Rest]
    ),
    filter_vertices(Vs, S1, Rest).