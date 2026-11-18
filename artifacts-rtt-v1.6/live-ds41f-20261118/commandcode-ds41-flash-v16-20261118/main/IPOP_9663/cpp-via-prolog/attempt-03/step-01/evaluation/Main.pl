main :-
    read_all_codes(user_input, Codes),
    filter_digits(Codes, Digits),
    number_codes(N, Digits),
    count_queens(N, Count),
    write(Count),
    nl.

read_all_codes(Stream, Codes) :-
    get_code(Stream, C),
    ( C =:= -1 ->
        Codes = []
    ;   Codes = [C|Rest],
        read_all_codes(Stream, Rest)
    ).

filter_digits([], []).
filter_digits([C|Cs], Ds) :-
    ( C >= 48, C =< 57 ->
        Ds = [C|Rest],
        filter_digits(Cs, Rest)
    ;   filter_digits(Cs, Ds)
    ).

count_queens(N, Count) :-
    Full is (1 << N) - 1,
    nq_solve(N, Full, 0, 0, 0, 0, 0, Count).

nq_solve(N, _, R, _, _, _, Acc, Count) :-
    R =:= N,
    !,
    Count is Acc + 1.
nq_solve(N, Full, R, Col, D1, D2, Acc, Count) :-
    Used is (Col \/ D1 \/ D2) /\ Full,
    Avail is Full - Used,
    nq_loop(N, Full, R, Col, D1, D2, Avail, Acc, Count).

nq_loop(_, _, _, _, _, _, 0, Acc, Acc) :- !.
nq_loop(N, Full, R, Col, D1, D2, Avail, Acc, Count) :-
    Bit is Avail /\ -Avail,
    Rest is Avail - Bit,
    NewCol is Col \/ Bit,
    NewD1 is ((D1 \/ Bit) << 1) /\ Full,
    NewD2 is ((D2 \/ Bit) >> 1) /\ Full,
    R1 is R + 1,
    nq_solve(N, Full, R1, NewCol, NewD1, NewD2, Acc, Acc1),
    nq_loop(N, Full, R, Col, D1, D2, Rest, Acc1, Count).