-module(solution).
-export([main/1]).

read_all() ->
    case io:get_chars("", 65536) of
        eof -> [];
        {error, _} -> [];
        Data -> Data ++ read_all()
    end.

main(_) ->
    Content = read_all(),
    case string:tokens(Content, " \t\r\n") of
        [] -> ok;
        [_NStr | NumStrs] ->
            Nums = [list_to_integer(S) || S <- NumStrs],
            NonZeros = [X || X <- Nums, X =/= 0],
            Zeros = [X || X <- Nums, X =:= 0],
            Result = NonZeros ++ Zeros,
            Out = lists:join(" ", [integer_to_list(X) || X <- Result]),
            io:put_chars([Out, "\n"])
    end.
