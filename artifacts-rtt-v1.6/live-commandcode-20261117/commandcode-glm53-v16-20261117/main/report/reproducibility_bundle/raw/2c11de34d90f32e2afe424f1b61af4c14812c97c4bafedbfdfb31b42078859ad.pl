:- module(main, []).
:- use_module(library(clpfd)).

main :-
    read_line_to_codes(user_input, L),
    parse_nums(L, [M, N]),
    unique_paths(M, N, R),
    format("~d~n", [R]).

parse_nums(L, Ns) :-
    phrase(all_nums(Ns), L).

all_nums([N|Ns]) --> blanks, num(N), blanks, ( all_nums(Ns) ; { Ns = [] } ).
all_nums([]) --> [].

num(N) --> digits(D), { number_codes(N, D) }, !.
num(N) --> digits(D), { number_codes(N, D) }.

digits([D|Ds]) --> [D], { code_type(D, digit) }, digits(Ds).
digits([D]) --> [D], { code_type(D, digit) }.

blanks --> [C], { code_type(C, space) }, !, blanks.
blanks --> [].

unique_paths(1, _, 1) :- !.
unique_paths(_, 1, 1) :- !.
unique_paths(M, N, R) :-
    length(Row0, N),
    maplist(=(1), Row0),
    M1 is M - 1,
    iterate(M1, N, Row0, Row),
    nth1(N, Row, R).

iterate(0, _, Row, Row) :- !.
iterate(I, N, Row0, Row) :-
    I > 0,
    update_row(Row0, Row1),
    I1 is I - 1,
    iterate(I1, N, Row1, Row).

update_row(Row0, Row1) :-
    Row0 = [F|Rest],
    update_rest(F, Rest, Row1).

update_rest(_, [], []).
update_rest(Prev, [X|Xs], [Y|Ys]) :-
    Y is Prev + X,
    update_rest(Y, Xs, Ys).