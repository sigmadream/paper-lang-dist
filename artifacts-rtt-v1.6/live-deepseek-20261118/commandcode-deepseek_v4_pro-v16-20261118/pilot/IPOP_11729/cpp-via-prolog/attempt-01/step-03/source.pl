main :-
    read_line_to_string(user_input, Line),
    ( Line = end_of_file -> true
    ; number_string(N, Line),
      Count is 2^N - 1,
      format("~d~n", [Count]),
      hanoi(N, 1, 2, 3)
    ).

hanoi(1, From, _, To) :-
    format("~d ~d~n", [From, To]).
hanoi(N, From, Mid, To) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, From, To, Mid),
    format("~d ~d~n", [From, To]),
    hanoi(N1, Mid, From, To).