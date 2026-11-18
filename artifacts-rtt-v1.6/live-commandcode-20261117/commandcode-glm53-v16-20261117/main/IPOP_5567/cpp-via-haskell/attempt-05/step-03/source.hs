module Main (main) where

import qualified Data.Set as S
import Data.List (foldl')
import Data.Maybe (fromMaybe)
import qualified Data.Map as M
import Data.Char (isDigit, isSpace)

main :: IO ()
main = do
  inp <- getContents
  let nums = map readInt (words inp)
      (n : m : rest) = nums
      edges = pairs rest
      adj = buildAdj edges
      d1 = S.delete 1 (S.fromList [ v | (a, b) <- edges, v <- [a, b], a == 1 || b == 1 ])
      d2 = S.delete 1 (S.fromList [ w
                                  | v <- S.toList d1
                                  , Just ws <- [M.lookup v adj]
                                  , w <- ws ])
      ans = S.size (S.union d1 d2)
  print ans

readInt :: String -> Int
readInt s = case dropWhile isSpace s of
  '-':rest -> negate (readDigit rest)
  rest -> readDigit rest
  where readDigit = read . takeWhile isDigit

pairs :: [Int] -> [(Int, Int)]
pairs (a:b:xs) = (a, b) : pairs xs
pairs _ = []

buildAdj :: [(Int, Int)] -> M.Map Int [Int]
buildAdj = foldl' ins M.empty
  where
    ins m (a, b) = M.insertWith (++) b [a] (M.insertWith (++) a [b] m)