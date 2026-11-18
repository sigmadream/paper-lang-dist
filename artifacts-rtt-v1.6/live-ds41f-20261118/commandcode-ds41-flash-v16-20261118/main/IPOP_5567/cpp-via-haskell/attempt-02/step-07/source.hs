module Main (main) where

import Data.Array
import qualified Data.Set as Set

main :: IO ()
main = do
  input <- getContents
  let xs = map read (words input) :: [Int]
  case xs of
    (n:m:rest) ->
      if n < 1
        then putStrLn "0"
        else do
          let pairs (a:b:ts) = (a, b) : pairs ts
              pairs _        = []
              edges = take m (pairs rest)
              adj = accumArray (flip (++)) [] (1, n) $
                      concatMap (\(a, b) -> [(a, b), (b, a)]) edges
              startVisited = Set.singleton 1
              bfs [] _ acc = acc
              bfs ((u, d):q) visited acc
                | d >= 2 = bfs q visited acc
                | otherwise =
                    let nexts = [v | v <- adj ! u, not (Set.member v visited)]
                        visited' = foldl (flip Set.insert) visited nexts
                    in bfs (q ++ [(v, d + 1) | v <- nexts]) visited' (acc + length nexts)
          print (bfs [(1, 0)] startVisited 0)
    _ -> return ()