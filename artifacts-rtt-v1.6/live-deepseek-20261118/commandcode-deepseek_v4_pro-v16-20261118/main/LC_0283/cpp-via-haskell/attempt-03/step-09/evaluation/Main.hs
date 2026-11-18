module Main where

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (nStr:rest) -> case reads nStr of
      [(n, "")] -> let nums = map read (take n rest)
                       nonZeros = filter (/= 0) nums
                       zeros = filter (== 0) nums
                   in putStrLn (unwords (map show (nonZeros ++ zeros)))
      _ -> return ()