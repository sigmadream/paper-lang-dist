module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (t:ts) ->
            let n = read t :: Integer
                k = fromIntegral (max 0 n) :: Int
                vals = map read (take k ts) :: [Integer]
            in if null vals
               then putStrLn "0"
               else print (solve vals)

solve :: [Integer] -> Integer
solve [] = 0
solve (x:xs) = snd (foldl' step (x, x) xs)
  where
    step (cur, best) y =
        let cur' = max y (cur + y)
            best' = max best cur'
        in (cur', best')