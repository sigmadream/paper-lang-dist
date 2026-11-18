:- use_module(library(readutil)).

main :-
    read_line_to_string(user_input, Line),
    split_string(Line, " \t\r\n", " \t\r\n", Parts),
    (   Parts = [MStr, NStr | _],
        number_string(M, MStr),
        number_string(N, NStr)
    ->  print_primes(M, N)
    ;   true
    ).

print_primes(M, N) :-
    (   N < 2
    ->  true
    ;   Len is N - 1,
        functor(Arr, a, Len),
        fill_flags(1, Len, Arr),
        sieve(2, N, Arr),
        print_range(M, N, Arr)
    ).

fill_flags(I, Len, _Arr) :-
    I > Len,
    !.
fill_flags(I, Len, Arr) :-
    setarg(I, Arr, true),
    I1 is I + 1,
    fill_flags(I1, Len, Arr).

sieve(I, N, _Arr) :-
    I * I > N,
    !.
sieve(I, N, Arr) :-
    Idx is I - 1,
    arg(Idx, Arr, true),
    !,
    Start is I * I,
    mark_multiples(Start, N, I, Arr),
    I1 is I + 1,
    sieve(I1, N, Arr).
sieve(I, N, Arr) :-
    I1 is I + 1,
    sieve(I1, N, Arr).

mark_multiples(J, N, _Step, _Arr) :-
    J > N,
    !.
mark_multiples(J, N, Step, Arr) :-
    Idx is J - 1,
    setarg(Idx, Arr, false),
    J1 is J + Step,
    mark_multiples(J1, N, Step, Arr).

print_range(M, N, Arr) :-
    (   M < 2
    ->  Start = 2
    ;   Start = M
    ),
    print_from(Start, N, Arr).

print_from(I, N, _Arr) :-
    I > N,
    !.
print_from(I, N, Arr) :-
    Idx is I - 1,
    arg(Idx, Arr, true),
    !,
    format('~d~n', [I]),
    I1 is I + 1,
    print_from(I1, N, Arr).
print_from(I, N, Arr) :-
    I1 is I + 1,
    print_from(I1, N, Arr).