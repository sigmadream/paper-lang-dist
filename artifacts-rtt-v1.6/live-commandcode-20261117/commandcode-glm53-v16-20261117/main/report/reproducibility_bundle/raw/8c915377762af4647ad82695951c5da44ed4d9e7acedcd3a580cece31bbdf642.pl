:- module(main, [main/0]).

main :-
    read_line_to_codes(user_input, L1),
    ( L1 == end_of_file -> true
    ; parse_ints(L1, [N|_]),
      read_line_to_codes(user_input, L2),
      parse_ints(L2, Nums0),
      length(Nums0, N),
      partition_nonzero(Nums0, NonZero),
      length(NonZero, K),
      length(Zeros, K), maplist(=(0), Zeros),
      append(NonZero, Zeros, Result),
      format_result(Result)
    ).

partition_nonzero([], []).
partition_nonzero([X|Xs], Ys) :-
    ( X =\= 0 -> Ys = [X|Rest] ; Ys = Rest ),
    partition_nonzero(Xs, Rest).

format_result([]) :- nl.
format_result([X]) :- !, format("~d~n", [X]).
format_result([X|Xs]) :-
    format("~d ", [X]),
    format_result(Xs).

parse_ints(Codes, Nums) :-
    parse_tokens(Codes, Tokens),
    maplist(number_codes, Nums, Tokens).

parse_tokens([], []).
parse_tokens(Codes, [T|Ts]) :-
    skip_ws(Codes, Rest),
    ( Rest == [] -> T = [], Ts = []
    ; take_token(Rest, T, Remainder),
      parse_tokens(Remainder, Ts)
    ).

skip_ws([C|Cs], Rest) :-
    ( C == 32 ; C == 9 ; C == 10 ; C == 13 ),
    !, skip_ws(Cs, Rest).
skip_ws(Cs, Cs).

take_token(Codes, Token, Rest) :-
    take_nonws(Codes, Token, Rest).

take_nonws([], [], []).
take_nonws([C|Cs], Tok, Rest) :-
    ( C == 32 ; C == 9 ; C == 10 ; C == 13 ),
    !, Tok = [], Rest = [C|Cs].
take_nonws([C|Cs], [C|Tok], Rest) :-
    take_nonws(Cs, Tok, Rest).