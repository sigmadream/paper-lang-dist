hanoi(1, From, _, To) :-
    write(From), write(' '), write(To), nl.
hanoi(N, From, Aux, To) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, From, To, Aux),
    write(From), write(' '), write(To), nl,
    hanoi(N1, Aux, From, To).

read_int(N) :-
    get_char(C),
    read_int_chars(C, Chars),
    number_chars(N, Chars).

read_int_chars(C, []) :-
    ( C == '\n' ; C == '\r' ; C == end_of_file ),
    !.
read_int_chars(C, [C|Chars]) :-
    get_char(Next),
    read_int_chars(Next, Chars).

main :-
    read_int(N),
    MoveCount is (1 << N) - 1,
    write(MoveCount), nl,
    hanoi(N, 1, 2, 3).