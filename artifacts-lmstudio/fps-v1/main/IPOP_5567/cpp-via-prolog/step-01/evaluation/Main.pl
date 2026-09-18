:- use_module(library(readutil)).
:- use_module(library(lists)).

main :-
    read_line_to_string(_, Input),
    string_split(Input, ' ', Numbers),
    maplist(string_to_integer, Numbers, [N, M|_]),
    findall([A, B], (between(1, M, I), read_line_to_string(_, Line), string_split(Line, ' ', [A0, B0]), A is min(A0, B0), B is max(A0, B0)), Edges),
    build_graph(N, Edges, Graph),
    bfs(Graph, 1, Distances),
    count_nodes(Distances, 2, Count),
    write(Count), nl.

build_graph(N, Edges, Graph) :-
    length(Graph, N+1),
    maplist(init_list, Graph),
    maplist(add_edges(Edges), Graph).

init_list([], []).

add_edges(Edges, List) :-
    member([A, B], Edges),
    (   A =:= List -> add_edge(B, List)
    ;   B =:= List -> add_edge(A, List)
    ).

add_edge(Node, List) :-
    append(List, [Node], NewList).

bfs(Graph, Start, Distances) :-
    length(Distances, N+1),
    maplist(init_dist, Distances),
    bfs_helper(Graph, Start, 0, Distances).

init_dist(_, -1).

bfs_helper(Graph, Node, Dist, Distances) :-
    nth0(Node, Graph, Neighbors),
    maplist(update_dist(Neighbors, Dist), Distances),
    findall(NewNode, (between(1, N, NewNode), nth0(NewNode, Distances, D), D =:= -1), NextNodes),
    maplist(bfs_helper(Graph, _, Dist+1), NextNodes).

update_dist(Neighbors, OldDist, [_, NewDist|_]) :-
    member(Node, Neighbors),
    nth0(Node, Distances, CurrentDist),
    (   CurrentDist =:= -1 -> nth0(Node, Distances, OldDist + 1)
    ;   CurrentDist > OldDist + 1 -> nth0(Node, Distances, OldDist + 1)
    ).

count_nodes(Distances, MaxDist, Count) :-
    findall(Node, (between(2, N, Node), nth0(Node, Distances, D), D =< MaxDist), Nodes),
    length(Nodes, Count).