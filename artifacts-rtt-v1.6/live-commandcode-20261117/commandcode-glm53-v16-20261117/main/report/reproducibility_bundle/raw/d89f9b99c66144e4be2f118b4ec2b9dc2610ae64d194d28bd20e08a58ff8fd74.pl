:- module(main, [main/0]).
:- use_module(library(apply)).
:- use_module(library(charsio)).
:- use_module(library(lists)).
:- use_module(library(pcre)).
:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, Line),
    ( Line == end_of_file -> true
    ; split_numbers(Line, [M, N]),
      sieve(N, Sieve),
      findall(P, (between(M, N, P), nth0(P, Sieve, 1)), Ps),
      maplist(writeln, Ps)
    ).

split_numbers(Line, Ns) :-
    split_string(Line, " ", " ", Parts),
    maplist(number_string, Ns, Parts).

sieve(N, Sieve) :-
    L is N + 1,
    length(Sieve, L),
    maplist(=(1), Sieve),
    set_zero(Sieve, 0),
    ( L > 1 -> set_zero(Sieve, 1) ; true ),
    I = 2,
    sieve_loop(I, N, Sieve).

sieve_loop(I, N, Sieve) :-
    I * I =< N, !,
    ( nth0(I, Sieve, 1) ->
        J is I * I,
        cross_out(J, I, N, Sieve)
    ; true
    ),
    I1 is I + 1,
    sieve_loop(I1, N, Sieve).
sieve_loop(_, _, _).

cross_out(J, I, N, Sieve) :-
    J =< N, !,
    set_zero(Sieve, J),
    J1 is J + I,
    cross_out(J1, I, N, Sieve).
cross_out(_, _, _, _).

set_zero(List, Index) :-
    nth0(Index, List, _, Rest),
    nth0(Index, NewList, 0, Rest),
    ( var(List) -> List = NewList ; true ),
    nb_setarg(succ(Index), List, 0).