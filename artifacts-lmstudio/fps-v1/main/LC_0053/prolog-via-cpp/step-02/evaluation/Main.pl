:- use_module(library(readutil)).

main :-
    read_line_to_string(STDIN),
    string_to_list(STDIN, Input),
    split_string(Input, "\n", "", [N|Nums]),
    maplist(string_to_number, Nums, NumList),
    kadane(NumList, Result),
    write(Result),
    nl.

kadane([], 0).
kadane([H|T], Result) :-
    kadane(T, Temp),
    Current is max(H, H + Temp),
    Global is max(Current, Temp),
    Result is Global.