module Main where

import Text.Read (readMaybe)

hanoiIO :: Int -> Int -> Int -> Int -> IO ()
hanoiIO n from mid to
  | n == 1 = putStrLn (show from ++ " " ++ show to)
  | otherwise = do
      hanoiIO (n - 1) from to mid
      putStrLn (show from ++ " " ++ show to)
      hanoiIO (n - 1) mid from to

main :: IO ()
main = do
  contents <- getContents
  let firstWord = case words contents of
        w : _ -> w
        [] -> ""
  case readMaybe firstWord :: Maybe Int of
    Just n | n >= 1 && n <= 20 -> do
      putStrLn (show (2 ^ n - 1 :: Integer))
      hanoiIO n 1 2 3
    _ -> pure ()