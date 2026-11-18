module Main (main) where

import Data.IORef
import qualified Data.Set as Set

solve :: Int -> Int
solve n = go Set.empty Set.empty Set.empty 0
  where
    go cols d1 d2 r
      | r == n = 1
      | otherwise = sum
          [ if ok c then go (Set.insert c cols) (Set.insert (r+c) d1) (Set.insert (r-c+n-1) d2) (r+1) else 0
          | c <- [0 .. n-1] ]
      where
        ok c = not (Set.member c cols
                 || Set.member (r+c) d1
                 || Set.member (r-c+n-1) d2)

main :: IO ()
main = do
    inp <- getContents
    case map reads (lines inp) of
      ((n,_):_) -> print (solve (n :: Int))
      _ -> return ()