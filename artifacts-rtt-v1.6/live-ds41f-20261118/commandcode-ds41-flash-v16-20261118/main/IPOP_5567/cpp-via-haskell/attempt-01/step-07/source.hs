module Main where

import qualified Data.Set as Set
import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Int]
    case nums of
        (n:m:rest) ->
            if n <= 0
                then putStrLn "0"
                else do
                    let edges = take m rest
                    let adj = buildAdj n edges
                    let d1 = Set.fromList (adj !! 0)
                    let d2 = Set.fromList
                            [ w
                            | v <- Set.toList d1
                            , w <- adj !! v
                            , w /= 0
                            , not (Set.member w d1)
                            ]
                    print (Set.size d1 + Set.size d2)
        _ -> return ()

buildAdj :: Int -> [Int] -> [[Int]]
buildAdj n xs = go (replicate n []) xs
  where
    go adj (a:b:rest) =
        let a' = a - 1
            b' = b - 1
            adj1 = update adj a' b'
            adj2 = update adj1 b' a'
        in go adj2 rest
    go adj _ = adj

    update adj i v =
        [ if j == i then v : adj !! j else adj !! j
        | j <- [0 .. length adj - 1]
        ]