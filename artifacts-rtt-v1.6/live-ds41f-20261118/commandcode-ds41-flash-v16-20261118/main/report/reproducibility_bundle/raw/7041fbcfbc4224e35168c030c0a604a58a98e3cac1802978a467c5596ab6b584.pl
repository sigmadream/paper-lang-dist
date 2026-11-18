main :-
    read_line_to_string(user_input, Line),
    number_string(N, Line),
    Count is (1 << N) - 1,
    number_codes(Count, CountCodes),
    hanoi_codes(N, 1, 2, 3, Moves, []),
    append(CountCodes, [10|Moves], Codes),
    string_codes(Out, Codes),
    write(Out),
    flush_output.

hanoi_codes(1, S, _, E, [Sc, 32, Ec, 10|Tail], Tail) :-
    Sc is S + 48,
    Ec is E + 48.
hanoi_codes(N, S, M, E, Codes, Tail) :-
    N > 1,
    N1 is N - 1,
    hanoi_codes(N1, S, E, M, Codes, T1),
    Sc is S + 48,
    Ec is E + 48,
    T1 = [Sc, 32, Ec, 10|T2],
    hanoi_codes(N1, M, S, E, T2, Tail).