module Main (main) where

import qualified Data.IntSet as IS
import qualified Data.IntMap.Strict as IM
import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  let (nLine : rest) = lines inp
      n = read nLine :: Int
      (mLine : edgeLines) = rest
      m = read mLine :: Int
      edges = take m [ (a, b) | l <- edgeLines, let ws = map read (words l) :: [Int], (a:b:_) <- [ws] ]
      adj = foldl' add IM.empty edges
      add g (a, b) = IM.insertWith (++) a [b] (IM.insertWith (++) b [a] g)
      neighbors x = IM.findWithDefault [] x adj
      s1 = IS.fromList (neighbors 1)
      s2 = IS.unions [ IS.fromList (neighbors y) | y <- IS.toList s1 ]
      invited = IS.delete 1 (IS.union s1 s2)
  print (IS.size invited)