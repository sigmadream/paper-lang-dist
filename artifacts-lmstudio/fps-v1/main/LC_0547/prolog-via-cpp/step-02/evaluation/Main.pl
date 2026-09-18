:- use_module(library(lists)).

visit(_, [], _).
visit(Rows, [H|T], Seen) :-
    \+ member(H, Seen),
    mark_visited(Rows, H, Seen, NewSeen),
    visit(Rows, T, NewSeen).

mark_visited([], _, Seen, Seen).
mark_visited([Row|Rows], V, Seen, NewSeen) :-
    (   Row[V] = 1
    ->  \+ member(V, Seen),
        append(Seen, [V], NewSeen)
    ;   true
    ),
    mark_visited(Rows, V, Seen, NewSeen).

components(Rows, N, Count) :-
    length(Rows, N),
    init_seen(N, Seen),
    count_components(Rows, N, 0, Seen, Count).

init_seen(N, Seen) :-
    length(Seen, N),
    maplist(=(false), Seen).

count_components(_, 0, Count, _, Count).
count_components(Rows, N, Acc, Seen, Count) :-
    \+ member(false, Seen),
    count_components(Rows, N, Acc + 1, Seen, Count).
count_components(Rows, N, Acc, Seen, Count) :-
    find_false(Seen, V),
    visit(Rows, [V], Seen, NewSeen),
    count_components(Rows, N, Acc, NewSeen, Count).

find_false([false|_], 0).
find_false([_|T], I) :-
    find_false(T, J),
    I is J + 1.

main :-
    read_line_to_string(_, Input),
    string_to_list(Input, Numbers),
    split_string(Numbers, "\n", "", Lines),
    length(Lines, N),
    maplist(string_to_list, Lines, Rows),
    components(Rows, N, Count),
    write(Count), nl.