module Main (main) where

import qualified Data.Set as S
import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  let (nLine : rest) = lines inp
      n = read nLine :: Int
      mLine : edgeLines = rest
      m = read mLine :: Int
      es = take m [ (a, b) | l <- edgeLines
                           , let ws = map read (words l) :: [Int]
                           , length ws >= 2
                           , let a = ws !! 0
                                 b = ws !! 1 ]
      adj v = [ b | (a, b) <- es, a == v ] ++ [ a | (a, b) <- es, b == v ]
      d1 = S.delete 1 $ S.fromList
             ([ b | (a, b) <- es, a == 1 ] ++ [ a | (a, b) <- es, b == 1 ])
      d2 = S.delete 1 $ S.fromList (concatMap adj (S.toList d1))
      ans = S.union d1 d2
  print (S.size ans)