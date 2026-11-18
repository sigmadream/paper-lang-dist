filter_nonempty([], []).
filter_nonempty([H|T], L) :-
    H == "",
    !,
    filter_nonempty(T, L).
filter_nonempty([H|T], [H|L]) :-
    filter_nonempty(T, L).

tokens(S, Tokens) :-
    split_string(S, " \n\r\t", " \n\r\t", Parts),
    filter_nonempty(Parts, Tokens).

take_n(0, L, [], L) :- !.
take_n(N, [H|T], [H|Ts], R) :-
    N > 0,
    N1 is N - 1,
    take_n(N1, T, Ts, R).

split_zeroes([], [], []).
split_zeroes([0|T], NZ, [0|Z]) :-
    split_zeroes(T, NZ, Z).
split_zeroes([H|T], [H|NZ], Z) :-
    H \= 0,
    split_zeroes(T, NZ, Z).

write_numbers([]) :-
    nl.
write_numbers([X]) :-
    !,
    write(X),
    nl.
write_numbers([X|Xs]) :-
    write(X),
    write(' '),
    write_numbers(Xs).

main :-
    read_string(user_input, end_of_file, Input),
    tokens(Input, Tokens),
    ( Tokens = [NToken|Rest] ->
        number_string(N, NToken),
        take_n(N, Rest, ValueTokens, _),
        maplist(number_string, Values, ValueTokens),
        split_zeroes(Values, NonZeroes, Zeroes),
        append(NonZeroes, Zeroes, Result),
        write_numbers(Result)
    ;
        true
    ).