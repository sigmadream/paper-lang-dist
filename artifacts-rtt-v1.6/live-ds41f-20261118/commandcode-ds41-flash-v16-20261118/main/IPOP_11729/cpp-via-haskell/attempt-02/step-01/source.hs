module Main where

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi n start mid end
  | n == 1 = [(start, end)]
  | otherwise =
      hanoi (n - 1) start end mid
        ++ [(start, end)]
        ++ hanoi (n - 1) mid start end

moveStr :: (Int, Int) -> String
moveStr (a, b) = show a ++ " " ++ show b ++ "\n"

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (x:_) -> do
      let n = read x :: Int
      putStr (show (2 ^ n - 1) ++ "\n")
      putStr (concatMap moveStr (hanoi n 1 2 3))