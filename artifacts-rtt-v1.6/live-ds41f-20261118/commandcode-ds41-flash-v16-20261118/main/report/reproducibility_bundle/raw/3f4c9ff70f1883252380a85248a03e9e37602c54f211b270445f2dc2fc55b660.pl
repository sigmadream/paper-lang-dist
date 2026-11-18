:- use_module(library(readutil)).

main :-
    read_all_tokens(Tokens),
    ( Tokens = [NTok|Rest] ->
        number_string(N, NTok),
        take(N, Rest, NumTokens),
        tokens_to_numbers(NumTokens, Nums),
        move_zeroes(Nums, Result),
        print_values(Result)
    ; print_values([])
    ).

read_all_tokens(Tokens) :-
    read_all_tokens([], Tokens).

read_all_tokens(Acc, Tokens) :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        Tokens = Acc
    ; split_string(Line, " \t\r\n", " \t\r\n", Ts),
      append(Acc, Ts, Acc1),
      read_all_tokens(Acc1, Tokens)
    ).

take(0, _, []) :- !.
take(N, [X|Xs], [X|Ys]) :-
    N > 0,
    N1 is N - 1,
    take(N1, Xs, Ys).

tokens_to_numbers([], []).
tokens_to_numbers([T|Ts], [N|Ns]) :-
    number_string(N, T),
    tokens_to_numbers(Ts, Ns).

move_zeroes(List, Result) :-
    collect_nonzeros(List, NonZeros, ZeroCount),
    make_zeros(ZeroCount, Zeros),
    append(NonZeros, Zeros, Result).

collect_nonzeros(List, NonZeros, ZeroCount) :-
    collect_nonzeros(List, [], RevNonZeros, 0, ZeroCount),
    reverse(RevNonZeros, NonZeros).

collect_nonzeros([], Acc, Acc, ZC, ZC).
collect_nonzeros([X|Xs], Acc, NonZeros, ZC0, ZC) :-
    ( X =:= 0 ->
        ZC1 is ZC0 + 1,
        collect_nonzeros(Xs, Acc, NonZeros, ZC1, ZC)
    ; collect_nonzeros(Xs, [X|Acc], NonZeros, ZC0, ZC)
    ).

make_zeros(0, []).
make_zeros(N, [0|T]) :-
    N > 0,
    N1 is N - 1,
    make_zeros(N1, T).

print_values([]) :- nl.
print_values([X]) :- write(X), nl.
print_values([X|Xs]) :-
    write(X),
    write(' '),
    print_values(Xs).