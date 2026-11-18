module Main (main) where

import Data.List (intercalate)

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    (nStr:rest) -> do
      let n = read nStr :: Int
          nums = map read (take n rest) :: [Integer]
          nonZeros = filter (/= 0) nums
          zeros = filter (== 0) nums
          result = nonZeros ++ zeros
      putStrLn (intercalate " " (map show result))
    _ -> return ()