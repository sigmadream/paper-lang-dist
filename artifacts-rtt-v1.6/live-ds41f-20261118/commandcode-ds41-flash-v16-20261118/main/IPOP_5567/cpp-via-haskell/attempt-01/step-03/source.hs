module Main where

import qualified Data.IntMap.Strict as IM
import Data.List (foldl')
import Data.Sequence (Seq, ViewL(..), (|>), singleton, viewl)

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Int]
  case nums of
    [] -> return ()
    (n:rest) -> do
      let (m, rest2) = case rest of
                         [] -> (0, [])
                         (x:xs) -> (x, xs)
          edges = pairs (take (2 * m) rest2)
          adj = foldl' addEdge IM.empty edges
          dist = bfs adj
          ans = length [() | (v, d) <- IM.toList dist, v /= 1, d == 1 || d == 2]
      print ans

pairs :: [Int] -> [(Int, Int)]
pairs (a:b:cs) = (a, b) : pairs cs
pairs _ = []

addEdge :: IM.IntMap [Int] -> (Int, Int) -> IM.IntMap [Int]
addEdge mp (a, b) =
  IM.insertWith (++) b [a] (IM.insertWith (++) a [b] mp)

bfs :: IM.IntMap [Int] -> IM.IntMap Int
bfs adj = go (IM.singleton 1 0) (singleton 1)
  where
    go dist q = case viewl q of
      EmptyL -> dist
      (u :< qs) ->
        let du = dist IM.! u
        in if du == 2
             then go dist qs
             else
               let vs = IM.findWithDefault [] u adj
                   step (d, qq) v =
                     if IM.member v d
                       then (d, qq)
                       else (IM.insert v (du + 1) d, qq |> v)
                   (dist', q') = foldl' step (dist, qs) vs
               in go dist' q'