module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)

readInts :: IO [Int]
readInts = do
  s <- BS.getContents
  return $ map (maybe 0 fst . BS.readInt) (BS.words s)

feasible :: [Int] -> Int -> Int -> Bool
feasible (x:xs) mid c = go xs x 1 >= c
  where
    go [] _ cnt = cnt
    go (a:as) prev cnt
      | a - prev >= mid = go as a (cnt + 1)
      | otherwise = go as prev cnt
feasible [] _ _ = False

main :: IO ()
main = do
  ws <- readInts
  case ws of
    (n:c:rest) -> do
      let a = sort (take n rest)
          hi = last a - head a
          binSearch lo hi' ans
            | lo > hi' = ans
            | feasible a mid c = binSearch (mid + 1) hi' mid
            | otherwise = binSearch lo (mid - 1) ans
            where mid = lo + (hi' - lo) `div` 2
          ans = binSearch 1 hi 0
      print ans
    _ -> return ()