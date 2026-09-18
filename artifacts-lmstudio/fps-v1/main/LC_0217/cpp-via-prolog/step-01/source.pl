:- use_module(library(apply)).
:- use_module(library(lists)).

main :-
    read_line_to_string(_, Input),
    string_to_list(Input, Chars),
    split_string(Chars, " ", "", Parts),
    maplist(atom_number, Parts, Numbers),
    length(Numbers, N),
    contains_duplicate(N, Numbers, Result),
    write(Result), nl.

contains_duplicate(_, [], false).
contains_duplicate(N, [H|T], Result) :-
    member(H, T), !,
    Result = true.
contains_duplicate(N, [_|T], Result) :-
    contains_duplicate(N, T, Result).