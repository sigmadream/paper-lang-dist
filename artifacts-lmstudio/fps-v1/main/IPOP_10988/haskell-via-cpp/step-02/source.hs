module Main where

main :: IO ()
main = do
    s <- getLine
    putStrLn $ if isPalindrome s then "1" else "0"

isPalindrome :: String -> Bool
isPalindrome s = s == reverse s