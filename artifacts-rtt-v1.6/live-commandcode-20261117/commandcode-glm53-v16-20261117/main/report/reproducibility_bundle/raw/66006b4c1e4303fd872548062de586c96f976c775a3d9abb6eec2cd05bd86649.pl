:- module(main, [main/0]).
:- set_prolog_flag(double_quotes, atom).

read_num(N) :-
    read_line_to_codes(user_input, L),
    L \== end_of_file,
    phrase(number_codes(N), L).

number_codes(N) -->
    { D = "0123456789" },
    digits(Ds),
    { name(N, Ds) }.

digits([D|Ds]) --> [D], { member(D, "0123456789") }, digits(Ds).
digits([]) --> [].

gcd(A, 0, A) :- !.
gcd(A, B, G) :- C is A mod B, gcd(B, C, G).

main :-
    read_num(A),
    read_num(B),
    gcd(A, B, G),
    L is A // G * B,
    format("~d~n~d~n", [G, L]),
    halt.