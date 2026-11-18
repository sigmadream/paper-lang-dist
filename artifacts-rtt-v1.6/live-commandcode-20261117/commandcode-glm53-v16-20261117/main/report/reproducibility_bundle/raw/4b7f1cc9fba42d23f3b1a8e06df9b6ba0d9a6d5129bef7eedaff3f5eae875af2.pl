:- module(main, [main/0]).
:- use_module(library(dcg/basics)).

main :-
    current_input(In),
    read_line_to_codes(In, L1),
    ( L1 == end_of_file -> true
    ; number_codes(N, L1),
      read_line_to_codes(In, L2),
      number_codes(M, L2),
      read_edges(M, In, Edges),
      length(Dist, N),
      maplist(=(-1), Dist),
      nth0(1, Dist, 0, Dist0),
      bfs([1], Edges, Dist0, 0, Ans),
      format("~d~n", [Ans])
    ).

read_edges(0, _, []) :- !.
read_edges(M, In, [u-v|Es]) :-
    read_line_to_codes(In, L),
    append(Us, [0' | Rest], L),
    append(Vs, [0' | _], Rest),
    number_codes(U, Us),
    number_codes(V, Vs),
    M1 is M - 1,
    read_edges(M1, In, Es).

bfs([], _, _, Ans, Ans).
bfs([C|Q], Edges, Dist, Acc, Ans) :-
    nth0(C, Dist, DC),
    ( DC =< 2 ->
        findall(Nx, (member(u-v, Edges), (u == C, v = Nx ; v == C, u = Nx)), Ns0),
        sort(Ns0, Ns),
        process(Ns, Q, Dist, DC, Acc, Q2, Dist2, Acc2),
        bfs(Q2, Edges, Dist2, Acc2, Ans)
    ; bfs(Q, Edges, Dist, Acc, Ans)
    ).

process([], Q, Dist, _, Acc, Q, Dist, Acc).
process([N|Ns], Q, Dist, DC, Acc, Q3, Dist3, Acc3) :-
    nth0(N, Dist, DN),
    ( DN == -1 ->
        DN1 is DC + 1,
        nth0(N, Dist, DN1, Dist1),
        Acc1 is Acc + 1,
        process(Ns, [N|Q], Dist1, DC, Acc1, Q3, Dist3, Acc3)
    ; process(Ns, Q, Dist, DC, Acc, Q3, Dist3, Acc3)
    ).