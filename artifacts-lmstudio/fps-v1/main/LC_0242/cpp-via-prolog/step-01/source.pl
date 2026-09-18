:- use_module(library(io)).
:- use_module(library(lists)).

main :-
    read_string(user_input, S),
    read_string(user_input, T),
    string_to_list(S, SList),
    string_to_list(T, TList),
    sort(SList, SortedS),
    sort(TList, SortedT),
    (SortedS = SortedT -> write(1); write(0)),
    nl.

string_to_list(String, List) :-
    atom_codes(String, Codes),
    maplist(char_code, Codes, List).