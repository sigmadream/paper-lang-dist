:- module(main, [main/0]).
:- use_module(library(readutil)).

check(0) :- !.
check(B) :- B > 0, fail.

balance(0, yes) :- !.
balance(_, no).

solve(S, Ans) :-
    (   foldl([C, Acc, NA]>>(
                (   Acc = ok(B), B1 is B + (C == '(' ? 1 : -1)
                ;   Acc = neg, B1 = -1
                ),
                (   B1 < 0 -> NA = neg
                ;   NA = ok(B1)
                )),
                S, ok(0), Final),
        Final = ok(0)
    ->  Ans = "YES"
    ;   Ans = "NO"
    ).

main :-
    read_line_to_string(user_input, TLine),
    (   TLine == end_of_file -> true
    ;   number_string(T, TLine),
        loop(T)
    ).

loop(0) :- !.
loop(N) :-
    read_line_to_string(user_input, Line),
    (   Line == end_of_file -> true
    ;   string_chars(Line, Chars0),
        exclude([C]>>(C == '\n'), Chars0, Chars),
        exclude([C]>>(C == ' '), Chars, S),
        solve(S, Ans),
        writeln(Ans),
        N1 is N - 1,
        loop(N1)
    ).