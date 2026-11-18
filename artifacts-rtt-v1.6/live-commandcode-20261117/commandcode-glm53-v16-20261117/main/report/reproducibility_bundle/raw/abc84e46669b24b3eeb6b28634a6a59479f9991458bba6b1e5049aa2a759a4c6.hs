module Main (main) where

import Data.List (intercalate)

main :: IO ()
main = do
  input <- getContents
  let (nLine:rest) = lines input
      n = read nLine :: Int
      nums = take n (map read (words (unwords rest)) :: [Integer])
      nonZeros = filter (/= 0) nums
      zeros = replicate (n - length nonZeros) 0
      result = nonZeros ++ zeros
  putStrLn (intercalate " " (map show result))