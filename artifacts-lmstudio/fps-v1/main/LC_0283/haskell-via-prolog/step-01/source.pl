:- use_module(library(readutil)).

main :-
    read_line_to_string(In),
    string_split(In, ' ', Parts),
    maplist(string_to_integer, Parts, Numbers),
    length(Numbers, N),
    take(N, Numbers, Xs),
    filter(nonzero, Xs, NonZero),
    length(NonZero, Len),
    Zeros is N - Len,
    append(NonZero, Zeros times 0, Answer),
    maplist(integer_to_string, Answer, Strings),
    write(Strings),
    nl.

nonzero(X) :-
    X \= 0.

take(_, [], []).
take(N, [H|T], [H|R]) :-
    N > 0,
    M is N - 1,
    take(M, T, R).

filter(_, [], []).
filter(Pred, [H|T], [H|R]) :-
    Pred(H),
    filter(Pred, T, R).
filter(Pred, [_|T], R) :-
    \+ Pred(_),
    filter(Pred, T, R).

Zeros times 0 is Zeros.