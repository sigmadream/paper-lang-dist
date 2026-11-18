:- module(main, [main/0]).
:- use_module(library(dcgs)).

main :-
    read_line_to_codes(user_input, L1),
    parse_int(L1, N, []),
    read_line_to_codes(user_input, L2),
    parse_ints(L2, Ints),
    length(Ints, N),
    partition_zeroes(Ints, NonZero, Zeroes),
    append(NonZero, Zeroes, Result),
    format_result(Result, Codes),
    append(Codes, "\n", Out),
    put_chars(Out).

parse_int(Codes, N, Rest) :-
    number_codes(N, Codes).

parse_ints(Codes, Ints) :-
    (   Codes == [] -> Ints = []
    ;   split(Codes, Ints)
    ).

split(Codes, [N|Ns]) :-
    (   take_token(Codes, Tok, Rest0) ->
        (   Tok == [] -> split(Rest0, [N|Ns])
        ;   number_codes(N, Tok),
            skip_spaces(Rest0, Rest),
            split(Rest, Ns)
        )
    ;   Ns = [],
        N = 0,
        true
    ).

take_token([], [], []) :- !.
take_token([C|Cs], Tok, Rest) :-
    (   C == 32 -> Tok = [], Rest = [C|Cs]
    ;   take_token1([C|Cs], Tok, Rest)
    ).

take_token1([], [], []) :- !.
take_token1([C|Cs], Tok, Rest) :-
    (   C == 32 -> Tok = [], Rest = [C|Cs]
    ;   Tok = [C|T1], Rest = R1,
        take_token1(Cs, T1, R1)
    ).

take_token(Codes, Tok, Rest) :-
    take_token1(Codes, Tok, Rest0),
    Tok \= [],
    skip_spaces(Rest0, Rest).

skip_spaces([], []) :- !.
skip_spaces([32|Cs], Rest) :- !, skip_spaces(Cs, Rest).
skip_spaces([C|Cs], [C|Cs]).

split([], []) :- !.
split(Cs, Ns) :-
    skip_spaces(Cs, Cs1),
    (   Cs1 == [] -> Ns = []
    ;   take_token(Cs1, Tok, Rest),
        Tok \= [],
        number_codes(N, Tok),
        split(Rest, Ns)
    ).

partition_zeroes([], [], []).
partition_zeroes([X|Xs], [X|Nz], Z) :-
    X \= 0, !,
    partition_zeroes(Xs, Nz, Z).
partition_zeroes([X|Xs], Nz, [0|Z]) :-
    partition_zeroes(Xs, Nz, Z).

format_result([], []).
format_result([X], Cs) :- !, format_codes(X, Cs).
format_result([X|Xs], Cs) :-
    format_codes(X, Cs1),
    append(Cs1, " ", Cs2),
    format_result(Xs, Cs3),
    append(Cs2, Cs3, Cs).

format_codes(X, Cs) :-
    format(atom(A), "~d", [X]),
    atom_codes(A, Cs).

put_chars([]).
put_chars([C|Cs]) :- put_char(C), put_chars(Cs).