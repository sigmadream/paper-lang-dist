main :-
    (   read(N),
        integer(N)
    ->  read_numbers(N, Nums),
        move_zeroes(Nums, Result),
        write_numbers(Result)
    ;   nl
    ).

read_numbers(0, []) :- !.
read_numbers(N, [X|Xs]) :-
    N > 0,
    read(X),
    N1 is N - 1,
    read_numbers(N1, Xs).

move_zeroes(Nums, Result) :-
    split_zeroes(Nums, NonZeroes, ZeroCount),
    length(Zeros, ZeroCount),
    append(NonZeroes, Zeros, Result).

split_zeroes([], [], 0).
split_zeroes([X|Xs], NonZeroes, ZeroCount) :-
    split_zeroes(Xs, Rest, RestZeroCount),
    (   X =:= 0
    ->  NonZeroes = Rest,
        ZeroCount is RestZeroCount + 1
    ;   NonZeroes = [X|Rest],
        ZeroCount = RestZeroCount
    ).

write_numbers([]) :- nl.
write_numbers([X|Xs]) :-
    write(X),
    write_tail(Xs).

write_tail([]) :- nl.
write_tail([X|Xs]) :-
    write(' '),
    write(X),
    write_tail(Xs).