main :-
    read_all_codes(Codes),
    tokenize_codes(Codes, Tokens),
    parse_tokens(Tokens, Numbers),
    process(Numbers).

read_all_codes(Codes) :-
    get_code(user_input, C),
    ( C =:= -1 ->
        Codes = []
    ;   Codes = [C|Rest],
        read_all_codes(Rest)
    ).

tokenize_codes([], []).
tokenize_codes([C|Cs], Tokens) :-
    is_space(C), !,
    tokenize_codes(Cs, Tokens).
tokenize_codes([C|Cs], [Token|Tokens]) :-
    \+ is_space(C),
    take_token([C|Cs], TokenCodes, Rest),
    atom_codes(Token, TokenCodes),
    tokenize_codes(Rest, Tokens).

take_token([], [], []).
take_token([C|Cs], [C|T], Rest) :-
    \+ is_space(C), !,
    take_token(Cs, T, Rest).
take_token(Cs, [], Cs).

is_space(C) :- C =:= 32.
is_space(C) :- C =:= 9.
is_space(C) :- C =:= 10.
is_space(C) :- C =:= 13.
is_space(C) :- C =:= 12.
is_space(C) :- C =:= 11.

parse_tokens([], []).
parse_tokens([Tok|Toks], Ns) :-
    ( atom_number(Tok, N) ->
        Ns = [N|Rest]
    ;   Ns = Rest
    ),
    parse_tokens(Toks, Rest).

process([]) :-
    nl.
process([N|Rest]) :-
    take_n(Rest, N, Values),
    partition_zeros(Values, NonZeros, Zeros),
    append(NonZeros, Zeros, Result),
    print_values(Result).

take_n(_, N, []) :-
    N =< 0, !.
take_n([], _, []) :-
    !.
take_n([H|T], N, [H|R]) :-
    N > 0,
    N1 is N - 1,
    take_n(T, N1, R).

partition_zeros([], [], []).
partition_zeros([H|T], [H|N], Z) :-
    H =\= 0,
    partition_zeros(T, N, Z).
partition_zeros([0|T], N, [0|Z]) :-
    partition_zeros(T, N, Z).

print_values([]) :-
    nl.
print_values([H|T]) :-
    write(H),
    print_rest(T).

print_rest([]) :-
    nl.
print_rest([H|T]) :-
    write(' '),
    write(H),
    print_rest(T).