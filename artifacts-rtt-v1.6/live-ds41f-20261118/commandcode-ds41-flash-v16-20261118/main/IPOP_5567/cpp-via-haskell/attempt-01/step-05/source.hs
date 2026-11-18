{-# OPTIONS_GHC -O2 #-}
module Main where

import Data.Array
import qualified Data.Set as Set

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (nStr : mStr : rest) -> do
            let n = read nStr :: Int
                m = read mStr :: Int
            if n <= 0
                then putStrLn "0"
                else do
                    let edgeVals = map read (take (2 * m) rest) :: [Int]
                        es = pairUp edgeVals
                        adj = accumArray (flip (:)) [] (0, n - 1)
                                (concatMap (\(a, b) -> [(a - 1, b - 1), (b - 1, a - 1)]) es)
                        d1 = Set.fromList (adj ! 0)
                        d2 = Set.fromList
                                [ w
                                | v <- Set.toList d1
                                , w <- adj ! v
                                , w /= 0
                                , not (Set.member w d1)
                                ]
                        answer = Set.size d1 + Set.size d2
                    putStrLn (show answer)
        _ -> return ()

pairUp :: [Int] -> [(Int, Int)]
pairUp (a : b : xs) = (a, b) : pairUp xs
pairUp _ = []