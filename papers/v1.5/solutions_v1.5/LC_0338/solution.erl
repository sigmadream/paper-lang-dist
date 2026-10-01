-module(solution).
-export([main/1]).

read_all() ->
    case io:get_chars("", 65536) of
        eof -> [];
        {error, _} -> [];
        Data -> Data ++ read_all()
    end.

popcount(0) -> 0;
popcount(X) -> (X band 1) + popcount(X bsr 1).

main(_) ->
    Content = read_all(),
    case string:tokens(Content, " \t\r\n") of
        [] -> ok;
        [NStr | _] ->
            N = list_to_integer(NStr),
            Counts = [integer_to_list(popcount(I)) || I <- lists:seq(0, N)],
            Out = lists:join(" ", Counts),
            io:put_chars([Out, "\n"])
    end.
