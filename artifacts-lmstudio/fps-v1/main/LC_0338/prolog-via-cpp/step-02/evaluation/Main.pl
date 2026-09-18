:- use_module(library(readutil)).

count_ones(N, Count) :-
    N =< 0 -> Count = 0;
    N mod 2 =:= 1 -> count_ones(N // 2, Temp), Count is Temp + 1;
    N mod 2 =:= 0 -> count_ones(N // 2, Count).

main :-
    read_line_to_string(_, Input),
    string_to_integer(Input, N),
    findall(Count, (between(0, N, I), count_ones(I, Count)), Counts),
    maplist(write, Counts),
    nl.