:- module(main, [main/0]).
:- use_module(library(charsio)).

hanoi(1, A, _, C) :- !,
    format("~d ~d~n", [A, C]).
hanoi(N, A, B, C) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, A, C, B),
    format("~d ~d~n", [A, C]),
    hanoi(N1, B, A, C).

main :-
    current_input(In),
    read_line_to_codes(In, Line),
    ( Line == end_of_file -> true
    ; line_number(Line, N),
      N >= 1,
      Count is 2^N - 1,
      format("~d~n", [Count]),
      hanoi(N, 1, 2, 3) ).

line_number(Codes, N) :-
    number_codes(N, Codes).