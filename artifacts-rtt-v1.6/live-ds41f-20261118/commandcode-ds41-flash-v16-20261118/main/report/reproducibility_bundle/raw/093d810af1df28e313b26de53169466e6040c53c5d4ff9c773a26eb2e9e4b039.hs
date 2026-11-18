module Main where

import qualified Data.ByteString.Lazy.Char8 as BS
import Data.List (sort)
import Data.List (foldl')

main :: IO ()
main = do
    input <- BS.getContents
    let nums = map (read . BS.unpack) (BS.words input) :: [Int]
    case nums of
        (n:c:rest) -> do
            let houses = sort (take n rest)
            print (solve c houses)
        _ -> return ()

solve :: Int -> [Int] -> Int
solve c houses =
    let lo = 1
        hi = last houses - head houses
    in binary lo hi 0
  where
    binary :: Int -> Int -> Int -> Int
    binary l r ans
        | l > r = ans
        | otherwise =
            let mid = l + (r - l) `div` 2
                cnt = countWithMinDistance mid houses
            in if cnt >= c
                  then binary (mid + 1) r mid
                  else binary l (mid - 1) ans

countWithMinDistance :: Int -> [Int] -> Int
countWithMinDistance d (x:xs) =
    let (cnt, _) = foldl' step (1, x) xs
    in cnt
  where
    step (cnt, prev) cur
        | cur - prev >= d = (cnt + 1, cur)
        | otherwise       = (cnt, prev)
countWithMinDistance _ [] = 0