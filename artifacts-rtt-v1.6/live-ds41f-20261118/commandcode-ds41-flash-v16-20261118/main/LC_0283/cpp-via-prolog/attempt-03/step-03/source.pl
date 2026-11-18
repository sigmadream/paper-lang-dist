main :-
    read_all_codes(user_input, Codes),
    parse_ints(Codes, Ints),
    ( Ints = [N|Rest] ->
        take_n(N, Rest, Values),
        partition_zero(Values, NonZeros, Zeros),
        append_lists(NonZeros, Zeros, Result),
        write_ints(Result)
    ;
        nl
    ).

read_all_codes(Stream, Codes) :-
    get_code(Stream, C),
    ( C =:= -1 ->
        Codes = []
    ;
        Codes = [C|Rest],
        read_all_codes(Stream, Rest)
    ).

parse_ints(Codes, Ints) :-
    parse_ints_skip(Codes, Ints).

parse_ints_skip([], []).
parse_ints_skip([C|Cs], Ints) :-
    ( is_ws(C) ->
        parse_ints_skip(Cs, Ints)
    ; C =:= 45 ->
        parse_digits(Cs, 0, D, Rest),
        I is -D,
        Ints = [I|Ints1],
        parse_ints_skip(Rest, Ints1)
    ; C >= 48, C =< 57 ->
        parse_digits([C|Cs], 0, D, Rest),
        Ints = [D|Ints1],
        parse_ints_skip(Rest, Ints1)
    ;
        parse_ints_skip(Cs, Ints)
    ).

is_ws(32).
is_ws(9).
is_ws(10).
is_ws(13).
is_ws(12).

parse_digits([C|Cs], Acc, D, Rest) :-
    C >= 48,
    C =< 57,
    !,
    Acc1 is Acc * 10 + (C - 48),
    parse_digits(Cs, Acc1, D, Rest).
parse_digits(Rest, Acc, Acc, Rest).

take_n(0, _, []) :- !.
take_n(N, [], []) :- N > 0, !.
take_n(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take_n(N1, Xs, Ys).

partition_zero([], [], []).
partition_zero([X|Xs], NZ, Z) :-
    ( X =:= 0 ->
        NZ = NZ1,
        Z = [0|Z1]
    ;
        NZ = [X|NZ1],
        Z = Z1
    ),
    partition_zero(Xs, NZ1, Z1).

append_lists([], Ys, Ys).
append_lists([X|Xs], Ys, [X|Zs]) :-
    append_lists(Xs, Ys, Zs).

write_ints([]) :-
    nl.
write_ints([X|Xs]) :-
    write(X),
    write_ints_rest(Xs),
    nl.

write_ints_rest([]).
write_ints_rest([X|Xs]) :-
    write(' '),
    write(X),
    write_ints_rest(Xs).