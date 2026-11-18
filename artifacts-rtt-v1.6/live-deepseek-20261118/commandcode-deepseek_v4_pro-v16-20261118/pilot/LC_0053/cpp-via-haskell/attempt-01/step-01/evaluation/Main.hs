module Main (main) where

import Data.List (foldl')

maxSubarray :: [Integer] -> Integer
maxSubarray (x:xs) = snd $ foldl' step (x, x) xs
  where
    step (cur, best) a =
      let cur' = max a (cur + a)
      in (cur', max best cur')
maxSubarray [] = 0

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Integer]
      n = head nums
      arr = take n (tail nums)
  print (maxSubarray arr)