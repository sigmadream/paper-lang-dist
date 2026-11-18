balanced [] depth = depth == 0
balanced (c:cs) depth
  | depth < 0 = False
  | c == '(' = balanced cs (depth+1)
  | otherwise = balanced cs (depth-1)
main = do
  input <- fmap words getContents
  let n = read (head input) :: Int
  mapM_ (putStrLn . (\s -> if balanced s (0::Int) then "YES" else "NO")) (take n (tail input))
