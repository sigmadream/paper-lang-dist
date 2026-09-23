-module(solution).
-export([main/1]).

read_all() ->
    case io:get_chars("", 65536) of
        eof -> [];
        {error, _} -> [];
        Data -> Data ++ read_all()
    end.

build_adj([], _I, _J, _N, Adj) -> Adj;
build_adj([Val | Rest], I, J, N, Adj) ->
    NextJ = (J + 1) rem N,
    NextI = if NextJ == 0 -> I + 1; true -> I end,
    NewAdj = case Val of
        1 ->
            maps:update_with(I, fun(Neighs) -> [J | Neighs] end, [J], Adj);
        0 ->
            maps:update_with(I, fun(Neighs) -> Neighs end, [], Adj)
    end,
    build_adj(Rest, NextI, NextJ, N, NewAdj).

dfs([], _Adj, Seen) -> Seen;
dfs([U | Stack], Adj, Seen) ->
    Neighbors = maps:get(U, Adj, []),
    Unvisited = [V || V <- Neighbors, not sets:is_element(V, Seen)],
    NewSeen = lists:foldl(fun(V, S) -> sets:add_element(V, S) end, Seen, Unvisited),
    dfs(Unvisited ++ Stack, Adj, NewSeen).

count_provinces(I, N, _Adj, _Seen, Count) when I >= N -> Count;
count_provinces(I, N, Adj, Seen, Count) ->
    case sets:is_element(I, Seen) of
        true ->
            count_provinces(I + 1, N, Adj, Seen, Count);
        false ->
            NewSeen = dfs([I], Adj, sets:add_element(I, Seen)),
            count_provinces(I + 1, N, Adj, NewSeen, Count + 1)
    end.

main(_) ->
    Content = read_all(),
    case string:tokens(Content, " \t\r\n") of
        [] -> ok;
        [NStr | MatrixStrs] ->
            N = list_to_integer(NStr),
            Ints = [list_to_integer(S) || S <- MatrixStrs],
            Adj = build_adj(Ints, 0, 0, N, #{}),
            Ans = count_provinces(0, N, Adj, sets:new(), 0),
            io:format("~p~n", [Ans])
    end.
