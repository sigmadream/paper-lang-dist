:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, atom).

hanoi(1, S, _, E, [[S, E]]).
hanoi(N, S, M, E, Moves) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, S, E, M, Ms1),
    hanoi(N1, M, S, E, Ms2),
    append(Ms1, [[S, E] | Ms2], Moves).

print_moves([]).
print_moves([[A, B] | T]) :-
    format("~d ~d~n", [A, B]),
    print_moves(T).

main :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        N = 0
    ; number_string(N, Line)
    ),
    ( N >= 1 ->
        hanoi(N, 1, 2, 3, Moves),
        length(Moves, Count),
        format("~d~n", [Count]),
        print_moves(Moves)
    ; true
    ).