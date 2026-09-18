:- use_module(library(lists)).

visit(Graph, [], Seen) :- !.
visit(Graph, [V|Todo], Seen) :-
    memberchk(V, Seen), !,
    visit(Graph, Todo, Seen).
visit(Graph, [V|Todo], Seen) :-
    NewSeen = [V | Seen],
    Adjacent = Graph.V,
    append(Adjacent, Todo, NewTodo),
    visit(Graph, NewTodo, NewSeen).

components(Graph, [], Seen, Count) :- !, Count is 0.
components(Graph, [V|Vs], Seen, Count) :-
    memberchk(V, Seen), !,
    components(Graph, Vs, Seen, Count).
components(Graph, [V|Vs], Seen, Count) :-
    NewSeen = [V | Seen],
    Adjacent = Graph.V,
    append(Adjacent, [V], NewTodo),
    visit(Graph, NewTodo, NewSeen),
    NextCount is Count + 1,
    components(Graph, Vs, NewSeen, NextCount).

main :-
    read_line_to_string(Input),
    split_string(Input, "\n", "", Lines),
    length(Lines, N),
    maplist(read_list, Lines, Matrix),
    build_graph(N, Matrix, Graph),
    findall(V, between(0, N-1, V), Vertices),
    components(Graph, Vertices, [], Count),
    write(Count).

read_list(Line, List) :-
    split_string(Line, " ", "", Tokens),
    maplist(atom_number, Tokens, List).

build_graph(N, Matrix, Graph) :-
    build_graph(N, Matrix, 0, Graph).

build_graph(_, _, N, _) :- N >= 200, !.
build_graph(N, Matrix, I, Graph) :-
    nth1(I+1, Matrix, Row),
    build_row(Row, I, Graph, NewGraph),
    I1 is I + 1,
    build_graph(N, Matrix, I1, NewGraph).

build_row([], _, Graph, Graph).
build_row([0|Row], I, Graph, NewGraph) :-
    build_row(Row, I+1, Graph, NewGraph).
build_row([1|Row], I, Graph, NewGraph) :-
    update_graph(Graph, I, I, NewGraph),
    build_row(Row, I+1, NewGraph, NewGraph).

update_graph(Graph, I, J, NewGraph) :-
    put_dict(I-J, Graph, 1, NewGraph).