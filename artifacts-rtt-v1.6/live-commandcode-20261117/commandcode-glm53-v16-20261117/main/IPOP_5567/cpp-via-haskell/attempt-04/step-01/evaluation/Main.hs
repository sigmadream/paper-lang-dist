module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.Sequence (Seq, (|>), (><))
import qualified Data.Sequence as Seq
import qualified Data.IntSet as Set
import qualified Data.IntMap as Map
import Data.Maybe (fromMaybe)

readInts :: IO [Int]
readInts = do
  s <- BS.getContents
  return (map (maybe 0 fst . BS.readInt) (BS.words s))

main :: IO ()
main = do
  xs <- readInts
  case xs of
    (n:m:rest) -> do
      let edges = pairs rest
          adj = buildAdj edges
          ans = bfsCount adj n
      print ans
    _ -> return ()

pairs :: [Int] -> [(Int, Int)]
pairs (a:b:r) = (a, b) : pairs r
pairs _ = []

buildAdj :: [(Int, Int)] -> Map.IntMap [Int]
buildAdj = foldl add Map.empty
  where
    add m (u, v) = Map.insertWith (++) u [v] (Map.insertWith (++) v [u] m)

bfsCount :: Map.IntMap [Int] -> Int -> Int
bfsCount adj _ = go (Seq.singleton 1) (Set.singleton 1) 0 0
  where
    go queue visited ans d
      | Seq.null queue = ans
      | d >= 2 = go Seq.empty visited ans d
      | otherwise =
          let (curr Seq.:< rest) = Seq.viewl queue
              nbrs = fromMaybe [] (Map.lookup curr adj)
              new = [x | x <- nbrs, not (Set.member x visited)]
              visited' = foldr Set.insert visited new
              ans' = ans + length new
          in go (rest >< Seq.fromList new) visited' ans' (d + 1)