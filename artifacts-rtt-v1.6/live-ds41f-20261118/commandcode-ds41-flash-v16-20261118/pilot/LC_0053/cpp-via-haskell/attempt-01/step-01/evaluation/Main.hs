module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  input <- getContents
  let values = map read (words input) :: [Integer]
  case values of
    (n:rest) ->
      let a = take (fromIntegral n) rest
      in case a of
           [] -> return ()
           (x:xs) ->
             let (_, best) = foldl' step (x, x) xs
                 step (cur, bestSoFar) y =
                   let cur' = max y (cur + y)
                       best' = max bestSoFar cur'
                   in (cur', best')
             in print best
    _ -> return ()