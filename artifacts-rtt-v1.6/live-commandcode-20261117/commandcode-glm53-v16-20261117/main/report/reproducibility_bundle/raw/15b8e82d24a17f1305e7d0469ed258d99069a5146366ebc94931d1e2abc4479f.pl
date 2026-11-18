:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, codes).

read_int(I) :-
    read_line_to_codes(user_input, Cs),
    Cs \== end_of_file,
    phrase(int(I), Cs), !.

read_ints(0, []) :- !.
read_ints(N, [X|Xs]) :- read_int(X), N1 is N-1, read_ints(N1, Xs).

int(I) -->
    ws,
    ( "-" -> Ds, { number_codes(I, [0'-|Ds]) }
    ; Ds, { number_codes(I, Ds) }
    ),
    ws.

ws --> " ", !, ws.
ws --> [].

digits([D|Ds]) --> digit(D), digits(Ds).
digits([D]) --> digit(D).

digit(D) --> [C], { C >= 0'0, C =< 0'9 }.

main :-
    catch(read_int(N), _, fail),
    ( integer(N), N >= 1 ->
        read_ints(N, A),
        partition_zeros(A, NonZ, Zeros),
        append(NonZ, Zeros, R),
        atomic_list_join(R)
    ; true ).

partition_zeros([], [], []).
partition_zeros([X|Xs], [X|Nz], Z) :- X =\= 0, !, partition_zeros(Xs, Nz, Z).
partition_zeros([X|Xs], Nz, [X|Z]) :- partition_zeros(Xs, Nz, Z).

atomic_list_join([]).
atomic_list_join([X]) :- !, write(X), nl.
atomic_list_join([X|Xs]) :- write(X), write(' '), atomic_list_join(Xs).