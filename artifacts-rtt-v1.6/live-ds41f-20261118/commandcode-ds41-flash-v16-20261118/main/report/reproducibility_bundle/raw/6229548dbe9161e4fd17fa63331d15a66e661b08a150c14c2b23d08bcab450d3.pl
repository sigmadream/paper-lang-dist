:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
:- set_prolog_flag(optimise, true).
search(Mask,Mask,_,_,1) :- !.
search(Mask,Columns,Down,Up,Count) :- Available is Mask /\ \(Columns \/ Down \/ Up), choices(Available,Mask,Columns,Down,Up,0,Count).
choices(0,_,_,_,_,Count,Count) :- !.
choices(Available,Mask,Columns,Down,Up,SoFar,Count) :-
    Bit is Available /\ -Available, Rest is Available-Bit,
    C is Columns \/ Bit, D is (Down \/ Bit)<<1, U is (Up \/ Bit)>>1,
    search(Mask,C,D,U,Branch), Next is SoFar+Branch,
    choices(Rest,Mask,Columns,Down,Up,Next,Count).
branch(Mask,Column,Count) :- Bit is 1<<Column, D is Bit<<1, U is Bit>>1, search(Mask,Bit,D,U,Count).
main :- read_numbers([N]), Mask is (1<<N)-1, Last is N//2-1,
    findall(Count,(between(0,Last,C),branch(Mask,C,Count)),Counts), sum_list(Counts,Half),
    (N mod 2 =:= 1 -> Center is N//2, branch(Mask,Center,Extra); Extra=0),
    Answer is 2*Half+Extra, writeln(Answer).
