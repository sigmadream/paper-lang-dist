module Main where

import Data.Array
import qualified Data.Set as Set
import Data.List (foldl')

main :: IO ()
main = do
    s <- getContents
    let vals = map read (words s) :: [Int]
    case vals of
        [] -> return ()
        (n:m:rest) -> do
            let es = take m (toPairs rest)
                adj = accumArray (flip (:)) [] (1, n) $
                      concatMap (\(a, b) -> [(a, b), (b, a)]) es
                ans = countWithinTwo n adj
            print ans
        _ -> return ()

toPairs :: [Int] -> [(Int, Int)]
toPairs (a:b:rest) = (a, b) : toPairs rest
toPairs _ = []

countWithinTwo :: Int -> Array Int [Int] -> Int
countWithinTwo n adj
    | n < 1 = 0
    | otherwise = go (Set.singleton 1) [(1, 0 :: Int)] 0
  where
    go _ [] ans = ans
    go visited ((x, d):q) ans =
        let nbrs = adj ! x
            fresh = filter (`Set.notMember` visited) nbrs
            visited' = foldl' (flip Set.insert) visited fresh
            nd = d + 1
            ans' = if nd <= 2 then ans + length fresh else ans
            q' = if nd < 2 then q ++ [(y, nd) | y <- fresh] else q
        in go visited' q' ans'