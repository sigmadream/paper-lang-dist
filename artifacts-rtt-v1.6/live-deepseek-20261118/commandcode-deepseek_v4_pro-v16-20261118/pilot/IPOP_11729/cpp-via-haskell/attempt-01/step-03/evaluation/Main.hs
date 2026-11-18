module Main where

main :: IO ()
main = do
  input <- getLine
  let n = read input :: Int
  let moves = hanoi n 1 2 3
  putStrLn (show (length moves))
  mapM_ (\(from, to) -> putStrLn (show from ++ " " ++ show to)) moves

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 start _ end = [(start, end)]
hanoi n start mid end =
  hanoi (n - 1) start end mid
    ++ [(start, end)]
    ++ hanoi (n - 1) mid start end