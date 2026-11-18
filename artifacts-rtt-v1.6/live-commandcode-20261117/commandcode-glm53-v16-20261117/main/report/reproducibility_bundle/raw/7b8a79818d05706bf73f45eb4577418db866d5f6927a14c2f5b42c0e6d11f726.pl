:- module(main, [main/0]).

main :-
    current_input(In),
    read_line_to_codes(In, Line1),
    parse_int(Line1, N),
    read_line_to_codes(In, Line2),
    parse_ints(Line2, N, A),
    partition_nonzero(A, NonZero, Zeros),
    append(NonZero, Zeros, Result),
    atomic_list_concat(Result, ' ', Atom),
    format("~w~n", [Atom]).

parse_int(Codes, N) :-
    number_codes(N, Codes).

parse_ints(_, 0, []) :- !.
parse_ints(Codes, N, [X|Xs]) :-
    parse_token(Codes, X, Rest),
    N1 is N - 1,
    parse_ints(Rest, N1, Xs).

parse_token([], 0, []) :- !.
parse_token([C|Cs], X, Rest) :-
    (   C == 32
    ->  parse_token(Cs, X, Rest)
    ;   take_number([C|Cs], X, Rest)
    ).

take_number(Codes, X, Rest) :-
    take_digits(Codes, Digits, Rest),
    Digits \= [],
    number_codes(X, Digits).

take_digits([], [], []).
take_digits([C|Cs], [C|Ds], Rest) :-
    (   C == 32
    ->  Rest = []
    ;   take_digits(Cs, Ds, Rest)
    ).

partition_nonzero([], [], []).
partition_nonzero([X|Xs], [X|NonZero], Zeros) :-
    X \== 0,
    !,
    partition_nonzero(Xs, NonZero, Zeros).
partition_nonzero([X|Xs], NonZero, [X|Zeros]) :-
    partition_nonzero(Xs, NonZero, Zeros).