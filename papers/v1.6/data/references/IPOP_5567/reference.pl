:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
edges([],[]).
edges([A,B|Xs],[A-B,B-A|Es]) :- edges(Xs,Es).
main :- read_numbers([_,_|Xs]), edges(Xs,Es),
        findall(B,member(1-B,Es),Direct),
        findall(C,(member(A,Direct),member(A-C,Es)),Second),
        append(Direct,Second,All), sort(All,Unique), delete(Unique,1,Invited), length(Invited,N), writeln(N).
