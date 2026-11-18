module Main (main) where

import qualified Data.Vector as V
import Data.Vector ((!), (//))
import qualified Data.Vector as Vec

main :: IO ()
main = do
  contents <- getContents
  let (nStr:rest) = lines contents
      n = read nStr :: Int
      scores = map read (take n rest) :: [Int]
      score = Vec.fromList (0 : scores) :: Vec.Vector Int
  if n == 1
    then print (score ! 1)
    else if n == 2
      then print (score ! 1 + score ! 2)
      else do
        let dp0 = 0
            dp1 = score ! 1
            dp2 = score ! 1 + score ! 2
            go i dpIm1 dpIm2 dpIm3
              | i > n = dpIm1
              | otherwise =
                  let v = max dpIm2 (dpIm3 + score ! (i - 1)) + score ! i
                  in go (i + 1) v dpIm1 dpIm2
        print (go 3 dp2 dp1 dp0)