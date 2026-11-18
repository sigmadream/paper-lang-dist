main :-
    read_string(user_input, end_of_file, S),
    split_string(S, " \t\n\r", " \t\n\r", Tokens),
    ( Tokens == [] -> writeln(0)
    ; Tokens = [_] -> writeln(0)
    ; tokens_to_nums(Tokens, Nums),
      ( Nums = [N, M | Rest] ->
          ( take_edges(M, Rest, Edges) ->
              solve(N, Edges)
          ; writeln(0)
          )
      ; writeln(0)
      )
    ).

tokens_to_nums([], []).
tokens_to_nums([T|Ts], [N|Ns]) :-
    number_string(N, T),
    tokens_to_nums(Ts, Ns).

take_edges(0, _, []) :- !.
take_edges(M, [A,B|Ts], [e(A,B)|Es]) :-
    M > 0,
    M1 is M - 1,
    take_edges(M1, Ts, Es).

solve(_, Edges) :-
    neighbors(1, Edges, Ns1),
    sort(Ns1, S1),
    filter_not_one(S1, Level1),
    findall(U, (my_member(V, Level1), neighbors(V, Edges, Ns), my_member(U, Ns)), All2),
    sort(All2, S2),
    filter_not_one(S2, Tmp),
    filter_not_in(Level1, Tmp, Level2),
    length(Level1, L1),
    length(Level2, L2),
    Ans is L1 + L2,
    writeln(Ans).

neighbors(V, Edges, Ns) :-
    findall(U, (my_member(e(A,B), Edges), ( (A == V, U = B) ; (B == V, U = A) )), Ns).

filter_not_one([], []).
filter_not_one([1|Ts], Rs) :- !, filter_not_one(Ts, Rs).
filter_not_one([X|Ts], [X|Rs]) :- filter_not_one(Ts, Rs).

filter_not_in(_, [], []).
filter_not_in(List, [X|Xs], Rs) :-
    ( my_member(X, List) ->
        filter_not_in(List, Xs, Rs)
    ;   Rs = [X|Rs1],
        filter_not_in(List, Xs, Rs1)
    ).

my_member(X, [X|_]).
my_member(X, [_|T]) :- my_member(X, T).