module Main where

import qualified Data.IntMap.Strict as IM
import qualified Data.IntSet as IS
import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let xs = map read (words input) :: [Int]
    case xs of
        (n : m : rest) -> do
            let edges = take m (toPairs rest)
                adj = foldl' addEdge IM.empty edges
                neighbors v = IM.findWithDefault [] v adj

                layer1 = IS.fromList [v | v <- neighbors 1, v /= 1]
                visited1 = IS.insert 1 layer1
                layer2 = IS.fromList
                    [ w
                    | v <- IS.toList layer1
                    , w <- neighbors v
                    , not (IS.member w visited1)
                    ]

                answer = IS.size (IS.union layer1 layer2)
            putStrLn (show answer)
        _ -> return ()

toPairs :: [Int] -> [(Int, Int)]
toPairs (a : b : rest) = (a, b) : toPairs rest
toPairs _ = []

addEdge :: IM.IntMap [Int] -> (Int, Int) -> IM.IntMap [Int]
addEdge adj (a, b) =
    IM.insertWith (++) b [a] $
    IM.insertWith (++) a [b] adj