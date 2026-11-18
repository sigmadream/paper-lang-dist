module Main where

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
      n = read (head tokens) :: Int
      xs = take n (map read (tail tokens) :: [Int])
      nonZeros = filter (/= 0) xs
      result = nonZeros ++ replicate (n - length nonZeros) 0
  putStrLn (unwords (map show result))