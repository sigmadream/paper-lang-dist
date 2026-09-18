:- use_module(library(lists)).

main :-
    read_line_to_string(_, Input),
    string_split(Input, ' ', Parts),
    maplist(string_to_integer, Parts, [N, M | Edges]),
    findall((A, B), (nth0(I, Edges, A), nth0(J, Edges, B), I < J), EdgeList),
    direct_friends(EdgeList, 1, Direct),
    two_friends(EdgeList, Direct, Two),
    subtract(Two, [1], Result),
    length(Result, Output),
    write(Output).

direct_friends([], _, []).
direct_friends([(A, B) | Rest], 1, [B | Direct]) :-
    direct_friends(Rest, 1, Direct).
direct_friends([(_, A) | Rest], A, [B | Direct]) :-
    direct_friends(Rest, A, Direct).
direct_friends([_ | Rest], _, Direct) :-
    direct_friends(Rest, _, Direct).

two_friends([], _, []).
two_friends([(A, B) | Rest], Direct, [C | Two]) :-
    member(A, Direct), \+ member(B, Direct), !,
    two_friends(Rest, Direct, Two).
two_friends([(A, B) | Rest], Direct, [C | Two]) :-
    member(B, Direct), \+ member(A, Direct), !,
    two_friends(Rest, Direct, Two).
two_friends([_ | Rest], Direct, Two) :-
    two_friends(Rest, Direct, Two).