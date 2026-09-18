import Data.List

isPalindrome :: String -> Bool
isPalindrome s = s == reverse s

main :: IO ()
main = do
  word <- getLine
  if isPalindrome word then putStrLn "1" else putStrLn "0"