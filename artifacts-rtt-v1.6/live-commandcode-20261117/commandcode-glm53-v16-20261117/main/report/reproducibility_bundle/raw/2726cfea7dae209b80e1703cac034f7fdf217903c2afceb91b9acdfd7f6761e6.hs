module Main (main) where

import Data.Char (isDigit)
import Data.Bits (shiftL)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
  line <- getLine
  let digits = takeWhile isDigit (dropWhile (not . isDigit) line)
      n = read digits :: Int
      moves = if n > 0 then hanoi n 1 2 3 else []
      count = (1 `shiftL` n) - 1 :: Integer
  putStrLn (show count)
  mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) moves