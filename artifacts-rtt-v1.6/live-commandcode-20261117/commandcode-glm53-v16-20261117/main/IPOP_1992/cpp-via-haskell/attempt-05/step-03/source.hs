module Main (main) where

import Data.Char (isDigit)
import qualified Data.ByteString.Char8 as BS

solve :: [BS.ByteString] -> Int -> Int -> Int -> String
solve grid r c size
  | same = [first]
  | otherwise = "(" ++ concatMap quad [0,1,2,3] ++ ")"
  where
    first = BS.index (grid !! r) c
    same = all (\i -> all (\j -> BS.index (grid !! i) j == first) [c .. c+size-1]) [r .. r+size-1]
    half = size `div` 2
    quad k =
      let dr = (k `div` 2) * half
          dc = (k `mod` 2) * half
      in solve grid (r + dr) (c + dc) half

main :: IO ()
main = do
  contents <- BS.getContents
  let (nLine, rest) = BS.break (== '\n') contents
      n = read (filter isDigit (BS.unpack nLine)) :: Int
      grid = filter (not . BS.null) (BS.lines rest)
  putStrLn (solve grid 0 0 n)