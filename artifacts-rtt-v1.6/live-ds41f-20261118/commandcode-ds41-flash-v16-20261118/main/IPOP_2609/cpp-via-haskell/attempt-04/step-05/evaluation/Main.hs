module Main where

main :: IO ()
main = do
    input <- getContents
    let [a, b] = map read (words input) :: [Integer]
    print (gcd a b)
    print (lcm a b)