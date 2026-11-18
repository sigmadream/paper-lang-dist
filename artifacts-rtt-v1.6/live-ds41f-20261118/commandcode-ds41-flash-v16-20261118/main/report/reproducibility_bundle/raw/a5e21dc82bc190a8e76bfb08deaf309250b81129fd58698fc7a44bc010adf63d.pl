main :-
    read_string(user_input, end_of_file, Input),
    split_string(Input, " \n\r\t", " \n\r\t", Tokens),
    ( Tokens = [] -> true
    ; Tokens = [NTok | RestTokens],
      token_to_int(NTok, N),
      take(N, RestTokens, ValueTokens),
      maplist(token_to_int, ValueTokens, Values),
      Values = [First | Rest],
      kadane(Rest, First, First, Best),
      format("~d~n", [Best])
    ).

token_to_int(Token, Number) :-
    number_string(Number, Token).

take(0, _, []) :- !.
take(N, [X | Xs], [X | Ys]) :-
    N > 0,
    N1 is N - 1,
    take(N1, Xs, Ys).

kadane([], _, Best, Best).
kadane([X | Xs], Current, Best, Final) :-
    Current1 is max(X, Current + X),
    Best1 is max(Best, Current1),
    kadane(Xs, Current1, Best1, Final).