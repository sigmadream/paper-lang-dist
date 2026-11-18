import Data.List (nub)

addVertex :: Int -> Int -> [[Int]] -> [[Int]]
addVertex x v adj =
    let (before, rest) = splitAt x adj
    in case rest of
        [] -> adj
        (ys:after) -> before ++ ((v : ys) : after)

addEdge :: Int -> Int -> [[Int]] -> [[Int]]
addEdge a b adj = addVertex b a (addVertex a b adj)

buildEdges :: [Int] -> [(Int, Int)]
buildEdges (a:b:rest) = (a, b) : buildEdges rest
buildEdges _ = []

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Int]
    case nums of
        (n:m:rest) -> do
            let edges = take m (buildEdges rest)
                emptyAdj = replicate (n + 1) []
                adj = foldl (flip (uncurry addEdge)) emptyAdj edges
                friends1 = if n >= 1 then nub (adj !! 1) else []
                friends2 = concatMap (\u -> if u <= n then adj !! u else []) friends1
                candidates = nub (friends1 ++ friends2)
                answer = length (filter (/= 1) candidates)
            putStrLn (show answer)
        _ -> return ()