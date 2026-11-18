module Main where

import Data.List (foldl')

main :: IO ()
main = do
  input <- getContents
  let tokens = map read (words input) :: [Integer]
  case tokens of
    [] -> return ()
    (n:rest)
      | n <= 0 -> return ()
      | otherwise ->
          let m = min n (toInteger (length rest))
          in if m <= 0
             then return ()
             else case rest of
               [] -> return ()
               (first:others) ->
                 let k = fromInteger (m - 1)
                     step (cur, bestSoFar) y =
                       let cur' = max y (cur + y)
                           best' = max bestSoFar cur'
                       in (cur', best')
                     (_, best) = foldl' step (first, first) (take k others)
                 in print best