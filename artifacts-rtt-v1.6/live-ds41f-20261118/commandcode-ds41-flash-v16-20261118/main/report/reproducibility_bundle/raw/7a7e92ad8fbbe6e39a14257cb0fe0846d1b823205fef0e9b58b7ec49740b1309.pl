read_all_tokens(Tokens) :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file
    ->  Tokens = []
    ;   split_string(Line, " \t\r\n", " \t\r\n", RawParts),
        remove_empty(RawParts, Parts),
        maplist(number_string, Nums, Parts),
        read_all_tokens(Rest),
        append(Nums, Rest, Tokens)
    ).

remove_empty([], []).
remove_empty([S|Ss], Out) :-
    (   S == ""
    ->  remove_empty(Ss, Out)
    ;   Out = [S|Rest],
        remove_empty(Ss, Rest)
    ).

my_max(A, B, A) :- A >= B, !.
my_max(_, B, B).

kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best, Result) :-
    Sum is Cur + X,
    my_max(X, Sum, Cur1),
    my_max(Best, Cur1, Best1),
    kadane(Xs, Cur1, Best1, Result).

main :-
    read_all_tokens(Tokens),
    Tokens = [N|Rest],
    length(Values, N),
    append(Values, _, Rest),
    Values = [First|Tail],
    kadane(Tail, First, First, Best),
    writeln(Best).