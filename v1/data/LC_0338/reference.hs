ones 0 = 0
ones n = n `mod` 2 + ones (n `div` 2)
main = do
  n <- fmap read getContents :: IO Int
  putStrLn (unwords (map (show . ones) [0..n]))
