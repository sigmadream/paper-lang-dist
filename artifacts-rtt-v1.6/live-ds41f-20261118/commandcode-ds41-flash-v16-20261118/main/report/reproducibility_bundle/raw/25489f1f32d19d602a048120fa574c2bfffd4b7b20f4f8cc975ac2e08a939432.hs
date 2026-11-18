module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (nStr : rest) -> do
            let n = read nStr :: Int
                xs = take (max 0 n) (map (read :: String -> Integer) rest)
            case xs of
                [] -> return ()
                (x0 : xs') -> do
                    let step (cur, best) x =
                            let cur' = max x (cur + x)
                                best' = max best cur'
                            in (cur', best')
                        (_, answer) = foldl' step (x0, x0) xs'
                    print answer