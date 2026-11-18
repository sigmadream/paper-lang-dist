:- use_module(library(readutil)).
read_words(Words) :- read_string(user_input, _, Text), split_string(Text, " \n\r\t", " \n\r\t", Words).
read_numbers(Numbers) :- read_words(Words), maplist(number_string, Numbers, Words).
write_numbers(Numbers) :- atomic_list_concat(Numbers, ' ', Text), writeln(Text).
cell(Grid,R,C,Value) :- I is R+1, J is C+1, arg(I,Grid,Row), arg(J,Row,Value).
same(Grid,R,C,N,Value) :- EndR is R+N-1, EndC is C+N-1, forall((between(R,EndR,I),between(C,EndC,J)),cell(Grid,I,J,Value)).
encode(Grid,R,C,N) :- cell(Grid,R,C,Value),
    (same(Grid,R,C,N,Value) -> put_code(Value);
    H is N//2, R2 is R+H, C2 is C+H, put_char('('), encode(Grid,R,C,H), encode(Grid,R,C2,H), encode(Grid,R2,C,H), encode(Grid,R2,C2,H), put_char(')')).
row_term(Text,Row) :- string_codes(Text,Codes), Row =.. [row|Codes].
main :- read_words([Size|Lines]), number_string(N,Size), maplist(row_term,Lines,Rows), Grid =.. [grid|Rows], encode(Grid,0,0,N), nl.
