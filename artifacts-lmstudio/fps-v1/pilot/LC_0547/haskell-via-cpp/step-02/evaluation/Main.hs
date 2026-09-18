import Data.List (findIndex)
import Data.Maybe (fromJust)

components :: [[Int]] -> Int -> Int
components graph n = go graph [0..n-1] 0
  where
    go g [] count = count
    go g (i:is) count =
      let (newG, newIs) = bfs g i
      in go newG newIs (count + 1)

bfs :: [[Int]] -> Int -> ([[Int]], [Int])
bfs graph start = go graph [start] []
  where
    go g [] seen = (g, seen)
    go g (i:is) seen =
      let neighbors = filter ((== 1) . flip (!!) i) [0..length g - 1]
          newSeen = seen ++ i : neighbors
          newIs = is ++ filter (`notElem` newSeen) neighbors
      in go g newIs newSeen

main :: IO ()
main = do
  n <- readLn :: IO Int
  graph <- replicateM n (replicateM n readLn :: IO [Int])
  print $ components graph n