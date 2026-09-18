:- use_module(library(assoc)).

frequencies(S, F) :-
    string_to_list(S, L),
    frequencies(L, F).

frequencies([], []).
frequencies([H|T], F) :-
    (   get_assoc(H, F, C)
    ->  put_assoc(H, F, C+1, F1)
    ;   put_assoc(H, F, 1, F1)
    ),
    frequencies(T, F1).

main :-
    read_string(user_input, _, S),
    read_string(user_input, _, T),
    string_to_list(S, L1),
    string_to_list(T, L2),
    frequencies(L1, F1),
    frequencies(L2, F2),
    (   F1 = F2
    ->  write(1), nl
    ;   write(0), nl
    ).