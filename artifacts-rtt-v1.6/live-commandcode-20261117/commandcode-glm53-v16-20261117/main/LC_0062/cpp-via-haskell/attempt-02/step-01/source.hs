module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  l <- getLine
  let ws = words l
      m  = read (ws !! 0) :: Integer
      n  = read (ws !! 1) :: Integer
  -- dp row of length n, all 1s; update (m-1) times
  let step dp = scanl1 (+) dp
      dp = foldl' (\acc _ -> step acc) (replicate (fromIntegral n) 1) [1 .. m - 1]
  print (last dp)