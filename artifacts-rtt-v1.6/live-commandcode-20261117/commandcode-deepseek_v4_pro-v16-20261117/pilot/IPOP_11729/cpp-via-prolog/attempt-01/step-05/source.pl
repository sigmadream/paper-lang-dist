:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    number_string(N, Line),
    MoveCount is (1 << N) - 1,
    writeln(MoveCount),
    hanoi(N, 1, 2, 3).

hanoi(1, From, _, To) :-
    write(From), write(' '), write(To), nl.
hanoi(N, From, Aux, To) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, From, To, Aux),
    write(From), write(' '), write(To), nl,
    hanoi(N1, Aux, From, To).