module Main where

import Data.List (foldl')

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Int]
  case nums of
    [] -> return ()
    (n:rest) -> do
      let scores = take n rest
          dp = foldl' step [0] [1..n]
            where
              step acc i =
                let value
                      | i == 1 = scores !! 0
                      | i == 2 = (scores !! 0) + (scores !! 1)
                      | otherwise =
                          max (acc !! (i - 2))
                              ((acc !! (i - 3)) + (scores !! (i - 2)))
                          + (scores !! (i - 1))
                in acc ++ [value]
      print (last dp)