module Main where

import qualified Data.Set as S
import Data.Array (Array, accumArray, (!))

parsePairs :: [Int] -> [(Int, Int)]
parsePairs (a:b:xs) = (a, b) : parsePairs xs
parsePairs _ = []

main :: IO ()
main = do
  contents <- getContents
  let tokens = words contents
  case tokens of
    [] -> return ()
    _ -> do
      let nums = map read tokens :: [Int]
      case nums of
        (n:m:rest) -> do
          let edges = parsePairs (take (2 * m) rest)
              adj :: Array Int [Int]
              adj = accumArray (\xs x -> x : xs) [] (1, n)
                      (concatMap (\(a, b) -> [(a, b), (b, a)]) edges)
              level1 = S.delete 1 (S.fromList (adj ! 1))
              neighbors = S.fromList (concatMap (\v -> adj ! v) (S.toList level1))
              level2 = neighbors `S.difference` (S.insert 1 level1)
              ans = S.size level1 + S.size level2
          print ans
        _ -> return ()