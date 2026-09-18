import Data.List (findIndex)
import Data.Maybe (fromJust)

main :: IO ()
main = do
    [n, m] <- map read . words <$> getLine
    edges <- replicateM m $ map read . words <$> getLine
    let adj = buildAdjList n edges
    print $ bfsCount adj 1

buildAdjList :: Int -> [(Int, Int)] -> [[Int]]
buildAdjList n edges = [neighbors i | i <- [1..n]]
  where
    neighbors i = [j | (a, b) <- edges, a == i || b == i]

bfsCount :: [[Int]] -> Int -> Int
bfsCount adj start = length $ filter (\x -> x > 0 && x <= 2) distances
  where
    (distances, _) = bfs adj [start] []
    bfs _ [] visited = ([], visited)
    bfs adj (node:queue) visited =
        let newVisited = node : visited
            newQueue = queue ++ filter (`notElem` newVisited) (adj !! (node - 1))
            newDistances = updateDistances distances node (length newVisited)
        in bfs adj newQueue newDistances

updateDistances :: [Int] -> Int -> Int -> [Int]
updateDistances ds node dist = take (length ds) $ zipWith (\d x -> if d == -1 && x == node then dist else d) ds (repeat (-1))