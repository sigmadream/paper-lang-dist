:- use_module(library(readutil)).

main :-
    read_all_lines(Lines),
    tokenize_lines(Lines, Nums),
    ( Nums = [_N, _M | Rest] ->
        parse_edges(Rest, Edges),
        count_answer(Edges, Ans)
    ; Ans = 0
    ),
    writeln(Ans).

read_all_lines(Lines) :-
    read_line_to_string(user_input, Line),
    ( Line == end_of_file ->
        Lines = []
    ; Lines = [Line | Rest],
      read_all_lines(Rest)
    ).

tokenize_lines([], []).
tokenize_lines([Line | Lines], Nums) :-
    split_string(Line, " \t\r\n", " \t\r\n", Tokens0),
    include(nonempty_string, Tokens0, Tokens),
    maplist(token_to_number, Tokens, LineNums),
    append(LineNums, RestNums, Nums),
    tokenize_lines(Lines, RestNums).

nonempty_string(S) :-
    S \= "".

token_to_number(S, N) :-
    number_string(N, S).

parse_edges([], []).
parse_edges([A, B | Rest], [e(A, B) | Edges]) :-
    parse_edges(Rest, Edges).

count_answer(Edges, Ans) :-
    neighbors(1, Edges, D1),
    findall(X,
        ( member(Y, D1),
          neighbors(Y, Edges, Ns),
          member(X, Ns)
        ),
        D2
    ),
    append(D1, D2, Candidates0),
    delete(Candidates0, 1, Candidates1),
    sort(Candidates1, Unique),
    length(Unique, Ans).

neighbors(Node, Edges, Ns) :-
    findall(Other,
        ( member(e(A, B), Edges),
          ( A == Node, Other = B
          ; B == Node, Other = A
          )
        ),
        Ns
    ).