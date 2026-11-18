module Main (main) where

import Data.List (foldl')
import qualified Data.IntSet as IS
import System.IO

solve :: Int -> Int -> IS.IntSet -> IS.IntSet -> IS.IntSet -> Int
solve n r cols d1 d2
  | r == n = 1
  | otherwise = sum
      [ solve n (r+1) (IS.insert c cols) (IS.insert (r+c) d1) (IS.insert (r-c+n-1) d2)
      | c <- [0 .. n-1]
      , not (IS.member c cols)
      , not (IS.member (r+c) d1)
      , not (IS.member (r-c+n-1) d2)
      ]

main :: IO ()
main = do
  inp <- getContents
  let ns = map read (words inp) :: [Int]
  case ns of
    (n:_) -> print (solve n 0 IS.empty IS.empty IS.empty)
    _ -> return ()