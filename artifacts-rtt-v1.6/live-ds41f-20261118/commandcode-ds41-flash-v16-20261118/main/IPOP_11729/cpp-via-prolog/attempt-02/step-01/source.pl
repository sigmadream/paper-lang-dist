main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   atom_number(Line, N),
        integer(N),
        Count is (1 << N) - 1,
        write(Count), nl,
        hanoi(N, 1, 2, 3),
        flush_output(user_output)
    ).

hanoi(1, S, _, E) :- !,
    write(S), write(' '), write(E), nl.
hanoi(N, S, M, E) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, S, E, M),
    write(S), write(' '), write(E), nl,
    hanoi(N1, M, S, E).