:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", [MStr, NStr]),
    atom_string(MAtom, MStr),
    atom_number(MAtom, M),
    atom_string(NAtom, NStr),
    atom_number(NAtom, N),
    sqrt_int(N, SMax),
    primes_up_to(SMax, BasePrimes),
    sieve_range(M, N, BasePrimes).

sqrt_int(N, S) :-
    S is floor(sqrt(N)).

primes_up_to(Limit, Primes) :-
    findall(P, (between(2, Limit, P), prime_small(P)), Primes).

prime_small(P) :-
    prime_small_(P, 2).

prime_small_(P, D) :-
    D * D > P, !.
prime_small_(P, D) :-
    (P mod D) =:= 0, !, fail.
prime_small_(P, D) :-
    D1 is D + 1,
    prime_small_(P, D1).

sieve_range(M, N, BasePrimes) :-
    sieve_blocks(M, N, 1000, BasePrimes).

sieve_blocks(L, N, _, _) :-
    L > N, !.
sieve_blocks(L, N, BlockSize, BasePrimes) :-
    R is min(N, L + BlockSize - 1),
    Len is R - L + 1,
    functor(Arr, block, Len),
    init_block(Arr, Len),
    mark_primes(BasePrimes, L, R, Arr),
    output_block(L, R, Arr),
    L1 is R + 1,
    sieve_blocks(L1, N, BlockSize, BasePrimes).

init_block(Arr, Len) :-
    forall(between(1, Len, I), setarg(I, Arr, 1)).

mark_primes([], _, _, _).
mark_primes([P|Ps], L, R, Arr) :-
    P2 is P * P,
    (   P2 > R
    ->  true
    ;   First is max(P2, ((L + P - 1) // P) * P),
        (   First =< R
        ->  mark_multiples(First, R, P, L, Arr)
        ;   true
        )
    ),
    mark_primes(Ps, L, R, Arr).

mark_multiples(J, R, P, L, Arr) :-
    J =< R,
    Idx is J - L + 1,
    setarg(Idx, Arr, 0),
    J1 is J + P,
    mark_multiples(J1, R, P, L, Arr).
mark_multiples(_, _, _, _, _).

output_block(L, R, Arr) :-
    output_from(L, R, L, Arr).

output_from(I, R, L, Arr) :-
    I =< R,
    (   I >= 2,
        Idx is I - L + 1,
        arg(Idx, Arr, 1)
    ->  format('~d~n', [I])
    ;   true
    ),
    I1 is I + 1,
    output_from(I1, R, L, Arr).
output_from(_, _, _, _).