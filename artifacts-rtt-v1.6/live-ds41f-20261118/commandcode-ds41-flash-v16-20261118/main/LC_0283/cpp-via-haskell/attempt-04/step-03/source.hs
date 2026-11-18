module Main where

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (nStr : rest) -> do
      let n = read nStr :: Int
          xs = take n (map read rest :: [Int])
          nonZeros = filter (/= 0) xs
          zeroCount = length (filter (== 0) xs)
          result = nonZeros ++ replicate zeroCount 0
      putStrLn (unwords (map show result))