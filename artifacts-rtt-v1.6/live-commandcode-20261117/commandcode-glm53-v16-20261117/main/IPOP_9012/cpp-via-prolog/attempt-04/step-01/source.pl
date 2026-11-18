main :-
    read_line_to_codes(user_input, L),
    ( L == end_of_file -> true
    ; number_codes(T, L),
      loop(T)
    ).

loop(0) :- !.
loop(N) :-
    N > 0,
    read_line_to_codes(user_input, L),
    ( L == end_of_file -> true
    ; check(L, 0, R),
      ( R == ok(0) -> Out = "YES" ; Out = "NO" ),
      format("~s~n", [Out]),
      N1 is N - 1,
      loop(N1)
    ).

check([], B, ok(B)).
check([0'(|Cs], B, R) :-
    B1 is B + 1,
    check(Cs, B1, R).
check([_)|Cs], B, R) :-
    B1 is B - 1,
    ( B1 < 0 -> R = bad
    ; check(Cs, B1, R)
    ).