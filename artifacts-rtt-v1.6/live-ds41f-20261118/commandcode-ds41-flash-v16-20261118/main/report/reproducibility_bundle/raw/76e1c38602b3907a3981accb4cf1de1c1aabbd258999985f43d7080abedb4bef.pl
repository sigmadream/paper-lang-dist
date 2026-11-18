:- use_module(library(readutil)).

main :-
    current_input(Stream),
    read_line_to_codes(Stream, Codes),
    parse_two(Codes, M, N),
    Size is N + 1,
    functor(Flags, f, Size),
    fill(1, Size, Flags),
    setarg(1, Flags, 0),
    setarg(2, Flags, 0),
    sieve(2, N, Flags),
    output(M, N, Flags).

parse_two(Codes, M, N) :-
    skip_ws(Codes, C1),
    parse_int(C1, M, C2),
    skip_ws(C2, C3),
    parse_int(C3, N, _).

skip_ws([C|T], R) :-
    (C =:= 32 ; C =:= 9 ; C =:= 10 ; C =:= 13),
    !,
    skip_ws(T, R).
skip_ws(L, L).

parse_int(Codes, V, Rest) :-
    parse_digits(Codes, 0, V, Rest).

parse_digits([C|T], Acc, V, Rest) :-
    C >= 48,
    C =< 57,
    !,
    Acc1 is Acc * 10 + (C - 48),
    parse_digits(T, Acc1, V, Rest).
parse_digits(Rest, Acc, Acc, Rest).

fill(I, Size, Flags) :-
    I =< Size,
    !,
    setarg(I, Flags, 1),
    I1 is I + 1,
    fill(I1, Size, Flags).
fill(_, _, _).

sieve(P, N, Flags) :-
    P * P =< N,
    !,
    Idx is P + 1,
    arg(Idx, Flags, V),
    (V =:= 1 -> Start is P * P, mark(Start, N, P, Flags) ; true),
    P1 is P + 1,
    sieve(P1, N, Flags).
sieve(_, _, _).

mark(J, N, P, Flags) :-
    J =< N,
    !,
    Idx is J + 1,
    setarg(Idx, Flags, 0),
    J1 is J + P,
    mark(J1, N, P, Flags).
mark(_, _, _, _).

output(I, N, Flags) :-
    I =< N,
    !,
    Idx is I + 1,
    arg(Idx, Flags, V),
    (V =:= 1 -> writeln(I) ; true),
    I1 is I + 1,
    output(I1, N, Flags).
output(_, _, _).