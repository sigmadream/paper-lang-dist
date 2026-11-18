:- module(main, [main/0]).

main :-
    read_string(user_input, end_of_file, S),
    split_string(S, " \t\n\r", " \t\n\r", Tokens),
    Tokens = [NTok | NumToks],
    atom_number(NTok, N),
    length(Nums, N),
    append(Nums, _, NumToks),
    maplist(atom_number, Nums, Values),
    Values = [First | Tail],
    max_subarray(Tail, First, First, Best),
    writeln(Best).

max_subarray([], _, Best, Best).
max_subarray([X | Xs], Cur, Best0, Best) :-
    Cur1 is max(X, Cur + X),
    Best1 is max(Best0, Cur1),
    max_subarray(Xs, Cur1, Best1, Best).