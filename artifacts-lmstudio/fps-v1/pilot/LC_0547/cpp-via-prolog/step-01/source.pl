:- use_module(library(lists)).

read_values(N, A) :-
    length(A, N),
    maplist(read_line, A).

read_line(L) :-
    read_line_to_codes(user_input, Codes),
    atom_codes(Line, Codes),
    split_string(Line, ' ', '', L).

print_values(A) :-
    maplist(print_value, A),
    nl.

print_value(X) :-
    write(X),
    write(' ').

main :-
    read_line([N|_]),
    length(G, N),
    maplist(read_values(N), G),
    findall(I, (between(0, N-1, I), \+ memberchk(I, Seen)), Seen),
    length(Seen, Components),
    print_value(Components).

findall(X, P, L) :-
    findall(X, P, L, []).

findall(_, [], _, Acc) :-
    !,
    reverse(Acc, L).
findall(X, (P, Q), L, Acc) :-
    call(P, X),
    !,
    findall(Q, X, L, [X|Acc]).