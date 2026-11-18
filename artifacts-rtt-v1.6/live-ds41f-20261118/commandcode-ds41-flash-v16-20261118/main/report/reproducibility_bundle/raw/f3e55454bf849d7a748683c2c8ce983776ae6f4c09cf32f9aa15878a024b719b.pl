main :-
    read_string(user_input, end_of_file, Input),
    split_string(Input, " \t\n\r", " \t\n\r", Tokens),
    Tokens = [NTok|Rest],
    number_string(N, NTok),
    take_n(N, Rest, Values),
    partition_zero(Values, NonZero, ZeroCount),
    length(NonZero, NonZeroCount),
    ZeroCount is N - NonZeroCount,
    length(Zeros, ZeroCount),
    append(NonZero, Zeros, Result),
    print_values(Result).

take_n(0, _, []) :- !.
take_n(N, [Tok|Toks], [Value|Values]) :-
    N > 0,
    number_string(Value, Tok),
    N1 is N - 1,
    take_n(N1, Toks, Values).

partition_zero([], [], 0).
partition_zero([X|Xs], NonZero, ZeroCount) :-
    X =:= 0,
    !,
    partition_zero(Xs, NonZero, RestZeros),
    ZeroCount is RestZeros + 1.
partition_zero([X|Xs], [X|NonZero], ZeroCount) :-
    partition_zero(Xs, NonZero, ZeroCount).

print_values([]) :-
    nl.
print_values([X]) :-
    !,
    writeln(X).
print_values([X|Xs]) :-
    write(X),
    write(' '),
    print_values(Xs).