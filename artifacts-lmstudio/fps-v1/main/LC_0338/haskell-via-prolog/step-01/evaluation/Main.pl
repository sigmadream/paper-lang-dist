:- use_module(library(readutil)).

ones(0, 0).
ones(N, Result) :-
    N > 0,
    N1 is N // 2,
    N mod 2 =:= 1,
    ones(N1, R),
    Result is R + 1.
ones(N, Result) :-
    N > 0,
    N1 is N // 2,
    N mod 2 =:= 0,
    ones(N1, R),
    Result is R.

main :-
    read_line_to_string(CurrentLine),
    atom_number(CurrentLine, N),
    findall(Result, (between(0, N, I), ones(I, Result)), Results),
    maplist(write, Results),
    write('\n').