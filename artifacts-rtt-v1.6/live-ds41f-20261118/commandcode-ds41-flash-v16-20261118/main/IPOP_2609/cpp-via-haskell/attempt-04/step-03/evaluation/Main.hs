module Main where

main :: IO ()
main = do
    input <- getContents
    let [a, b] = map read (words input) :: [Integer]
        g = gcd a b
    print g
    print ((a `div` g) * b)