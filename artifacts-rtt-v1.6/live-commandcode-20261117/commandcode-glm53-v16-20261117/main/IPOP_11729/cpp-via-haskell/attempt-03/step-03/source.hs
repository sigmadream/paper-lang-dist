module Main (main) where

import Data.List (intercalate)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
  input <- getLine
  let n = read input :: Int
      moves = hanoi n 1 2 3
  putStrLn (show (length moves))
  mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) moves