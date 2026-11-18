hanoi 0 _ _ _ rest = rest
hanoi n a b c rest = hanoi (n-1) a c b ((show a ++ " " ++ show c) : hanoi (n-1) b a c rest)
main = do
  n <- fmap read getContents :: IO Int
  print ((2::Integer)^n - 1)
  mapM_ putStrLn (hanoi n (1::Int) 2 3 [])
