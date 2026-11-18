main :-
    read_line_to_string(user_input, NLine),
    split_string(NLine, " \t", " \t", [NStr]),
    number_string(N, NStr),
    read_line_to_string(user_input, ValsLine),
    split_string(ValsLine, " \t", " \t", Parts),
    maplist(number_string, Numbers, Parts),
    Numbers = [First|Rest],
    max_subarray(Rest, First, First, Result),
    writeln(Result).

max_subarray([], _, Best, Best).
max_subarray([X|Xs], Cur0, Best0, Best) :-
    Cur1 is max(X, Cur0 + X),
    Best1 is max(Best0, Cur1),
    max_subarray(Xs, Cur1, Best1, Best).