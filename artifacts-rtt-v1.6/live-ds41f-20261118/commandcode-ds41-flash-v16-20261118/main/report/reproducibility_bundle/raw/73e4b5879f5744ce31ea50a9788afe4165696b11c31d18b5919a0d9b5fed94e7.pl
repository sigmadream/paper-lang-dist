:- module(main, [main/0]).

main :-
    read_ints([N|Scores]),
    solve(N, Scores, Ans),
    write(Ans), nl.

solve(N, Scores, Ans) :-
    ( N =:= 1 ->
        Scores = [A|_],
        Ans = A
    ; N =:= 2 ->
        Scores = [A,B|_],
        Ans is A + B
    ;   Scores = [A1,A2|_],
        Dp0 = 0,
        Dp1 = A1,
        Dp2 is A1 + A2,
        compute_loop(3, N, Scores, [Dp0,Dp1,Dp2], Ans)
    ).

compute_loop(I, N, Scores, Dp, Ans) :-
    ( I > N ->
        last_dp(Dp, Ans)
    ;   nth1(I, Scores, Ai),
        I1 is I - 1,
        nth1(I1, Scores, Aprev),
        Pos1 is I - 1,
        nth1(Pos1, Dp, Dp_i_minus_2),
        Pos2 is I - 2,
        nth1(Pos2, Dp, Dp_i_minus_3),
        V1 is Dp_i_minus_2 + Ai,
        V2 is Dp_i_minus_3 + Aprev + Ai,
        ( V1 >= V2 -> New = V1 ; New = V2 ),
        append(Dp, [New], DpNext),
        I2 is I + 1,
        compute_loop(I2, N, Scores, DpNext, Ans)
    ).

last_dp([X], X) :- !.
last_dp([_|T], X) :- last_dp(T, X).

read_ints(List) :-
    get_char(user_input, C),
    read_ints_from(C, List).

read_ints_from(end_of_file, []) :- !.
read_ints_from(C, List) :-
    ( char_type(C, space) ->
        get_char(user_input, C1),
        read_ints_from(C1, List)
    ; char_type(C, digit) ->
        read_number(C, Num, Next),
        List = [Num|Rest],
        read_ints_from(Next, Rest)
    ;   get_char(user_input, C1),
        read_ints_from(C1, List)
    ).

read_number(C, Num, Next) :-
    read_digits(C, Chars, Next),
    number_chars(Num, Chars).

read_digits(C, [C|Rest], Next) :-
    get_char(user_input, C1),
    ( C1 == end_of_file ->
        Rest = [],
        Next = end_of_file
    ; char_type(C1, digit) ->
        read_digits(C1, Rest, Next)
    ;   Rest = [],
        Next = C1
    ).