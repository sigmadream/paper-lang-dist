:- module(main, [main/0]).

main :-
    read_string(user_input, _, Input),
    split_string(Input, "\n", "\r", Lines),
    Lines = [FirstLine | RestLines],
    number_string(T, FirstLine),
    process_cases(T, RestLines).

process_cases(0, _) :- !.
process_cases(N, [Line | Rest]) :-
    N > 0,
    string_chars(Line, Chars),
    check_chars(Chars, 0, 0, FinalBalance, MinBalance),
    (   FinalBalance =:= 0,
        MinBalance >= 0
    ->  writeln('YES')
    ;   writeln('NO')
    ),
    N1 is N - 1,
    process_cases(N1, Rest).
process_cases(_, []) :- !.

check_chars([], Bal, Min, Bal, Min).
check_chars([C | Cs], Bal0, Min0, Bal, Min) :-
    (   C = '('
    ->  Bal1 is Bal0 + 1,
        Min1 is Min0
    ;   C = ')'
    ->  Bal1 is Bal0 - 1,
        Min1 is min(Min0, Bal1)
    ;   % ignore other characters
        Bal1 = Bal0,
        Min1 = Min0
    ),
    check_chars(Cs, Bal1, Min1, Bal, Min).