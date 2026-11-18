:- module(main, [main/0]).
:- use_module(library(apply)).

main :-
    read_line_to_codes(user_input, Cs),
    ( Cs == end_of_file -> true
    ; phrase(number(N), Cs),
      N >= 1, N < 15,
      count_nqueens(N, Ans),
      format("~d~n", [Ans])
    ).

number(N) -->
    blanks, digits(Ds), { number_codes(N, Ds) }, blanks.

digits([D|Ds]) --> digit(D), digits(Ds).
digits([D]) --> digit(D).

digit(D) --> [C], { C >= 0'0, C =< 0'9, number_codes(D, [C]) }.

blanks --> [C], { C =< 32 }, blanks.
blanks --> [].

count_nqueens(N, Ans) :-
    M is 2*N - 1,
    length(Cols, N), maplist(=(false), Cols),
    length(D1, M), maplist(=(false), D1),
    length(D2, M), maplist(=(false), D2),
    State = state(Cols, D1, D2, 0),
    solve(0, N, State, State, Ans).

solve(R, N, _, _, Ans) :- R =:= N, !, Ans = 1.
solve(R, N, S0, S, Ans) :-
    R < N,
    findall(1, place(R, N, S0, S), Ls),
    sum_list(Ls, Ans).

place(R, N, state(Cols, D1, D2, _), state(Cols2, D1b, D2b, _)) :-
    between(0, N1, C), N1 is N - 1,
    nth0(C, Cols, false),
    I1 is R + C,
    nth0(I1, D1, false),
    I2 is R - C + N - 1,
    nth0(I2, D2, false),
    set_nth(C, Cols, true, Cols2),
    set_nth(I1, D1, true, D1b),
    set_nth(I2, D2, true, D2b).

set_nth(0, [_|T], V, [V|T]) :- !.
set_nth(I, [H|T], V, [H|T2]) :- I1 is I - 1, set_nth(I1, T, V, T2).

sum_list([], 0).
sum_list([H|T], S) :- sum_list(T, S1), S is H + S1.