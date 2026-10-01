-module(solution).
-export([main/1]).

read_all() ->
    case io:get_chars("", 65536) of
        eof -> [];
        {error, _} -> [];
        Data -> Data ++ read_all()
    end.

kadane([], _Cur, Best) -> Best;
kadane([X | Rest], Cur, Best) ->
    NewCur = max(X, Cur + X),
    NewBest = max(Best, NewCur),
    kadane(Rest, NewCur, NewBest).

main(_) ->
    Content = read_all(),
    case string:tokens(Content, " \t\r\n") of
        [] -> ok;
        [_NStr, FirstStr | RestStrs] ->
            First = list_to_integer(FirstStr),
            Rest = [list_to_integer(S) || S <- RestStrs],
            Best = kadane(Rest, First, First),
            io:format("~p~n", [Best])
    end.
