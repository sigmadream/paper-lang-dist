module Main where

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (nStr:rest) ->
      let n = read nStr :: Int
          xs = take n (map read rest) :: [Int]
          nonZeros = filter (/= 0) xs
          zeros = filter (== 0) xs
      in putStrLn (unwords (map show (nonZeros ++ zeros)))