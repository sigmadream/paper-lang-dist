module Main (main) where

import System.IO
import Data.Maybe (listToMaybe)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
  eof <- isEOF
  if eof
    then return ()
    else do
      line <- getLine
      case listToMaybe (mapMaybe readMaybeInt (words line)) of
        Nothing -> return ()
        Just n
          | n < 1 -> return ()
          | otherwise -> do
              let moves = hanoi n 1 2 3
              putStrLn (show (length moves))
              mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) moves
  where
    readMaybeInt w = case reads w :: [(Int, String)] of
      [(v, "")] -> Just v
      _ -> Nothing
    mapMaybe f = foldr (\x acc -> case f x of Just v -> v : acc; Nothing -> acc) []