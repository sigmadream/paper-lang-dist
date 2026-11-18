module Main where

main :: IO ()
main = do
    input <- getLine
    let [a, b] = map read (words input) :: [Integer]
        g = gcd a b
    putStrLn (show g)
    putStrLn (show ((a `div` g) * b))