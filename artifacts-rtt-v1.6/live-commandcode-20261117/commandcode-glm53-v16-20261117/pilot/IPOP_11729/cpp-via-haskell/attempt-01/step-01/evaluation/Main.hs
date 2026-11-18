module Main (main) where

import Data.Bits (shiftL)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s m' e
  where m' = s

main :: IO ()
main = do
  inp <- getContents
  let ls = lines inp
  case ls of
        (l0:_) | [(n, _)] <- reads l0 -> do
          let moves = hanoi n 1 2 3
          putStrLn (show (length moves))
          mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) moves
        _ -> return ()