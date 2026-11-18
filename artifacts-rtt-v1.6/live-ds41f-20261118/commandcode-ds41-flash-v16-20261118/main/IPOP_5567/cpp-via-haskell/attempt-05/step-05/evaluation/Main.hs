module Main (main) where

import qualified Data.IntMap.Strict as IM
import qualified Data.Sequence as Seq
import Data.Sequence (ViewL(..))
import Data.List (foldl')

main :: IO ()
main = do
  input <- getContents
  let xs = map read (words input) :: [Int]
  case xs of
    [] -> return ()
    (n:rest) -> do
      let m = case rest of
                (x:_) -> x
                [] -> 0
          edgeVals = case rest of
                       (_:es) -> es
                       [] -> []
          pairs = take m (pairUp edgeVals)
          validPairs =
            [ (a, b)
            | (a, b) <- pairs
            , a >= 1, a <= n
            , b >= 1, b <= n
            ]
      if n <= 0
        then putStrLn "0"
        else do
          let adj = buildAdj validPairs
              dist = bfs adj
              ans = length
                [ i
                | i <- [2 .. n]
                , isNear (IM.lookup i dist)
                ]
          putStrLn (show ans)

pairUp :: [Int] -> [(Int, Int)]
pairUp (a:b:ts) = (a, b) : pairUp ts
pairUp _ = []

buildAdj :: [(Int, Int)] -> IM.IntMap [Int]
buildAdj edges = foldl' add IM.empty edges
  where
    add graph (a, b) =
      IM.insertWith (++) b [a] (IM.insertWith (++) a [b] graph)

bfs :: IM.IntMap [Int] -> IM.IntMap Int
bfs adj = go (Seq.singleton 1) (IM.singleton 1 0)
  where
    go queue dist =
      case Seq.viewl queue of
        EmptyL -> dist
        u :< rest ->
          let d = dist IM.! u
              vs = IM.findWithDefault [] u adj
              (dist', queue') = foldl' addNeighbor (dist, rest) vs
              addNeighbor (dm, qq) v =
                if IM.member v dm
                  then (dm, qq)
                  else (IM.insert v (d + 1) dm, qq Seq.|> v)
          in go queue' dist'

isNear :: Maybe Int -> Bool
isNear (Just 1) = True
isNear (Just 2) = True
isNear _ = False