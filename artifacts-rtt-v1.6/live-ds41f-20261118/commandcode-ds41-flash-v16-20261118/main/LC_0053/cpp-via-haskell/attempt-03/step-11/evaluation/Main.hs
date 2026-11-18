module Main where

import Data.List (foldl')

solve :: [Int] -> Int
solve [] = 0
solve (x:xs) = snd (foldl' step (x, x) xs)
  where
    step (cur, best) y =
      let cur' = max y (cur + y)
          best' = max best cur'
      in (cur', best')

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Int]
  case nums of
    [] -> return ()
    (n:rest) ->
      if n == 0
        then putStrLn "0"
        else putStrLn (show (solve (take n rest)))