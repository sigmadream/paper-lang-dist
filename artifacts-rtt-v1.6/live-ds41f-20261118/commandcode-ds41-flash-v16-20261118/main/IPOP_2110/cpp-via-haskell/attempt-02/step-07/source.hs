module Main where

import qualified Data.ByteString.Lazy.Char8 as BS
import Data.List (sort)

solve :: [Int] -> Int -> Int -> Int -> Int -> Int
solve houses c lo hi ans
    | lo > hi = ans
    | count >= c = solve houses c (mid + 1) hi mid
    | otherwise = solve houses c lo (mid - 1) ans
  where
    mid = lo + (hi - lo) `div` 2
    count = countHouses houses mid c

countHouses :: [Int] -> Int -> Int -> Int
countHouses [] _ _ = 0
countHouses (h:hs) d c = go hs h 1
  where
    go [] _ cnt = cnt
    go (x:xs) prev cnt
        | cnt >= c = cnt
        | x - prev >= d = go xs x (cnt + 1)
        | otherwise = go xs prev cnt

main :: IO ()
main = do
    input <- BS.getContents
    let nums = map (read . BS.unpack) (BS.words input) :: [Int]
    case nums of
        (n:c:rest) -> do
            let houses = sort (take n rest)
                lo = 1
                hi = last houses - head houses
            print (solve houses c lo hi 0)
        _ -> return ()