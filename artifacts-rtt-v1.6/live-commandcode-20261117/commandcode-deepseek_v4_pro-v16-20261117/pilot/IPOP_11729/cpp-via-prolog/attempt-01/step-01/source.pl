main :-
    read_string(user_input, _, Input),
    split_string(Input, " \t\n", " \t\n", [S|_]),
    number_string(N, S),
    hanoi(N, 1, 2, 3, Moves, []),
    length(Moves, Len),
    format('~d~n', [Len]),
    print_moves(Moves).

print_moves([]).
print_moves([[From, To]|Rest]) :-
    format('~d ~d~n', [From, To]),
    print_moves(Rest).

hanoi(1, From, _Aux, To, [[From, To]|Z], Z).
hanoi(N, From, Aux, To, Moves, Z) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, From, To, Aux, Moves, Z1),
    Z1 = [[From, To]|Z2],
    hanoi(N1, Aux, From, To, Z2, Z).