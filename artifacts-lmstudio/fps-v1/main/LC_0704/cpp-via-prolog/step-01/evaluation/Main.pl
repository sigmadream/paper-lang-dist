:- use_module(library(readutil)).

binary_search(N, Target, A, Index) :-
    binary_search(0, N, Target, A, Index).

binary_search(Low, High, Target, A, Index) :-
    Low < High,
    Mid is (Low + High) // 2,
    nth1(Mid, A, Element),
    (   Element =< Target
    ->  binary_search(Mid, High, Target, A, Index)
    ;   binary_search(Low, Mid, Target, A, Index)
    ).

binary_search(_, _, _, _, -1).

main :-
    read_line_to_codes(user_input, Input),
    string_to_list(Input, Tokens),
    split_string(Tokens, ' ', '', [NStr, TargetStr | Rest]),
    number_string(N, NStr),
    number_string(Target, TargetStr),
    maplist(number_string, Rest, AList),
    list_to_array(AList, A),
    binary_search(N, Target, A, Index),
    write(Index), nl.