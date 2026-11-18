main :-
    read_n(N),
    Count is (1 << N) - 1,
    with_output_to(string(Out),
        ( format("~w~n", [Count]),
          hanoi(N, 1, 2, 3)
        )),
    format("~s", [Out]).

hanoi(1, A, _, C) :-
    !,
    format("~w ~w~n", [A, C]).
hanoi(N, A, B, C) :-
    N > 1,
    N1 is N - 1,
    hanoi(N1, A, C, B),
    format("~w ~w~n", [A, C]),
    hanoi(N1, B, A, C).

read_n(N) :-
    get_char(C0),
    skip_ws(C0, C),
    read_digits(C, 0, N).

skip_ws(C, C) :-
    C == end_of_file,
    !.
skip_ws(C, C1) :-
    char_type(C, space),
    !,
    get_char(C2),
    skip_ws(C2, C1).
skip_ws(C, C).

read_digits(C, Acc, N) :-
    C \== end_of_file,
    char_type(C, digit),
    !,
    char_code(C, Code),
    D is Code - 48,
    Acc1 is Acc * 10 + D,
    get_char(C2),
    read_digits(C2, Acc1, N).
read_digits(_, N, N).