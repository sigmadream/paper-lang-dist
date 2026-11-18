main :-
    read_string(current_input, end_of_file, Input),
    split_string(Input, " \n\t\r", " \n\t\r", Tokens),
    Tokens = [NToken|ValueTokensAll],
    number_string(N, NToken),
    length(ValueTokens, N),
    append(ValueTokens, _, ValueTokensAll),
    maplist(number_string, Values, ValueTokens),
    Values = [First|Rest],
    kadane(Rest, First, First, Best),
    writeln(Best).

kadane([], _, Best, Best).
kadane([X|Xs], Cur, Best, Final) :-
    CurPlus is Cur + X,
    (   X > CurPlus
    ->  Cur1 = X
    ;   Cur1 = CurPlus
    ),
    (   Cur1 > Best
    ->  Best1 = Cur1
    ;   Best1 = Best
    ),
    kadane(Xs, Cur1, Best1, Final).