module Main (main) where

import System.IO

gcd' :: Int -> Int -> Int
gcd' a b
  | b == 0    = a
  | otherwise = gcd' b (a `mod` b)

main :: IO ()
main = do
  line <- getLine
  case map read (words line) :: [Int] of
    (a:b:_) -> do
      let g = gcd' a b
      putStrLn (show g)
      putStrLn (show ((a `div` g) * b))
    _ -> return ()