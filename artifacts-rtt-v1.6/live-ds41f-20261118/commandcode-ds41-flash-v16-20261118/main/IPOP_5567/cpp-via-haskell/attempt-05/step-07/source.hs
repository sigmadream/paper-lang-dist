module Main where

import qualified Data.Set as Set

pairUp :: [Int] -> [(Int, Int)]
pairUp (a:b:xs) = (a, b) : pairUp xs
pairUp _ = []

main :: IO ()
main = do
  input <- getContents
  let vals = map read (words input) :: [Int]
  case vals of
    [] -> return ()
    (n:rest) ->
      if n <= 0
        then putStrLn "0"
        else do
          let (m, afterM) = case rest of
                              [] -> (0, [])
                              (x:xs) -> (x, xs)
              edges0 = pairUp (take (2 * max 0 m) afterM)
              edges = filter valid edges0
              valid (a, b) = a >= 1 && a <= n && b >= 1 && b <= n
              neighbors x =
                [b | (a, b) <- edges, a == x] ++
                [a | (a, b) <- edges, b == x]
              firstList = neighbors 1
              firstSet = Set.fromList firstList
              secondSet = Set.fromList (concatMap neighbors firstList)
              countSet =
                (firstSet `Set.union` secondSet)
                  `Set.difference` Set.singleton 1
          print (Set.size countSet)