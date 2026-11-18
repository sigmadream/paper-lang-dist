module Main (main) where

import Data.List (foldl')
import Text.Read (readMaybe)

parseInt :: String -> Maybe Int
parseInt s = readMaybe s

main :: IO ()
main = do
    input <- getContents
    let toks = words input
    case toks of
        [] -> return ()
        (t0 : rest) ->
            case parseInt t0 of
                Nothing -> return ()
                Just n -> do
                    let intMax = 2147483647 :: Int
                        k | n <= 0 = 0
                          | n > intMax = intMax
                          | otherwise = n
                        takeParsed _ 0 = []
                        takeParsed [] _ = []
                        takeParsed (x:xs) m =
                            case parseInt x of
                                Just v -> v : takeParsed xs (m - 1)
                                Nothing -> []
                        nums = takeParsed rest k
                    case nums of
                        [] -> putStrLn "0"
                        (x:xs) -> putStrLn (show (maxSubarray x xs))

maxSubarray :: Int -> [Int] -> Int
maxSubarray x xs =
    let (_, best) = foldl' step (x, x) xs
    in best
  where
    step (cur, best) v =
        let cur' = max v (cur + v)
            best' = max best cur'
        in cur' `seq` best' `seq` (cur', best')