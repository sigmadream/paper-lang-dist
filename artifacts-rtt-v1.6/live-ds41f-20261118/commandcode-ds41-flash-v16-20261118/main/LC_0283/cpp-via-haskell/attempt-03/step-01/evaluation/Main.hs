module Main where

import Data.List (partition)

main :: IO ()
main = do
  input <- getContents
  let values = map read (words input) :: [Int]
  case values of
    [] -> return ()
    (n:rest) -> do
      let arr = take n rest
          (nonZero, zeros) = partition (/= 0) arr
      putStrLn (unwords (map show (nonZero ++ zeros)))