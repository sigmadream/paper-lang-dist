main :-
    read_line_to_string(Input),
    string_split(Input, ' ', Parts),
    maplist(string_to_integer, Parts, [N, M]),
    findall(Edge, (between(1, M, I), read_line_to_string(Line), string_split(Line, ' ', EdgeParts), maplist(string_to_integer, EdgeParts, Edge)), Edges),
    build_graph(N, Edges, Graph),
    bfs(Graph, 1, Distance),
    count_distance(Distance, 2, Count),
    write(Count).

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

add_edge(X, List) :-
    append(List, [X], NewList).

bfs(Graph, Start, Distance) :-
    length(Distance, N+1),
    maplist(init_distance, Distance),
    bfs_helper(Graph, Start, 0, Distance).

init_distance(_, -1).

bfs_helper(Graph, Node, Dist, Distance) :-
    nth0(Node, Graph, Neighbors),
    update_distances(Neighbors, Dist, Distance, NewDistance),
    findall(NewNode, (between(1, N, NewNode), nth0(NewNode, NewDistance, D), D =:= -1), NextNodes),
    (   NextNodes = [] -> true
    ;   maplist(bfs_helper(Graph, _, Dist+1), NextNodes)
    ).

update_distances(Neighbors, OldDist, Distance, NewDistance) :-
    length(Distance, N+1),
    maplist(update_distance(OldDist), Neighbors, Distance, NewDistance).

update_distance(_, Node, Distance, NewDistance) :-
    nth0(Node, Distance, D),
    (   D =:= -1 -> nth0(Node, NewDistance, OldDist + 1)
    ;   true
    ).

count_distance(Distance, MaxDist, Count) :-
    length(Distance, N+1),
    findall(Node, (between(2, N, Node), nth0(Node, Distance, D), D =:= MaxDist), Nodes),
    length(Nodes, Count).