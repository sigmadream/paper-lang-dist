:- use_module(library(readutil)).

main :-
    catch(run, _, true).

run :-
    read_line_to_codes(user_input, L),
    ( L == end_of_file -> true
    ; parse_two(L, M, N),
      solve(M, N)
    ).

parse_two(L, M, N) :-
    append_codes_num(L, Rest, M),
    append_codes_num(Rest, _, N).

append_codes_num(L, Rest, Num) :-
    skip_ws(L, L1),
    collect_digits(L1, Rest, Ds),
    number_codes(Num, Ds).

skip_ws([C|T], R) :- ( C =:= 32 ; C =:= 9 ; C =:= 10 ; C =:= 13 ), !, skip_ws(T, R).
skip_ws(L, L).

collect_digits([C|T], Rest, [C|Ds]) :-
    C >= 48, C =< 57, !,
    collect_digits(T, Rest, Ds).
collect_digits(L, L, []).

solve(M, N) :-
    N1 is N + 1,
    functor(Arr, a, N1 is N1,
    init_arr(Arr, N1),
    setarg(1, Arr, 0),
    setarg(2, Arr, 0),
    sieve(Arr, 2, N),
    print_range(Arr, M, N).

init_arr(_, 0) :- !.
init_arr(Arr, K) :-
    setarg(K, Arr, 1),
    K1 is K - 1,
    init_arr(Arr, K1).

sieve(Arr, I, N) :-
    I * I =< N, !,
    K is I + 1,
    ( arg(K, Arr, 1) ->
        S is I * I,
        mark(Arr, S, I, N)
    ; true
    ),
    I1 is I + 1,
    sieve(Arr, I1, N).
sieve(_, _, _).

mark(Arr, J, I, N) :-
    J =< N, !,
    K is J + 1,
    setarg(K, Arr, 0),
    J1 is J + I,
    mark(Arr, J1, I, N).
mark(_, _, _, _).

print_range(Arr, M, N) :-
    M =< N, !,
    K is M + 1,
    ( arg(K, Arr, 1) ->
        format("~d~n", [M])
    ; true
    ),
    M1 is M + 1,
    print_range(Arr, M1, N).
print_range(_, _, _).