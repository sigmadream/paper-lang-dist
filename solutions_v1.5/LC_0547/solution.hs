import qualified Data.IntSet as Set
import qualified Data.IntMap.Strict as Map
import Data.List (foldl')

buildAdj :: Int -> [(Int, Int)] -> Map.IntMap [Int]
buildAdj n pairs = foldl' addEdge Map.empty pairs
  where
    addEdge m (idx, val)
      | val == 1 =
          let u = idx `div` n
              v = idx `mod` n
          in Map.insertWith (++) u [v] m
      | otherwise = m

dfs :: [Int] -> Map.IntMap [Int] -> Set.IntSet -> Set.IntSet
dfs [] _ seen = seen
dfs (u:stack) adj seen =
    let neighbors = Map.findWithDefault [] u adj
        unvisited = filter (`Set.notMember` seen) neighbors
        newSeen = foldl' (flip Set.insert) seen unvisited
    in dfs (unvisited ++ stack) adj newSeen

countProvinces :: Int -> Map.IntMap [Int] -> Int
countProvinces n adj = go 0 Set.empty 0
  where
    go i seen count
      | i >= n = count
      | Set.member i seen = go (i + 1) seen count
      | otherwise =
          let newSeen = dfs [i] adj (Set.insert i seen)
          in go (i + 1) newSeen (count + 1)

main :: IO ()
main = do
    content <- getContents
    case words content of
        [] -> return ()
        (nStr:rest) -> do
            let n = read nStr :: Int
                vals = map read rest :: [Int]
                pairs = zip [0..] vals
                adj = buildAdj n pairs
            print (countProvinces n adj)
