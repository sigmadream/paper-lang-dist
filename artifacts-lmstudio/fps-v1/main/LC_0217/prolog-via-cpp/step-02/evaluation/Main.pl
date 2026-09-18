:- use_module(library(lists)).

has_duplicate([H|T], Seen) :-
    member(H, Seen), !.
has_duplicate([H|T], Seen) :-
    has_duplicate(T, [H|Seen]).

main :-
    read_line_to_string(_, Input),
    string_to_list(Input, NumbersStrList),
    maplist(string_to_number, NumbersStrList, Numbers),
    nth0(1, Numbers, N),
    nth0(2, Numbers, NumList),
    has_duplicate(NumList, []),
    write(1), nl.