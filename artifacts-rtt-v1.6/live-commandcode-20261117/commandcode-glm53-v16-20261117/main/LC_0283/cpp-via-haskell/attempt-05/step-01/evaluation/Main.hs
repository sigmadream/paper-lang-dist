module Main (main) where

import Data.List (intercalate)
import Data.Maybe (fromMaybe)

main :: IO ()
main = do
  first <- getLine
  let n = read first :: Int
  rest <- getContents
  let nums = take n (map read (words rest) :: [Integer])
      nonZeros = filter (/= 0) nums
      zeros = replicate (n - length nonZeros) 0
  putStrLn (intercalate " " (map show (nonZeros ++ zeros)))