module Main (main) where

import Data.Char (isDigit)
import Data.List (isPrefixOf)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

readInt :: String -> Maybe Int
readInt s =
  let (sign, rest) = case s of
        ('-':r) -> (-1, r)
        _       -> (1, s)
  in if not (null rest) && all isDigit rest
       then Just (sign * read rest)
       else Nothing

main :: IO ()
main = do
  input <- getContents
  let ws = words (head (lines input ++ [""]))
      go [] = return ()
      go (w:rest) = case readInt w of
        Just n | n >= 1 -> do
          let moves = hanoi n 1 2 3
          putStrLn (show (length moves))
          mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) moves
        _ -> go rest
  go ws