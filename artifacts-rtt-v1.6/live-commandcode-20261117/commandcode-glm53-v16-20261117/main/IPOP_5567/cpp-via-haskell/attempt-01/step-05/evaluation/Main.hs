module Main (main) where

import qualified Data.Set as S
import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  let (nStr : mStr : rest) = words inp
      _n = read nStr :: Int
      m = read mStr :: Int
      edges = take m (map (\(a:b:_) -> (a, b)) (map words (lines (unwords rest))))
  let adj v = [ b | (a, b) <- edges, a == v ] ++ [ a | (a, b) <- edges, b == v ]
      invited = foldl' (\s z -> if z /= 1 then S.insert z s else s)
                       (S.fromList [ y | y <- adj 1, y /= 1 ])
                       (concatMap adj [ y | y <- adj 1, y /= 1 ])
  print (S.size invited)