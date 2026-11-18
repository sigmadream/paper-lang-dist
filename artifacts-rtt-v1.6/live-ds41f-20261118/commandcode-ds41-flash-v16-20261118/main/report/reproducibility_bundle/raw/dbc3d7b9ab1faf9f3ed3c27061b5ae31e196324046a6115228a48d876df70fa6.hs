module Main where

import Data.List (foldl')

main :: IO ()
main = do
  input <- getContents
  let values = map read (words input) :: [Integer]
  case values of
    (n : rest) -> do
      let arr = take (fromIntegral n) rest
      case arr of
        [] -> return ()
        (x : xs) -> do
          let (_, best) = foldl' step (x, x) xs
              step (cur, ans) v =
                let newCur = max v (cur + v)
                    newAns = max ans newCur
                in (newCur, newAns)
          print best
    _ -> return ()