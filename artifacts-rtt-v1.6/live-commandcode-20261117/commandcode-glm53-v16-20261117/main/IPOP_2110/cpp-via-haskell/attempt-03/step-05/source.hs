module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)

readInts :: IO [Integer]
readInts = do
  s <- BS.getContents
  return $ map read (words (map id (BS.unpack s)))

main :: IO ()
main = do
  xs <- readInts
  case xs of
    (n:c:rest) -> do
      let a = take n rest
          s = sort a
          lo0 = 1
          hi0 = last s - head s
          feasible mid = go (tail s) (head s) 1
            where
              go [] _ cnt = cnt
              go (x:xs') prev cnt =
                if x - prev >= mid then go xs' x (cnt+1)
                else go xs' prev cnt
          search lo hi ans
            | lo > hi = ans
            | otherwise =
                let mid = lo + (hi - lo) `div` 2
                    cnt = feasible mid s
                in if cnt >= fromIntegral c
                     then search (mid+1) hi mid
                     else search lo (mid-1) ans
          ans = search lo0 hi0 0
      print ans
    _ -> return ()