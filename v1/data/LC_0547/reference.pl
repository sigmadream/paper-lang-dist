:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
:- use_module(library(ordsets)).
matrix_rows([],_,[]).
matrix_rows(Xs,N,[Row|Rows]) :- length(Row,N), append(Row,Rest,Xs), matrix_rows(Rest,N,Rows).
visit([],_,Seen,Seen).
visit([V|Todo],Rows,Seen,Out) :-
    (ord_memberchk(V,Seen) -> visit(Todo,Rows,Seen,Out)
    ; nth1(V,Rows,Row), findall(J,nth1(J,Row,1),Neighbors), append(Neighbors,Todo,Next),
      ord_add_element(Seen,V,Added), visit(Next,Rows,Added,Out)).
components(I,N,_,_,0) :- I > N, !.
components(I,N,Rows,Seen,Count) :- J is I+1,
    (ord_memberchk(I,Seen) -> components(J,N,Rows,Seen,Count)
    ; visit([I],Rows,Seen,Next), components(J,N,Rows,Next,C), Count is C+1).
main :- read_numbers([N|Xs]), matrix_rows(Xs,N,Rows), components(1,N,Rows,[],C), writeln(C).
