:- module(main, [main/0]).

main :-
    read_line_to_codes(user_input, Codes),
    ( Codes == end_of_file ->
        true
    ;
        phrase(numbers(Codes), [M, N]),
        sieve(N, IsPrime),
        print_primes(M, N, IsPrime)
    ).

numbers(Codes) --> ws, num(M), ws, num(N), ws, { [M, N] }.
ws --> [C], { C =< 32 }, !, ws.
ws --> [].
num(X) --> digits(Ds), { number_codes(X, Ds) }, !.
digits([D|Ds]) --> [C], { C >= 48, C =< 57 }, !, digits(Ds), { D = [C] }.
digits([]) --> [].

sieve(N, IsPrime) :-
    Size is N + 1,
    functor(IsPrime, arr, Size),
    ( for(I, 1, Size), param(IsPrime) do
        arg(I, IsPrime, true)
    ),
    ( I is 1, arg(1, IsPrime, V1), V1 = false, true ; true ),
    setarg(1, IsPrime, false),
    ( N >= 1 ->
        ( arg(2, IsPrime, _), setarg(2, IsPrime, true) )
    ; true ),
    MaxI is floor(sqrt(N)),
    ( for(I, 2, MaxI), param(IsPrime, N) do
        arg(I, IsPrime, true) ->
            Start is I * I,
            ( for(J, Start, N, I), param(IsPrime) do
                setarg(J, IsPrime, false)
            )
        ; true
    ).

print_primes(M, N, IsPrime) :-
    ( for(I, M, N), param(IsPrime) do
        arg(I, IsPrime, true) ->
            write(I), nl
        ; true
    ).