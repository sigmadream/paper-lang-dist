module Main where

import Data.List (foldl')

main :: IO ()
main = do
  contents <- getContents
  let nums = map read (words contents) :: [Integer]
  case nums of
    [] -> return ()
    (n:rest) ->
      let k = fromIntegral n
          arr = take k rest
      in if k <= 0
           then return ()
           else case arr of
             [] -> return ()
             (x:xs) ->
               let (_, best) = foldl' step (x, x) xs
                   step (cur, bestSoFar) y =
                     let cur' = max y (cur + y)
                         best' = max bestSoFar cur'
                     in (cur', best')
               in print best