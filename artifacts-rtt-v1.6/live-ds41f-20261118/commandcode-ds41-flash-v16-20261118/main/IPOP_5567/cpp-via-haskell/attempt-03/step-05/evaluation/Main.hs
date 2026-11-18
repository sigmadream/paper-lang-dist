module Main where

import Data.Array
import qualified Data.Set as Set

main :: IO ()
main = do
    input <- getContents
    let xs = map read (words input) :: [Int]
    case xs of
        (n : m : rest) -> do
            let pairs [] = []
                pairs (a : b : more) = (a, b) : pairs more
                pairs _ = []
                edges = take m (pairs rest)
                adj = accumArray (flip (:)) [] (1, n)
                        (concatMap (\(a, b) -> [(a, b), (b, a)]) edges)
                friends = Set.fromList (adj ! 1)
                withinTwo = Set.unions
                    (friends : [Set.fromList (adj ! v) | v <- Set.toList friends])
                answer = Set.size (Set.delete 1 withinTwo)
            print answer
        _ -> return ()