module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.Array
import Data.List (foldl')
import Data.Maybe (fromMaybe)

main :: IO ()
main = do
    input <- BS.getContents
    let nums = map (fst . fromMaybe (0, BS.empty) . BS.readInt) (BS.words input)
    case nums of
        [] -> return ()
        (n:rest) ->
            let m = case rest of
                        (x:_) -> x
                        [] -> 0
                vals = case rest of
                           (_:xs) -> xs
                           [] -> []
                rawPairs = take (2 * m) vals
                pairs = makePairs rawPairs
                validPairs = [ (a, b) | (a, b) <- pairs, a >= 1, a <= n, b >= 1, b <= n ]
            in if n <= 0
                then putStrLn "0"
                else do
                    let edges = concatMap (\(a, b) -> [(a, b), (b, a)]) validPairs
                        adj = accumArray (flip (:)) [] (1, n) edges
                        initialDist = array (1, n) [(i, -1) | i <- [1..n]] // [(1, 0)]
                        dist = bfs adj initialDist [(1, 0)]
                        answer = length [ v | v <- [2..n], let d = dist ! v, d == 1 || d == 2 ]
                    print answer

makePairs :: [Int] -> [(Int, Int)]
makePairs (a:b:xs) = (a, b) : makePairs xs
makePairs _ = []

bfs :: Array Int [Int] -> Array Int Int -> [(Int, Int)] -> Array Int Int
bfs _ dist [] = dist
bfs adj dist ((u, du):q)
    | du >= 2 = bfs adj dist q
    | otherwise =
        let (dist', q') = foldl' step (dist, q) (adj ! u)
            step (d, queue) v =
                if d ! v == -1
                    then (d // [(v, du + 1)], queue ++ [(v, du + 1)])
                    else (d, queue)
        in bfs adj dist' q'