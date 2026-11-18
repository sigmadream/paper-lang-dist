:- use_module(library(readutil)).

main :-
    read_line_to_codes(user_input, Codes),
    ( Codes == end_of_file ->
        true
    ; parse_two(Codes, M, N),
      S is floor(sqrt(N)),
      base_sieve(S, BasePrimes),
      process_segments(M, N, BasePrimes)
    ).

parse_two(Codes, M, N) :-
    skip_spaces(Codes, C1),
    parse_int(C1, M, Rest),
    skip_spaces(Rest, C2),
    parse_int(C2, N, _).

skip_spaces([C|Cs], Rest) :-
    C =< 32,
    !,
    skip_spaces(Cs, Rest).
skip_spaces(Rest, Rest).

parse_int(Codes, Num, Rest) :-
    parse_digits(Codes, 0, Num, Rest).

parse_digits([C|Cs], Acc, Num, Rest) :-
    C >= 0'0,
    C =< 0'9,
    !,
    Acc1 is Acc * 10 + (C - 0'0),
    parse_digits(Cs, Acc1, Num, Rest).
parse_digits(Rest, Acc, Acc, Rest).

base_sieve(S, Primes) :-
    S < 2,
    !,
    Primes = [].
base_sieve(S, Primes) :-
    S1 is S + 1,
    functor(Array, base, S1),
    setarg(1, Array, 0),
    setarg(2, Array, 0),
    SqrtS is floor(sqrt(S)),
    base_mark(2, SqrtS, S, Array),
    collect_primes(2, S, Array, Primes).

base_mark(I, SqrtS, S, Array) :-
    I =< SqrtS,
    !,
    arg(I+1, Array, V),
    ( var(V) ->
        J is I * I,
        base_mark_multiples(I, J, S, Array)
    ; true
    ),
    I1 is I + 1,
    base_mark(I1, SqrtS, S, Array).
base_mark(_, _, _, _).

base_mark_multiples(I, J, S, Array) :-
    J =< S,
    !,
    setarg(J+1, Array, 0),
    J1 is J + I,
    base_mark_multiples(I, J1, S, Array).
base_mark_multiples(_, _, _, _).

collect_primes(I, S, Array, Primes) :-
    I =< S,
    !,
    arg(I+1, Array, V),
    ( var(V) ->
        Primes = [I|Rest]
    ; Primes = Rest
    ),
    I1 is I + 1,
    collect_primes(I1, S, Array, Rest).
collect_primes(_, _, _, []).

process_segments(Low, N, _) :-
    Low > N,
    !.
process_segments(Low, N, BasePrimes) :-
    High0 is Low + 10000 - 1,
    ( High0 > N ->
        High = N
    ; High = High0
    ),
    Len is High - Low + 1,
    functor(Array, seg, Len),
    ( Low =:= 1 ->
        setarg(1, Array, 0)
    ; true
    ),
    mark_segment(BasePrimes, Low, High, Array),
    print_segment(Low, High, Array),
    Low1 is High + 1,
    process_segments(Low1, N, BasePrimes).

mark_segment([], _, _, _).
mark_segment([P|Ps], Low, High, Array) :-
    mark_prime(P, Low, High, Array),
    mark_segment(Ps, Low, High, Array).

mark_prime(P, Low, High, Array) :-
    P2 is P * P,
    ( P2 > High ->
        true
    ; Q is (Low + P - 1) // P,
      Start0 is Q * P,
      ( P2 > Start0 ->
          Start = P2
      ; Start = Start0
      ),
      ( Start =< High ->
          mark_segment_multiples(Start, P, High, Low, Array)
      ; true
      )
    ).

mark_segment_multiples(X, P, High, Low, Array) :-
    X =< High,
    !,
    Idx is X - Low + 1,
    setarg(Idx, Array, 0),
    X1 is X + P,
    mark_segment_multiples(X1, P, High, Low, Array).
mark_segment_multiples(_, _, _, _, _).

print_segment(Low, High, Array) :-
    print_segment_loop(Low, High, Low, Array).

print_segment_loop(X, High, Low, Array) :-
    X =< High,
    !,
    Idx is X - Low + 1,
    arg(Idx, Array, V),
    ( var(V) ->
        format("~d~n", [X])
    ; true
    ),
    X1 is X + 1,
    print_segment_loop(X1, High, Low, Array).
print_segment_loop(_, _, _, _).