:- module(main, [main/0]).
:- use_module(library(charsio)).

hanoi(1, S, _, E, [[S, E]|T], T) :- !.
hanoi(N, S, M, E, Moves, Tail) :-
    N1 is N - 1,
    hanoi(N1, S, E, M, Moves, T1),
    T1 = [[S, E]|T2],
    hanoi(N1, M, S, E, T2, Tail).

write_moves([]).
write_moves([[A, B]|Rest]) :-
    format("~A ~A~n", [A, B]),
    write_moves(Rest).

read_n(N) :-
    read_line_to_codes(user_input, Codes),
    ( Codes == end_of_file -> N = 0
    ; number_codes(N, Codes) -> true
    ; N = 0
    ).

main :-
    read_n(N),
    ( integer(N), N >= 1 ->
        hanoi(N, 1, 2, 3, Moves, []),
        length(Moves, C),
        format("~A~n", [C]),
        write_moves(Moves)
    ; true
    ).