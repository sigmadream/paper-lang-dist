:- use_module(library(lists)).

visit(Rows, V, Seen) :-
    nth1(V, Seen, SeenV),
    SeenV = true,
    !.
visit(Rows, V, Seen) :-
    nth1(V, Seen, false),
    nth1(V, Rows, Row),
    maplist((J, RowJ) -> (RowJ = 1, J \= V -> visit(Rows, J, Seen), fail ; true), Row).

components(Rows, Count) :-
    length(Rows, N),
    init_list(N, false, Seen),
    count_components(Rows, Seen, 0, Count).

count_components(_, [], Count, Count).
count_components(Rows, Seen, Acc, Count) :-
    nth1(I, Seen, false),
    visit(Rows, I, Seen),
    NewAcc is Acc + 1,
    count_components(Rows, Seen, NewAcc, Count).

init_list(0, _, []).
init_list(N, Value, [Value | Rest]) :-
    N > 0,
    M is N - 1,
    init_list(M, Value, Rest).

main :-
    read_line_to_string(_, Input),
    string_to_list(Input, Numbers),
    split_string(Numbers, "\n", "", Lines),
    length(Lines, N),
    maplist(string_to_list, Lines, Rows),
    components(Rows, Count),
    write(Count), nl.