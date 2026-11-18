module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)
import Data.Maybe (fromMaybe)

readInts :: IO [Int]
readInts = do
  s <- BS.getContents
  return $ map (fst . fromMaybe (0,"") . BS.readInt) (BS.words s)

main :: IO ()
main = do
  xs <- readInts
  case xs of
    (n:c:rest) -> do
      let a = take n rest
          sorted = sort a
          lo0 = 1
          hi0 = last sorted - head sorted
          feasible mid = go (tail sorted) (head sorted) 1 >= c
            where go [] _ cnt = cnt
                  go (x:xs') prev cnt =
                    if x - prev >= mid then go xs' x (cnt+1)
                    else go xs' prev cnt
          binSearch lo hi ans
            | lo > hi = ans
            | otherwise =
                let mid = lo + (hi - lo) `div` 2
                in if feasible mid
                     then binSearch (mid+1) hi mid
                     else binSearch lo (mid-1) ans
      print (binSearch lo0 hi0 0)
    _ -> return ()