:- use_module(library(lists)).

main :-
    read_all_codes([], Codes),
    tokenize(Codes, Tokens),
    ( Tokens = [NT|Rest] -> number_codes(N, NT) ; N = 0 ),
    take_n(Rest, N, Nums),
    ( Nums = [F|Fs] ->
        kadane(Fs, F, F, Best),
        write(Best), nl
    ; true ).

read_all_codes(Acc, Codes) :-
    get_code(user_input, C),
    ( C =:= -1 -> reverse(Acc, Codes)
    ; read_all_codes([C|Acc], Codes)
    ).

space(C) :- member(C, [32, 10, 13, 9, 12]).

tokenize(Codes, Tokens) :-
    tokens(Codes, [], [], Rev),
    reverse(Rev, Tokens).

tokens([], Curr, Acc, Result) :-
    ( Curr = [] -> Result = Acc
    ; reverse(Curr, Tok), Result = [Tok|Acc]
    ).
tokens([C|Cs], Curr, Acc, Result) :-
    ( space(C) ->
        ( Curr = [] -> tokens(Cs, [], Acc, Result)
        ; reverse(Curr, Tok), tokens(Cs, [], [Tok|Acc], Result)
        )
    ; tokens(Cs, [C|Curr], Acc, Result)
    ).

take_n(_, 0, []) :- !.
take_n([T|Ts], N, [V|Vs]) :-
    number_codes(V, T),
    N1 is N - 1,
    take_n(Ts, N1, Vs).

kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best, Result) :-
    C1 is max(X, Cur + X),
    B1 is max(Best, C1),
    kadane(Xs, C1, B1, Result).