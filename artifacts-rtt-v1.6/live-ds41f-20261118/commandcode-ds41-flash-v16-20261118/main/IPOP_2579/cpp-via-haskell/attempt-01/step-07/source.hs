module Main where

import Data.List (foldl')

solve :: Int -> [Int] -> Int
solve n xs
  | n <= 0 = 0
  | otherwise =
      case xs of
        [] -> 0
        (s1:ys) ->
          case ys of
            [] -> s1
            (s2:rest) ->
              let (_, _, dpn, _) = foldl' step (0, s1, s1 + s2, s2) rest
              in dpn
  where
    step (dp3, dp2, dp1, prevScore) score =
      let cur = max dp2 (dp3 + prevScore) + score
      in (dp2, dp1, cur, score)

main :: IO ()
main = do
  input <- getContents
  let values = map read (words input) :: [Int]
  case values of
    [] -> return ()
    (n:rest) -> do
      let scores = take n rest
      print (solve n scores)