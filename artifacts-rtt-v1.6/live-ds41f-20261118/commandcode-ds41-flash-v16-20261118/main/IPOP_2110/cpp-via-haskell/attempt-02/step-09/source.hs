module Main where

import qualified Data.ByteString.Char8 as B
import Data.List (sort)
import Data.Maybe (fromJust)

readInts :: B.ByteString -> [Int]
readInts = map (fst . fromJust . B.readInt) . B.words

main :: IO ()
main = do
    s <- B.getContents
    let (n:c:rest) = readInts s
        houses = sort (take n rest)
        hi = last houses - head houses
        ans = binarySearch houses c 1 hi 0
    print ans

binarySearch :: [Int] -> Int -> Int -> Int -> Int -> Int
binarySearch houses c lo hi ans
    | lo > hi = ans
    | otherwise =
        let mid = lo + (hi - lo) `div` 2
        in if countHouses houses mid c >= c
             then binarySearch houses c (mid + 1) hi mid
             else binarySearch houses c lo (mid - 1) ans

countHouses :: [Int] -> Int -> Int -> Int
countHouses [] _ _ = 0
countHouses (x:xs) d c = go xs 1 x
  where
    go _ cnt _ | cnt >= c = cnt
    go [] cnt _ = cnt
    go (y:ys) cnt prev
        | cnt >= c = cnt
        | y - prev >= d = go ys (cnt + 1) y
        | otherwise = go ys cnt prev