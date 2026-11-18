module Main where

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi n start mid end
  | n == 1 = [(start, end)]
  | otherwise = hanoi (n - 1) start end mid ++ [(start, end)] ++ hanoi (n - 1) mid start end

main :: IO ()
main = do
  input <- getContents
  let n = read (head (words input)) :: Int
      moves = hanoi n 1 2 3
  print (length moves)
  mapM_ (\(a, b) -> putStrLn $ show a ++ " " ++ show b) moves