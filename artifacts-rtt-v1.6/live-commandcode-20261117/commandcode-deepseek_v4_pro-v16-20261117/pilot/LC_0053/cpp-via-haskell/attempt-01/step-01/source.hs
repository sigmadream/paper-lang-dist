module Main where

import Data.List (foldl')

maxSubArray :: [Int] -> Int
maxSubArray (x:xs) = fst $ foldl' step (x, x) xs
  where
    step (cur, best) a = (cur', max best cur')
      where
        cur' = max a (cur + a)
maxSubArray [] = 0

main :: IO ()
main = do
  content <- getContents
  let tokens = words content
  let n = read (head tokens) :: Int
  let nums = map read (take n (tail tokens)) :: [Int]
  print (maxSubArray nums)