:- module(main, [main/0]).

main :-
    read_line_to_codes(user_input, Line1),
    Line1 \== end_of_file,
    phrase(number(T), Line1, _),
    T > 0,
    loop(T).
main.

loop(0) :- !.
loop(N) :-
    read_line_to_codes(user_input, L),
    ( L == end_of_file -> true
    ; check(L, R),
      format("~s~n", [R]),
      N1 is N - 1,
      loop(N1)
    ).

check(Codes, "YES") :-
    balance(Codes, 0), !.
check(_, "NO").

balance([], 0).
balance([0'(|Rest], B) :- !, B1 is B + 1, balance(Rest, B1).
balance([0')|Rest], B) :- B > 0, B1 is B - 1, balance(Rest, B1).
balance([_|Rest], B) :- balance(Rest, B).

number(N) --> digits(D), { number_codes(N, D) }.

digits([D|Ds]) --> digit(D), digits(Ds).
digits([D]) --> digit(D).

digit(D) --> [D], { between(0'0, 0'9, D) }.