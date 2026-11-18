main :-
    ( read_int(N) ->
        M is (1 << N) - 1,
        number_codes(M, MC),
        hanoi_codes(N, 1, 2, 3, Moves0, []),
        append(MC, [10|Moves0], All),
        string_codes(Out, All),
        write(Out),
        flush_output
    ; true
    ).

read_int(N) :-
    get_code(C),
    ( C == -1 -> fail
    ; C >= 48, C =< 57 ->
        read_digits(C, Codes),
        number_codes(N, Codes)
    ; read_int(N)
    ).

read_digits(C, [C|Rest]) :-
    get_code(C2),
    ( C2 >= 48, C2 =< 57 ->
        read_digits(C2, Rest)
    ; Rest = []
    ).

hanoi_codes(1, A, _, C, L0, L) :-
    CA is A + 48,
    CC is C + 48,
    L0 = [CA, 32, CC, 10 | L].
hanoi_codes(N, A, B, C, L0, L) :-
    N > 1,
    N1 is N - 1,
    hanoi_codes(N1, A, C, B, L0, L1),
    CA is A + 48,
    CC is C + 48,
    L1 = [CA, 32, CC, 10 | L2],
    hanoi_codes(N1, B, A, C, L2, L).