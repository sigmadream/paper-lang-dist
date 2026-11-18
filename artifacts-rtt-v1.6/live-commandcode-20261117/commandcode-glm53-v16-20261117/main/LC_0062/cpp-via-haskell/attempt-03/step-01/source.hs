module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  line <- getLine
  let (mS, nS) = span (/= ' ') (dropWhile (== ' ') line)
      m = read mS :: Int
      n = read (dropWhile (== ' ') nS) :: Int
      dp0 = replicate n 1 :: [Integer]
      step dp = scanl1 (+) dp
      dp = iterate step dp0 !! (m - 1)
  print (last dp)