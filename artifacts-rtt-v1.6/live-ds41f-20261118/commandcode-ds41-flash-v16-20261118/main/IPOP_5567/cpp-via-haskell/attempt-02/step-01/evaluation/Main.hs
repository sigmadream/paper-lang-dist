module Main where

import qualified Data.Map.Strict as M
import qualified Data.Set as S

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> pure ()
    (x : y : rest) -> do
      let m = read y :: Int

          pairs :: [String] -> [(Int, Int)]
          pairs [] = []
          pairs (a : b : xs) = (read a, read b) : pairs xs
          pairs _ = []

          edges = take m (pairs rest)

          addEdge mp (a, b) =
            M.insertWith (++) a [b] $
              M.insertWith (++) b [a] mp

          adj = foldl addEdge M.empty edges
          neighbors v = M.findWithDefault [] v adj

          dist1 = S.fromList (neighbors 1)
          dist2 = S.fromList
            [ w
            | v <- S.toList dist1
            , w <- neighbors v
            , w /= 1
            , not (S.member w dist1)
            ]

      print (S.size dist1 + S.size dist2)
    _ -> pure ()