:- use_module(library(lists)).

main :-
    read_line_to_string(current_input, NLine),
    atom_string(NAtom, NLine),
    atom_number(NAtom, N),
    read_rows(N, Grid),
    solve(Grid, Result),
    write_chars(Result),
    nl.

read_rows(0, []) :- !.
read_rows(N, [Chars|Rest]) :-
    N > 0,
    read_line_to_string(current_input, Line),
    string_chars(Line, Chars),
    N1 is N - 1,
    read_rows(N1, Rest).

write_chars([]).
write_chars([C|T]) :-
    put_char(C),
    write_chars(T).

solve(Matrix, [C]) :-
    Matrix = [[C|_]|_],
    all_same(Matrix, C),
    !.
solve(Matrix, Result) :-
    length(Matrix, Size),
    Half is Size // 2,
    split_n(Half, Matrix, Top, Bottom),
    maplist(split_n(Half), Top, TopL, TopR),
    maplist(split_n(Half), Bottom, BotL, BotR),
    solve(TopL, A),
    solve(TopR, B),
    solve(BotL, C),
    solve(BotR, D),
    append(A, B, AB),
    append(AB, C, ABC),
    append(ABC, D, ABCD),
    append(ABCD, [')'], Tail),
    Result = ['('|Tail].

split_n(0, List, [], List) :- !.
split_n(N, [H|T], [H|L], R) :-
    N > 0,
    N1 is N - 1,
    split_n(N1, T, L, R).

all_same([], _).
all_same([Row|Rows], C) :-
    all_chars(Row, C),
    all_same(Rows, C).

all_chars([], _).
all_chars([C|T], C) :-
    all_chars(T, C).