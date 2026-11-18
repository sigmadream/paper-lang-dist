:- use_module(library(readutil)).

hanoi(1, F, _, T) :-
    format('~d ~d~n', [F, T]).
hanoi(N, F, A, T) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, F, T, A),
    format('~d ~d~n', [F, T]),
    hanoi(N1, A, F, T).

main :-
    read_line_to_string(user_input, Line),
    number_string(N, Line),
    Count is (1 << N) - 1,
    write(Count), nl,
    hanoi(N, 1, 2, 3).