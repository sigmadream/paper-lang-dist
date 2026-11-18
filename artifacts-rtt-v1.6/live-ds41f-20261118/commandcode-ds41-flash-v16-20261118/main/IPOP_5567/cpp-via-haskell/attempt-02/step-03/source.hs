module Main where

import qualified Data.IntMap.Strict as IM
import qualified Data.IntSet as IS
import Data.List (foldl')

pairUp :: [Int] -> [(Int, Int)]
pairUp (a:b:xs) = (a, b) : pairUp xs
pairUp _ = []

addEdge :: IM.IntMap [Int] -> (Int, Int) -> IM.IntMap [Int]
addEdge mp (a, b) =
    IM.insertWith (++) b [a] (IM.insertWith (++) a [b] mp)

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Int]
    case nums of
        (_n:_m:rest) -> do
            let adj = foldl' addEdge IM.empty (pairUp rest)
                nbrs1 = IS.fromList (IM.findWithDefault [] 1 adj)
                nbrs2 = IS.fromList
                    (concatMap (\v -> IM.findWithDefault [] v adj) (IS.toList nbrs1))
                ans = IS.size (IS.delete 1 (IS.union nbrs1 nbrs2))
            print ans
        _ -> return ()