module Main where

import Data.List (partition)

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (nStr : rest) ->
      let n = read nStr :: Int
          arr = take n (map read rest :: [Int])
          (nonZeroes, _) = partition (/= 0) arr
          result = nonZeroes ++ replicate (n - length nonZeroes) 0
      in putStrLn (unwords (map show result))