use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   split_string(Line, " \t\r\n", " \t\r\n", Parts),
        (   Parts = [First|_]
        ->  number_string(N, First),
            Count is (1 << N) - 1,
            writeln(Count),
            hanoi(N, 1, 2, 3)
        ;   true
        )
    ).

hanoi(1, S, _, E) :-
    write(S), write(' '), write(E), nl.

hanoi(N, S, M, E) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, S, E, M),
    write(S), write(' '), write(E), nl,
    hanoi(N1, M, S, E).