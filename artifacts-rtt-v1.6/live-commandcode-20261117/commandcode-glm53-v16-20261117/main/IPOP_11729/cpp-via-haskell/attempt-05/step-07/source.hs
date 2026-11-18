module Main (main) where

import Data.Char (isDigit)
import Data.Bits (shiftL)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
  input <- getLine
  let digits = takeWhile isDigit (dropWhile (not . isDigit) input)
      n = read digits :: Int
      moves = hanoi n 1 2 3
  putStrLn (show ((2 ^ n) - 1 :: Integer))
  mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) moves