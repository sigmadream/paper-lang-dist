read_all_lines(Ls) :-
    read_line_to_string(user_input, L),
    (   L == end_of_file ->
        Ls = []
    ;   Ls = [L|Rest],
        read_all_lines(Rest)
    ).

line_tokens([], []).
line_tokens([L|Ls], Ts) :-
    split_string(L, " \t\r\n", " \t\r\n", T1),
    line_tokens(Ls, T2),
    append(T1, T2, Ts).

strings_to_numbers([], []).
strings_to_numbers([S|Ss], [N|Ns]) :-
    number_string(N, S),
    strings_to_numbers(Ss, Ns).

take(0, L, [], L) :- !.
take(K, [X|Xs], [X|Ys], Rest) :-
    K > 0,
    K1 is K - 1,
    take(K1, Xs, Ys, Rest).

make_edges([], []).
make_edges([A,B|Rest], [A-B|Es]) :-
    make_edges(Rest, Es).

neighbors(V, Edges, Nbrs) :-
    findall(Y,
            (   member(A-B, Edges),
                (   A =:= V, Y = B
                ;   B =:= V, Y = A
                )
            ),
            Nbrs).

exclude_one([], []).
exclude_one([1|T], R) :- !, exclude_one(T, R).
exclude_one([H|T], [H|R]) :- H \= 1, exclude_one(T, R).

solve(Edges, Ans) :-
    neighbors(1, Edges, N1List),
    sort(N1List, S1),
    findall(Z,
            (   member(X, S1),
                neighbors(X, Edges, NX),
                member(Z, NX)
            ),
            L2),
    sort(L2, S2),
    append(S1, S2, All),
    sort(All, Union),
    exclude_one(Union, Filtered),
    length(Filtered, Ans).

main :-
    read_all_lines(Lines),
    line_tokens(Lines, Tokens),
    strings_to_numbers(Tokens, Nums),
    (   Nums = [_N, M | Rest] ->
        Len is 2 * M,
        take(Len, Rest, EdgeNums, _),
        make_edges(EdgeNums, Edges),
        solve(Edges, Ans),
        format("~d~n", [Ans])
    ;   true
    ).