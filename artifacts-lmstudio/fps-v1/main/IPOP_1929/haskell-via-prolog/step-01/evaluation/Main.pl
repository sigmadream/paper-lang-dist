prime(N) :-
    N >= 2,
    trial(2).

trial(D, N) :-
    D * D > N.
trial(D, N) :-
    N mod D == 0,
    !, fail.
trial(D, N) :-
    D1 is D + 1,
    trial(D1, N).

main :-
    read_line(Input),
    split_string(Input, " ", "", [MStr, NStr]),
    M = MStr,
    N = NStr,
    between(M, N, X),
    prime(X),
    write(X), nl.

read_line(Line) :-
    get_code(Char),
    read_line(Char, Line).

read_line(-1, []) :- !.
read_line(10, []) :- !.
read_line(Char, [Char|Line]) :-
    get_code(NewChar),
    read_line(NewChar, Line).

split_string([], _, _, []).
split_string([H|T], Delimiter, CurrentWord, Result) :-
    H == Delimiter,
    !,
    split_string(T, Delimiter, [], [CurrentWord|Result]).
split_string([H|T], Delimiter, CurrentWord, Result) :-
    append(CurrentWord, [H], NewWord),
    split_string(T, Delimiter, NewWord, Result).