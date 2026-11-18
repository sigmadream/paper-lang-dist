module Main where

import qualified Data.Map.Strict as M
import qualified Data.Set as S
import qualified Data.Sequence as Seq
import Data.List (foldl')

main :: IO ()
main = do
  input <- getContents
  let xs = map read (words input) :: [Int]
  case xs of
    (n : m : rest) -> do
      let pairs = take m (pairUp rest)
          adj = foldl' addEdge M.empty pairs
      print (bfs adj n)
    _ -> return ()

pairUp :: [Int] -> [(Int, Int)]
pairUp (a : b : ts) = (a, b) : pairUp ts
pairUp _ = []

addEdge :: M.Map Int [Int] -> (Int, Int) -> M.Map Int [Int]
addEdge mp (a, b) =
  let mp1 = M.insertWith (++) a [b] mp
      mp2 = M.insertWith (++) b [a] mp1
  in mp2

bfs :: M.Map Int [Int] -> Int -> Int
bfs adj _ =
  go (Seq.singleton (1, 0)) (S.singleton 1) 0
  where
    go q seen count =
      case Seq.viewl q of
        Seq.EmptyL -> count
        ((u, d) Seq.:< qrest) ->
          let neigh = M.findWithDefault [] u adj
              (q', seen', count') = foldl' (step d) (qrest, seen, count) neigh
          in go q' seen' count'

    step d (q, seen, count) v
      | S.member v seen = (q, seen, count)
      | otherwise =
          let nd = d + 1
              count' = if nd <= 2 then count + 1 else count
          in (q Seq.|> (v, nd), S.insert v seen, count')