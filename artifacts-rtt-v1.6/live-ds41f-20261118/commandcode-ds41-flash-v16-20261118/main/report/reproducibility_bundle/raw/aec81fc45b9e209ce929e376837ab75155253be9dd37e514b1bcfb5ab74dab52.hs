module Main where

import Data.Array
import Data.List (nub)

main :: IO ()
main = do
    input <- getContents
    let ints = map read (words input) :: [Int]
    case ints of
        (n:m:rest) -> do
            let edgeList = pairUp (take (2 * m) rest)
                adj = accumArray (++) [] (1, n) $
                      concatMap (\(u, v) -> [(u, [v]), (v, [u])]) edgeList
                neighbors = adj ! 1
                candidates = [v | v <- neighbors, v /= 1] ++
                             [w | v <- neighbors, w <- adj ! v, w /= 1]
            print (length (nub candidates))
        _ -> return ()

pairUp :: [Int] -> [(Int, Int)]
pairUp (a:b:rest) = (a, b) : pairUp rest
pairUp _ = []