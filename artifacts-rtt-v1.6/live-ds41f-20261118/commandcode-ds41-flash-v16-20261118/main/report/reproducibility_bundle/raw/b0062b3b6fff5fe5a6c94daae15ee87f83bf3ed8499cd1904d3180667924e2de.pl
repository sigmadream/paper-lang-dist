main :-
    read_string(user_input, _, Input),
    split_string(Input, " \n\r\t", " \n\r\t", RawTokens),
    exclude(==(""), RawTokens, Tokens),
    maplist(number_string, Numbers, Tokens),
    Numbers = [N|Rest],
    length(Values, N),
    append(Values, _, Rest),
    max_subarray(Values, Best),
    format("~w~n", [Best]).

max_subarray([First|Rest], Best) :-
    kadane(Rest, First, First, Best).

kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best0, Best) :-
    Cur1 is max(X, Cur + X),
    Best1 is max(Best0, Cur1),
    kadane(Xs, Cur1, Best1, Best).