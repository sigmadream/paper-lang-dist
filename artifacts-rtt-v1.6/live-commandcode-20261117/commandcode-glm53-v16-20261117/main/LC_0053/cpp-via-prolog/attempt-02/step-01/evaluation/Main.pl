:- module(main, [main/0]).
:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, L1),
    parse_int(L1, N),
    read_line_to_codes(user_input, L2),
    split_ints(L2, As),
    length(As, N),
    (   As = [First|Rest]
    ->  kadane(Rest, First, First, Best),
        format("~d~n", [Best])
    ;   true
    ).

kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best0, Best) :-
    Cur1 is max(X, Cur + X),
    Best1 is max(Best0, Cur1),
    kadane(Xs, Cur1, Best1, Best).

parse_int(Codes, N) :-
    number_codes(N, Codes).

split_ints(Codes, Nums) :-
    split_whitespace(Codes, Tokens),
    maplist(parse_int, Tokens, Nums).

split_whitespace(Codes, Tokens) :-
    split_string(Codes, " ", "", Strs),
    exclude(empty_string, Strs, TokensS),
    maplist(string_codes, TokensS, Tokens).

empty_string(S) :- S == "".