module Main where

import qualified Data.IntMap.Strict as IM
import qualified Data.IntSet as IS

main :: IO ()
main = do
  s <- getContents
  let xs = map read (words s) :: [Int]
  case xs of
    [] -> return ()
    (n:ys) ->
      if n <= 0
        then putStrLn "0"
        else do
          let (m, zs) = case ys of
                          (a:as) -> (a, as)
                          [] -> (0, [])
              limit = max 0 m
              tokens = take (2 * limit) zs
              edges = pairs tokens
              adj = foldl (addEdge n) IM.empty edges
              l0 = IS.singleton 1
              l1 = IS.fromList [v | v <- IM.findWithDefault [] 1 adj, v /= 1]
              addSecond acc u =
                foldl
                  (\s v -> if IS.member v l0 || IS.member v l1 then s else IS.insert v s)
                  acc
                  (IM.findWithDefault [] u adj)
              l2 = foldl addSecond IS.empty (IS.toList l1)
              ans = IS.size (IS.union l1 l2)
          print ans
  where
    pairs (a:b:rest) = (a, b) : pairs rest
    pairs _ = []

    addEdge n mp (a, b)
      | a >= 1 && a <= n && b >= 1 && b <= n =
          IM.insertWith (++) b [a] (IM.insertWith (++) a [b] mp)
      | otherwise = mp