main :-
    read_string(current_input, end_of_file, Input),
    split_string(Input, " \t\n\r", " \t\n\r", RawTokens),
    include([T] >> (T \= ""), RawTokens, Tokens),
    maplist([S,N] >> number_string(N,S), Tokens, Numbers),
    ( Numbers = [N|Rest] ->
        ( N > 0 ->
            take(N, Rest, Values),
            ( Values = [H|T] ->
                kadane(T, H, H, Best),
                writeln(Best)
            ; true
            )
        ; true
        )
    ; true
    ).

take(0, _, []) :- !.
take(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take(N1, Xs, Ys).
take(_, [], []).

kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best0, Best) :-
    Cur1 is max(X, Cur + X),
    Best1 is max(Best0, Cur1),
    kadane(Xs, Cur1, Best1, Best).