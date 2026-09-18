main :-
    read_line_to_string(Input),
    string_to_list(Input, InputList),
    maplist(string_to_integer, InputList, Numbers),
    nth1(2, Numbers, N),
    nth1(N+2, Numbers, Scores),
    find_max_score(Scores, 0, 0, Result),
    write(Result), nl.

find_max_score([], _, _, 0).
find_max_score([_], _, _, 0).
find_max_score([_, _], _, _, 0).
find_max_score([S1, S2, S3 | Rest], Prev1, Prev2, Result) :-
    MaxPrev2 is max(Prev1, Prev2 + S1),
    NewResult is max(MaxPrev2 + S2, Prev2 + S3 + S2),
    find_max_score(Rest, Prev2, MaxPrev2, NewResult).