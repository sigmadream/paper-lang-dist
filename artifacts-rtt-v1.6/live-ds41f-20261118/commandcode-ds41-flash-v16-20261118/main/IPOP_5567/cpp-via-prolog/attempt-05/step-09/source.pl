:- use_module(library(readutil)).

main :-
    read_all_codes(Codes),
    split_ws(Codes, Tokens),
    ( Tokens = [N, M | Rest] ->
        take_edges(M, N, Rest, Edges),
        ( N < 1 ->
            Ans = 0
        ; solve(N, Edges, Ans)
        )
    ; Ans = 0
    ),
    write(Ans), nl.

read_all_codes(Codes) :-
    read_lines(Codes, []).

read_lines(Codes, Tail) :-
    read_line_to_codes(user_input, Line),
    ( Line == end_of_file ->
        Codes = Tail
    ; append(Line, [32|Rest], Codes),
      read_lines(Rest, Tail)
    ).

split_ws([], []) :- !.
split_ws([C|Cs], Tokens) :-
    C =< 32, !,
    split_ws(Cs, Tokens).
split_ws(Cs, [Tok|Toks]) :-
    take_word(Cs, Word, Rest),
    number_codes(Tok, Word),
    split_ws(Rest, Toks).

take_word([], [], []).
take_word([C|Cs], [C|Ws], Rest) :-
    C > 32, !,
    take_word(Cs, Ws, Rest).
take_word(Rest, [], Rest).

take_edges(0, _, _, []) :- !.
take_edges(M, N, [A,B|Rest], Edges) :-
    M > 0,
    M1 is M - 1,
    ( A >= 1, A =< N, B >= 1, B =< N ->
        Edges = [A-B|Edges1]
    ; Edges = Edges1
    ),
    take_edges(M1, N, Rest, Edges1).
take_edges(_, _, _, []).

solve(_N, Edges, Ans) :-
    neighbors(1, Edges, D1List),
    sort(D1List, D1),
    findall(V, (member(U, D1), neighbors(U, Edges, Ns), member(V, Ns)), D2All),
    sort(D2All, D2Sorted),
    exclude_vertices(D2Sorted, D1, 1, D2),
    length(D1, C1),
    length(D2, C2),
    Ans is C1 + C2.

neighbors(U, Edges, Ns) :-
    findall(V, (member(A-B, Edges), edge_neighbor(A, B, U, V)), Ns).

edge_neighbor(A, _, U, B) :- A =:= U.
edge_neighbor(_, B, U, A) :- B =:= U.

exclude_vertices([], _, _, []).
exclude_vertices([V|Vs], D1, One, Out) :-
    ( V =:= One ->
        exclude_vertices(Vs, D1, One, Out)
    ; memberchk(V, D1) ->
        exclude_vertices(Vs, D1, One, Out)
    ; Out = [V|Rest],
      exclude_vertices(Vs, D1, One, Rest)
    ).