main = do
  values <- fmap (map read . words) getContents :: IO [Integer]
  let n = fromInteger (head values)
      xs = take n (tail values)
      nonzero = filter (/=0) xs
      answer = nonzero ++ replicate (n-length nonzero) 0
  putStrLn (unwords (map show answer))
