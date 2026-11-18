read_n(N) :-
    current_input(In),
    read_line_to_string(In, Line),
    Line \== end_of_file,
    split_string(Line, " \t\r\n", " \t\r\n", Tokens),
    Tokens = [Token|_],
    number_string(N, Token).

hanoi(1, From, _, To) :-
    write(From), write(' '), write(To), nl.

hanoi(N, From, By, To) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, From, To, By),
    write(From), write(' '), write(To), nl,
    hanoi(N1, By, From, To).

main :-
    (   read_n(N)
    ->  Count is (1 << N) - 1,
        write(Count), nl,
        hanoi(N, 1, 2, 3)
    ;   true
    ).