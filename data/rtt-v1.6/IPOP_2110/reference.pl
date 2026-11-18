:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
placed([],_,_,Count,Count).
placed([X|Xs],Gap,Previous,Count,Answer) :- (X-Previous >= Gap -> Next is Count+1, placed(Xs,Gap,X,Next,Answer); placed(Xs,Gap,Previous,Count,Answer)).
search(_,_,Lo,Hi,Answer,Answer) :- Lo > Hi, !.
search([X|Xs],Needed,Lo,Hi,Old,Answer) :- Mid is (Lo+Hi)//2, placed(Xs,Mid,X,1,Count),
    (Count >= Needed -> Next is Mid+1, search([X|Xs],Needed,Next,Hi,Mid,Answer); Next is Mid-1, search([X|Xs],Needed,Lo,Next,Old,Answer)).
main :- read_numbers([_,Needed|Xs]), msort(Xs,[First|Rest]), last([First|Rest],Last), Hi is Last-First, search([First|Rest],Needed,1,Hi,0,Answer), writeln(Answer).
