main :-
    read_string(user_input, end_of_file, Input),
    split_string(Input, " \t\r\n", " \t\r\n", Tokens0),
    exclude(empty_string, Tokens0, Tokens),
    ( Tokens = [NTok|Rest] ->
        number_string(N, NTok),
        take_numbers(N, Rest, Nums),
        move_zeroes(Nums, Result),
        print_list(Result)
    ; true
    ).

empty_string(S) :-
    S == "".

take_numbers(0, _, []) :- !.
take_numbers(N, [Tok|Toks], [Num|Nums]) :-
    N > 0,
    number_string(Num, Tok),
    N1 is N - 1,
    take_numbers(N1, Toks, Nums).

move_zeroes(List, Result) :-
    include(is_nonzero, List, NonZeros),
    include(is_zero, List, Zeros),
    append(NonZeros, Zeros, Result).

is_nonzero(X) :- X =\= 0.
is_zero(X) :- X =:= 0.

print_list([]) :-
    nl.
print_list([X|Xs]) :-
    write(X),
    print_rest(Xs).

print_rest([]) :-
    nl.
print_rest([X|Xs]) :-
    write(' '),
    write(X),
    print_rest(Xs).