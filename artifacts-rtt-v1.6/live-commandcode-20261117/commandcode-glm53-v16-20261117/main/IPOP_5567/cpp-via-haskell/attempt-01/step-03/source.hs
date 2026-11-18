module Main (main) where

import qualified Data.Set as S
import qualified Data.IntMap.Strict as IM
import Data.List (foldl')

main :: IO ()
main = do
  contents <- getContents
  let (nStr : mStr : rest) = words contents
      n = read nStr :: Int
      m = read mStr :: Int
      edges = take m $ map (\(a:b:_) -> (read a, read b)) (chunk rest)
      adj = foldl' addEdge (IM.empty) edges
      addEdge g (a, b) = IM.insertWith (++) a [b] (IM.insertWith (++) b [a] g)
      neigh1 = IM.findWithDefault [] 1 adj
      invited = foldl' step S.empty neigh1
      step s y
        | y == 1 = s
        | otherwise = foldl' (\s' z -> if z == 1 then s' else S.insert z s')
                            (S.insert y s)
                            (IM.findWithDefault [] y adj)
  print (S.size invited)
  where
    chunk [] = []
    chunk (x:y:xs) = [x,y] : chunk xs
    chunk _ = []