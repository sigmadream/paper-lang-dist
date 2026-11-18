:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t", " \t", Tokens),
    Tokens = [First|_],
    atom_number(First, N),
    Count is (1 << N) - 1,
    format("~w~n", [Count]),
    hanoi(N, 1, 2, 3).

hanoi(1, S, _, E) :-
    !,
    format("~w ~w~n", [S, E]).
hanoi(N, S, M, E) :-
    N1 is N - 1,
    hanoi(N1, S, E, M),
    format("~w ~w~n", [S, E]),
    hanoi(N1, M, S, E).