module Main (main) where

import qualified Data.IntMap.Strict as IM
import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  let (nLine : rest) = lines inp
      _n = read nLine :: Int
      (mLine : edgeLines) = rest
      _m = read mLine :: Int
      edges = map parseEdge edgeLines
      adj = foldl' addEdge IM.empty edges
      visited = bfs adj (IM.singleton 1 (0 :: Int)) [1]
      ans = length [ d | (_, d) <- IM.toList visited, d == 1 || d == 2 ]
  print ans
  where
    parseEdge l = let (a, b) = span (/= ' ') l in (read a :: Int, read (dropWhile (== ' ') b) :: Int)
    addEdge m (u, v) = IM.insertWith (++) u [v] (IM.insertWith (++) v [u] m)
    bfs _ dist [] = dist
    bfs adj dist (c : cs)
      | otherwise =
          let d = dist IM.! c
              ns = IM.findWithDefault [] c adj
              newNs = [v | v <- ns, not (IM.member v dist)]
              dist' = foldl' (\m' v -> IM.insert v (d + 1) m') dist newNs
          in bfs adj dist' (cs ++ newNs)