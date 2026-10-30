-module(solution).
-export([main/1]).

read_all() ->
    case io:get_chars("", 65536) of
        eof -> [];
        {error, _} -> [];
        Data -> Data ++ read_all()
    end.

is_valid(Chars) ->
    check(Chars, 0).

check([], 0) -> true;
check([], _Bal) -> false;
check([$( | Rest], Bal) ->
    check(Rest, Bal + 1);
check([$) | Rest], Bal) when Bal > 0 ->
    check(Rest, Bal - 1);
check([$) | _Rest], _Bal) ->
    false;
check([_ | Rest], Bal) ->
    check(Rest, Bal).

process([]) -> ok;
process([S | Rest]) ->
    case is_valid(S) of
        true -> io:format("YES~n");
        false -> io:format("NO~n")
    end,
    process(Rest).

main(_) ->
    Content = read_all(),
    case string:tokens(Content, " \t\r\n") of
        [] -> ok;
        [_TStr | Strings] ->
            process(Strings)
    end.
