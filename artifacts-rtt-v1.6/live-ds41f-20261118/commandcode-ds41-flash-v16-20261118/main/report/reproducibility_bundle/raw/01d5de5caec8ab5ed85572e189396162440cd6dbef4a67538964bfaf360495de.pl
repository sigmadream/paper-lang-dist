:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, Codes),
    (   Codes == end_of_file
    ->  true
    ;   parse_two(Codes, M, N),
        run(M, N)
    ).

parse_two(Codes, M, N) :-
    skip_ws(Codes, C1),
    parse_int(C1, M, Rest),
    skip_ws(Rest, C2),
    parse_int(C2, N, _).

skip_ws([C|Cs], Rest) :-
    (   C =:= 32
    ;   C =:= 9
    ;   C =:= 10
    ;   C =:= 13
    ),
    !,
    skip_ws(Cs, Rest).
skip_ws(Cs, Cs).

parse_int(Codes, Num, Rest) :-
    parse_digits(Codes, 0, Num, Rest).

parse_digits([C|Cs], Acc, Num, Rest) :-
    C >= 48,
    C =< 57,
    !,
    Acc1 is Acc * 10 + (C - 48),
    parse_digits(Cs, Acc1, Num, Rest).
parse_digits(Rest, Acc, Acc, Rest).

run(M, N) :-
    (   N >= 1
    ->  functor(Arr, p, N),
        sieve(2, N, Arr),
        output(M, N, Arr)
    ;   true
    ).

sieve(I, N, Arr) :-
    I2 is I * I,
    I2 =< N,
    !,
    arg(I, Arr, V),
    (   V == 0
    ->  true
    ;   mark(I, N, Arr)
    ),
    I1 is I + 1,
    sieve(I1, N, Arr).
sieve(_, _, _).

mark(I, N, Arr) :-
    J is I * I,
    mark_loop(J, I, N, Arr).

mark_loop(J, Step, N, Arr) :-
    J =< N,
    !,
    setarg(J, Arr, 0),
    J1 is J + Step,
    mark_loop(J1, Step, N, Arr).
mark_loop(_, _, _, _).

output(I, N, Arr) :-
    I > N,
    !.
output(I, N, Arr) :-
    output_one(I, Arr),
    I1 is I + 1,
    output(I1, N, Arr).

output_one(I, Arr) :-
    I >= 2,
    arg(I, Arr, V),
    (   V == 0
    ->  true
    ;   format("~d~n", [I])
    ).
output_one(_, _).