:- use_module(library(system)).

read_int(N) :-
    get_code(C),
    read_int_(C, N).

read_int_(-1, -1) :- !.
read_int_(C, N) :-
    (C < 48 ; C > 57), !,
    get_code(C2),
    read_int_(C2, N).
read_int_(C, N) :-
    read_digits(C, 0, N).

read_digits(C, A, N) :-
    C >= 48, C =< 57, !,
    A1 is A * 10 + (C - 48),
    get_code(C2),
    read_digits(C2, A1, N).
read_digits(_, N, N).

conflict_any(_, _, []) :- !, fail.
conflict_any(R, C, [(R2, C2) | _]) :-
    (   C =:= C2
    ;   D is abs(R - R2),
        E is abs(C - C2),
        D =:= E
    ), !
    ;
    conflict_any(R, C, [_ | T]).

conflict_any(R, C, [_ | T]) :-
    conflict_any(R, C, T).

count_all(0, _, _, _) :-
    b_getval(ans, A),
    A1 is A + 1,
    b_setval(ans, A1).
count_all(Rem, N, Row, Placed) :-
    Rem > 0,
    Rem1 is Rem - 1,
    Row1 is Row + 1,
    between(0, N - 1, Col),
    \+ conflict_any(Row, Col, Placed),
    count_all(Rem1, N, Row1, [(Row, Col) | Placed]).

main :-
    read_int(N),
    (   N < 0
    ->  true
    ;   b_setval(ans, 0),
        count_all(N, N, 0, []),
        b_getval(ans, A),
        write(A),
        nl
    ).