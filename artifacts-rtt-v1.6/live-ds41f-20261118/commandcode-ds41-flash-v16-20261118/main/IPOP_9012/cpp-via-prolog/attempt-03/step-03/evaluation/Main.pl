read_line_codes(Codes) :-
    get_code(user_input, C),
    (   C =:= -1 -> Codes = end_of_file
    ;   C =:= 10 -> Codes = []
    ;   read_line_rest(C, Codes)
    ).

read_line_rest(First, [First|Rest]) :-
    get_code(user_input, C),
    (   C =:= -1 -> Rest = []
    ;   C =:= 10 -> Rest = []
    ;   read_line_rest(C, Rest)
    ).

main :-
    read_line_codes(FirstLine),
    (   FirstLine == end_of_file -> true
    ;   trim_ws(FirstLine, TLine),
        number_codes(T, TLine),
        process(T)
    ).

process(0) :- !.
process(N) :-
    read_line_codes(Line),
    (   Line == end_of_file -> true
    ;   check_line(Line, Res),
        write(Res), nl,
        N1 is N - 1,
        process(N1)
    ).

check_line(Codes, Res) :-
    trim_ws(Codes, Trimmed),
    (   Trimmed == [] -> Res = 'NO'
    ;   check(Trimmed, 0, Res)
    ).

check([], Bal, Res) :-
    (   Bal =:= 0 -> Res = 'YES' ; Res = 'NO' ).
check([C|Rest], Bal, Res) :-
    (   C =:= 40 ->
        B1 is Bal + 1,
        check(Rest, B1, Res)
    ;   C =:= 41 ->
        (   Bal > 0 ->
            B1 is Bal - 1,
            check(Rest, B1, Res)
        ;   Res = 'NO'
        )
    ;   Res = 'NO'
    ).

trim_ws(Codes, Trimmed) :-
    trim_left(Codes, L),
    reverse(L, RevL),
    trim_left(RevL, RevTrim),
    reverse(RevTrim, Trimmed).

trim_left([C|Rest], Out) :-
    is_ws(C), !,
    trim_left(Rest, Out).
trim_left(L, L).

is_ws(C) :- C =:= 32 ; C =:= 9 ; C =:= 10 ; C =:= 11 ; C =:= 12 ; C =:= 13.