main :-
    read_all_tokens(Tokens),
    Tokens = [NStr|Rest],
    number_string(N, NStr),
    take_n(N, Rest, ValueStrs, _),
    strings_to_numbers(ValueStrs, Values),
    move_zeroes(Values, Result),
    print_values(Result).

read_all_tokens(Tokens) :-
    read_all_tokens([], Tokens).

read_all_tokens(Acc, Tokens) :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        Tokens = Acc
    ;   split_string(Line, " \t\r\n", " \t\r\n", Parts0),
        filter_empty(Parts0, Parts),
        append(Acc, Parts, Acc1),
        read_all_tokens(Acc1, Tokens)
    ).

filter_empty([], []).
filter_empty([X|Xs], Ys) :-
    ( X == "" ->
        Ys = Ys1
    ;   Ys = [X|Ys1]
    ),
    filter_empty(Xs, Ys1).

take_n(0, Rest, [], Rest) :- !.
take_n(N, [X|Xs], [X|Ys], Rest) :-
    N > 0,
    N1 is N - 1,
    take_n(N1, Xs, Ys, Rest).

strings_to_numbers([], []).
strings_to_numbers([S|Ss], [V|Vs]) :-
    number_string(V, S),
    strings_to_numbers(Ss, Vs).

move_zeroes(List, Result) :-
    collect_nonzero(List, NonZero, ZeroCount),
    make_zeros(ZeroCount, Zeros),
    append(NonZero, Zeros, Result).

collect_nonzero([], [], 0).
collect_nonzero([X|Xs], NonZero, ZeroCount) :-
    collect_nonzero(Xs, RestNonZero, RestZeroCount),
    ( X =:= 0 ->
        NonZero = RestNonZero,
        ZeroCount is RestZeroCount + 1
    ;   NonZero = [X|RestNonZero],
        ZeroCount = RestZeroCount
    ).

make_zeros(0, []) :- !.
make_zeros(N, [0|Zs]) :-
    N > 0,
    N1 is N - 1,
    make_zeros(N1, Zs).

print_values([]) :-
    nl.
print_values([X|Xs]) :-
    write(X),
    print_rest(Xs).

print_rest([]) :-
    nl.
print_rest([X|Xs]) :-
    write(' '),
    write(X),
    print_rest(Xs).