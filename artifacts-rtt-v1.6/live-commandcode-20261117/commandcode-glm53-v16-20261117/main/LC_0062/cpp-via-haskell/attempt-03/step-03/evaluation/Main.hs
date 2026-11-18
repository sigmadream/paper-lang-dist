module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  line <- getLine
  let (mStr, rest) = break (== ' ') line
      nStr = dropWhile (== ' ') rest
      m = read mStr :: Integer
      n = read nStr :: Integer
      dp0 = replicate (fromIntegral n) 1 :: [Integer]
      step dp = tail (scanl (+) 1 dp)
      dpFinal = iterate step dp0 !! (fromIntegral m - 1)
  print (last dpFinal)