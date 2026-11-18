module Main (main) where

import qualified Data.IntMap.Strict as IM
import Data.Sequence (Seq, ViewL(..), (|>), singleton, viewl)

main :: IO ()
main = do
  input <- getContents
  let xs = map read (words input) :: [Int]
  case xs of
    [] -> return ()
    (n:m:rest) -> do
      let adj = buildAdj m rest
          dist = bfs adj
          answer = IM.foldrWithKey
            (\k d acc -> if k /= 1 && (d == 1 || d == 2) then acc + 1 else acc)
            0
            dist
      print answer

buildAdj :: Int -> [Int] -> IM.IntMap [Int]
buildAdj m xs = go m xs
  where
    go 0 _ = IM.empty
    go k (a:b:rest) =
      IM.insertWith (++) a [b] $
      IM.insertWith (++) b [a] $
      go (k - 1) rest
    go _ _ = IM.empty

bfs :: IM.IntMap [Int] -> IM.IntMap Int
bfs adj = loop (IM.singleton 1 0) (singleton 1)
  where
    loop dist q =
      case viewl q of
        EmptyL -> dist
        u :< qs ->
          let du = dist IM.! u
              neighbors = IM.findWithDefault [] u adj
              (dist', q') = foldl step (dist, qs) neighbors
              step (d, qq) v =
                if IM.member v d
                  then (d, qq)
                  else (IM.insert v (du + 1) d, qq |> v)
          in loop dist' q'