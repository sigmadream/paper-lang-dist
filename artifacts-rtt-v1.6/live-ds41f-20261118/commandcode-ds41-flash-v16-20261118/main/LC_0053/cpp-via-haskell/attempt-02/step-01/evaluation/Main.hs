module Main where

import Data.List (foldl')

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (nw:rest) -> do
      let n = read nw :: Int
          a = map read (take n rest) :: [Integer]
      case a of
        [] -> print (0 :: Integer)
        (x:xs) ->
          let (_, best) = foldl' step (x, x) xs
              step (cur, bestSoFar) v =
                let cur' = max v (cur + v)
                in (cur', max bestSoFar cur')
          in print best