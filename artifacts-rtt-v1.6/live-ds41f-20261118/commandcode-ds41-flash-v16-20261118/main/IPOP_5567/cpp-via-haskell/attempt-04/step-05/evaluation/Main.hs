module Main where

import qualified Data.IntMap.Strict as IM
import qualified Data.Set as Set
import Data.List (foldl')
import Data.Maybe (fromMaybe)

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Int]
  case nums of
    (n : m : rest) -> do
      let edges = pairUp (take (2 * m) rest)
          adj = foldl' addEdge IM.empty edges
          visited = bfs adj (Set.singleton 1) [(1, 0)]
          answer = if n >= 1 then Set.size visited - 1 else 0
      print answer
    _ -> return ()

pairUp :: [Int] -> [(Int, Int)]
pairUp (a : b : xs) = (a, b) : pairUp xs
pairUp _ = []

addEdge :: IM.IntMap [Int] -> (Int, Int) -> IM.IntMap [Int]
addEdge mp (a, b) =
  IM.insertWith (++) b [a] $
  IM.insertWith (++) a [b] mp

bfs :: IM.IntMap [Int] -> Set.Set Int -> [(Int, Int)] -> Set.Set Int
bfs _ visited [] = visited
bfs adj visited ((u, d) : q)
  | d >= 2 = bfs adj visited q
  | otherwise =
      let (vis', newQ) = foldl' step (visited, []) (fromMaybe [] (IM.lookup u adj))
          step (vis, acc) v
            | Set.member v vis = (vis, acc)
            | otherwise = (Set.insert v vis, acc ++ [(v, d + 1)])
      in bfs adj vis' (q ++ newQ)