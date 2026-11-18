:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  true
    ;   split_string(Line, " \t\r", " \t\r", [Token|_]),
        number_string(N, Token),
        Moves is (1 << N) - 1,
        write(Moves), nl,
        hanoi(N, 1, 2, 3),
        flush_output(user_output)
    ).

hanoi(1, Start, _, End) :-
    !,
    write(Start), write(' '), write(End), nl.
hanoi(N, Start, Mid, End) :-
    N1 is N - 1,
    hanoi(N1, Start, End, Mid),
    write(Start), write(' '), write(End), nl,
    hanoi(N1, Mid, Start, End).