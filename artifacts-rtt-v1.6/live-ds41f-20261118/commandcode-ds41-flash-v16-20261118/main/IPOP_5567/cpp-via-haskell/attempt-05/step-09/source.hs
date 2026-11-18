module Main (main) where

import Control.Monad (unless)
import Data.Maybe (fromMaybe)
import Data.List (foldl')
import qualified Data.IntMap.Strict as IM
import qualified Data.Sequence as Seq
import Data.Sequence (ViewL(..), (|>))

main :: IO ()
main = do
    input <- getContents
    let vals = map read (words input) :: [Int]
    unless (null vals) $ do
        let n = head vals
        if n <= 0
            then putStrLn "0"
            else do
                let rest = tail vals
                    m = case rest of
                          [] -> 0
                          (x:_) -> x
                    rest2 = case rest of
                              [] -> []
                              (_:xs) -> xs
                    limit = max 0 m
                    pairs = takePairs limit rest2
                    adj = buildAdj n pairs
                    dist = bfs adj
                    ans = length [ v
                                 | v <- [2..n]
                                 , let d = fromMaybe (-1) (IM.lookup v dist)
                                 , d == 1 || d == 2
                                 ]
                print ans

takePairs :: Int -> [Int] -> [(Int, Int)]
takePairs k _ | k <= 0 = []
takePairs _ [] = []
takePairs _ [_] = []
takePairs k (a:b:xs) = (a, b) : takePairs (k - 1) xs

buildAdj :: Int -> [(Int, Int)] -> IM.IntMap [Int]
buildAdj n = foldl' add IM.empty
  where
    inRange x = x >= 1 && x <= n
    add adj (a, b)
      | inRange a && inRange b =
          IM.insertWith (++) b [a] (IM.insertWith (++) a [b] adj)
      | otherwise = adj

bfs :: IM.IntMap [Int] -> IM.IntMap Int
bfs adj = go (Seq.singleton 1) (IM.singleton 1 0)
  where
    go queue dist =
      case Seq.viewl queue of
        EmptyL -> dist
        u :< rest ->
          let du = fromMaybe 0 (IM.lookup u dist)
          in if du >= 2
               then go rest dist
               else
                 let neighbors = fromMaybe [] (IM.lookup u adj)
                     step (q, d) v
                       | IM.member v d = (q, d)
                       | otherwise = (q |> v, IM.insert v (du + 1) d)
                     (queue', dist') = foldl' step (rest, dist) neighbors
                 in go queue' dist'