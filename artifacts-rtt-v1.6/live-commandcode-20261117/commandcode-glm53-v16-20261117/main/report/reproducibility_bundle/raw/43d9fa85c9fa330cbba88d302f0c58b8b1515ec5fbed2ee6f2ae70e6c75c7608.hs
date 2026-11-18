module Main (main) where

import Data.List (intercalate)
import qualified Data.ByteString.Char8 as BS

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
  contents <- BS.getContents
  let ns = map fst (map (BS.readInt . BS.dropWhile (== ' ')) (BS.lines contents))
  case filter (>= 1) [n | Just n <- ns] of
    (n:_) -> do
      let moves = hanoi n 1 2 3
      putStrLn (show (length moves))
      mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) moves
    [] -> return ()