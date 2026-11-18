module Main where

import Data.Array
import qualified Data.Set as Set

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Int]
  case nums of
    [] -> return ()
    (n : rest) ->
      case rest of
        [] -> return ()
        (m : rest2) ->
          if n <= 0
            then putStrLn "0"
            else do
              let rawEdges = take m (toPairs rest2)
                  edges =
                    [ (a, b)
                    | (a, b) <- rawEdges
                    , a >= 1, a <= n
                    , b >= 1, b <= n
                    ]
                  bothDirections = concat [[(a, b), (b, a)] | (a, b) <- edges]
                  adj = accumArray (\xs x -> x : xs) [] (1, n) bothDirections :: Array Int [Int]
                  neighborsOfOne = adj ! 1
                  reachable =
                    Set.fromList
                      (neighborsOfOne ++ concatMap (\u -> adj ! u) neighborsOfOne)
                  answer = Set.size (Set.delete 1 reachable)
              print answer

toPairs :: [Int] -> [(Int, Int)]
toPairs (a : b : xs) = (a, b) : toPairs xs
toPairs _ = []