main :-
    read_line_to_codes(user_input, Codes),
    number_codes(N, Codes),
    Count is (1 << N) - 1,
    format('~d~n', [Count]),
    hanoi(N, 1, 2, 3),
    halt.

hanoi(1, From, _, To) :- !,
    format('~d ~d~n', [From, To]).
hanoi(N, From, Via, To) :-
    N > 1,
    M is N - 1,
    hanoi(M, From, To, Via),
    format('~d ~d~n', [From, To]),
    hanoi(M, Via, From, To).