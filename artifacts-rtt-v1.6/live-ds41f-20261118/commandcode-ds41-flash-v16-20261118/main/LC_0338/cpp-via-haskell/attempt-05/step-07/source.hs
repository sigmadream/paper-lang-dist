module Main where

import Data.Array (Array, listArray, (!))

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (w:_) ->
            let n = read w :: Int
                dp :: Array Int Int
                dp = listArray (0, n)
                    [ if i == 0 then 0 else dp ! (i `div` 2) + (i `mod` 2)
                    | i <- [0..n]
                    ]
            in putStrLn $ unwords [show (dp ! i) | i <- [0..n]]