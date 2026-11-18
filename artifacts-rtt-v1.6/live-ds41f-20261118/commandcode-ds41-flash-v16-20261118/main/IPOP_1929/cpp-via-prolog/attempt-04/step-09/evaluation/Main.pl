:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, Codes),
    (   Codes == end_of_file
    ->  true
    ;   parse_pair(Codes, M, N),
        run(M, N)
    ).

parse_pair(Codes, M, N) :-
    string_codes(Str, Codes),
    split_string(Str, " \t\r\n", " \t\r\n", Parts),
    Parts = [MS, NS | _],
    number_string(M, MS),
    number_string(N, NS).

run(M, N) :-
    (   N < 2
    ->  true
    ;   Arity is N - 1,
        functor(A, a, Arity),
        init_true(A, 1, Arity),
        sieve_loop(A, 2, N),
        output_primes(M, N, A)
    ).

init_true(_, I, Max) :-
    I > Max,
    !.
init_true(A, I, Max) :-
    nb_setarg(I, A, true),
    I1 is I + 1,
    init_true(A, I1, Max).

sieve_loop(A, P, N) :-
    P * P > N,
    !.
sieve_loop(A, P, N) :-
    Idx is P - 1,
    arg(Idx, A, IsPrime),
    (   IsPrime == true
    ->  J is P * P,
        mark_multiples(A, J, N, P)
    ;   true
    ),
    P1 is P + 1,
    sieve_loop(A, P1, N).

mark_multiples(A, J, N, P) :-
    J > N,
    !.
mark_multiples(A, J, N, P) :-
    Idx is J - 1,
    nb_setarg(Idx, A, false),
    J1 is J + P,
    mark_multiples(A, J1, N, P).

output_primes(M, N, _) :-
    M > N,
    !.
output_primes(M, N, A) :-
    (   M >= 2
    ->  Idx is M - 1,
        arg(Idx, A, IsPrime),
        (   IsPrime == true
        ->  writeln(M)
        ;   true
        )
    ;   true
    ),
    M1 is M + 1,
    output_primes(M1, N, A).