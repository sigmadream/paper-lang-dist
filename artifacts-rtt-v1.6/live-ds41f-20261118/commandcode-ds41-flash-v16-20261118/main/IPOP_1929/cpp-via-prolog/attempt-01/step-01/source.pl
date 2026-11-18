:- use_module(library(readutil)).

main :-
    ( read_m_n(M, N) ->
        sieve_array(N, Array),
        output_primes(M, N, Array)
    ; true
    ).

read_m_n(M, N) :-
    read_line_to_codes(user_input, Line),
    Line \== end_of_file,
    split_ws(Line, Tokens),
    Tokens = [TokenM, TokenN | _],
    number_codes(M, TokenM),
    number_codes(N, TokenN).

split_ws([], []).
split_ws([C|Cs], Tokens) :-
    ( C =< 32 ->
        split_ws(Cs, Tokens)
    ; take_token([C|Cs], Token, Rest),
      Tokens = [Token|TokensRest],
      split_ws(Rest, TokensRest)
    ).

take_token([], [], []).
take_token([C|Cs], [C|Token], Rest) :-
    C > 32, !,
    take_token(Cs, Token, Rest).
take_token(Rest, [], Rest).

sieve_array(N, Array) :-
    functor(Array, b, N),
    init_args(1, N, Array),
    ( N >= 1 -> setarg(1, Array, false) ; true ),
    sieve_i(2, N, Array).

init_args(I, N, _) :- I > N, !.
init_args(I, N, Array) :-
    setarg(I, Array, true),
    I1 is I + 1,
    init_args(I1, N, Array).

sieve_i(I, N, _) :- I * I > N, !.
sieve_i(I, N, Array) :-
    arg(I, Array, IsTrue),
    ( IsTrue == true ->
        mark_multiples(I, N, Array)
    ; true
    ),
    I1 is I + 1,
    sieve_i(I1, N, Array).

mark_multiples(I, N, Array) :-
    J is I * I,
    mark_step(J, N, I, Array).

mark_step(J, N, _, _) :- J > N, !.
mark_step(J, N, I, Array) :-
    setarg(J, Array, false),
    J1 is J + I,
    mark_step(J1, N, I, Array).

output_primes(M, N, Array) :-
    output_loop(M, N, Array).

output_loop(I, N, _) :- I > N, !.
output_loop(I, N, Array) :-
    ( arg(I, Array, true) ->
        write(I), nl
    ; true
    ),
    I1 is I + 1,
    output_loop(I1, N, Array).