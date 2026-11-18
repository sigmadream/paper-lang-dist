module Main (main) where

import qualified Data.IntSet as Set
import qualified Data.IntMap.Strict as Map
import Data.List (foldl')

main :: IO ()
main = do
  input <- getContents
  let (n : m : rest) = map read (words input) :: [Int]
      edges = pairs rest
      adj = foldl' (\acc (u, v) ->
                      Map.insertWith (++) u [v] (Map.insertWith (++) v [u] acc))
                   Map.empty edges
      start = Set.singleton 1
      d1 = Set.delete 1 (friendsOf adj start)
      d2 = Set.delete 1 (friendsOf adj d1)
      answer = Set.size (Set.union d1 d2)
  print answer
  where
    pairs (a : b : xs) = (a, b) : pairs xs
    pairs _ = []
    friendsOf adj nodes = Set.fromList
      [ w
      | v <- Set.toList nodes
      , w <- Map.findWithDefault [] v adj
      ]