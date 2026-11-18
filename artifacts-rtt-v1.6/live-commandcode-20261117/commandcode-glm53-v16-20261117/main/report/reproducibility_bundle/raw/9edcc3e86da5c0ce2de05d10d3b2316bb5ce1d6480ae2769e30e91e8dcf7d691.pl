:- use_module(library(pcre)).
:- use_module(library(readutil)).

main :-
    current_input(In),
    read_line_to_codes(In, Cs),
    ( Cs == end_of_file -> true
    ; phrase(nums([M, N]), Cs, _),
      solve(M, N)
    ).

ws --> [C], { code_type(C, space) }, !, ws.
ws --> [].

num(X) --> ws, digits(D), { D = [_|_], number_codes(X, D) }.

nums([X]) --> num(X).
nums([X|T]) --> num(X), nums(T).

digits([D|T]) --> [D], { between(48, 57, D) }, !, digits(T).
digits([]) --> [].

solve(M, N) :-
    Ar is N + 1,
    functor(S, sieve, Ar),
    ( Ar > 1 -> nb_setarg(1, S, false) ; true ),
    ( Ar > 2 -> nb_setarg(2, S, false) ; true ),
    init_flags(3, N, S),
    Limit is floor(sqrt(N)),
    sieve_loop(2, Limit, N, S),
    output(M, N, S).

init_flags(I, N, _) :- I > N, !.
init_flags(I, N, S) :-
    nb_setarg(I, S, true),
    I1 is I + 1,
    init_flags(I1, N, S).

sieve_loop(I, Limit, _, _) :- I > Limit, !.
sieve_loop(I, Limit, N, S) :-
    ( arg(I, S, true) ->
        Start is I * I,
        mark(Start, I, N, S)
    ; true
    ),
    I1 is I + 1,
    sieve_loop(I1, Limit, N, S).

mark(J, _, N, _) :- J > N, !.
mark(J, Step, N, S) :-
    nb_setarg(J, S, false),
    J1 is J + Step,
    mark(J1, Step, N, S).

output(I, N, _) :- I > N, !.
output(I, N, S) :-
    ( arg(I, S, true) ->
        write(I), nl
    ; true
    ),
    I1 is I + 1,
    output(I1, N, S).