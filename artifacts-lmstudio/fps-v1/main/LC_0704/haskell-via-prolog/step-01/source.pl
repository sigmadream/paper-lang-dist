:- use_module(library(readutil)).

binary_search(N, Target, List, Index) :-
    binary_search(List, Target, 0, N-1, Index).

binary_search(_, _, Lo, Hi, Index) :-
    Lo > Hi,
    Index = -1.
binary_search(List, Target, Lo, Hi, Index) :-
    Mid is (Lo + Hi) // 2,
    nth0(Mid, List, Element),
    (   Element =:= Target
    ->  Index = Mid
    ;   Element < Target
    ->  binary_search(List, Target, Mid+1, Hi, Index)
    ;   binary_search(List, Target, Lo, Mid-1, Index)
    ).

main :-
    read_line_to_codes(user_input, Input),
    string_to_list(Input, Tokens),
    tokens_to_integers(Tokens, [N, Target | List]),
    binary_search(N, Target, List, Index),
    write(Index), nl.

tokens_to_integers([], []).
tokens_to_integers([H|T], [I|Is]) :-
    number_string(I, H),
    tokens_to_integers(T, Is).