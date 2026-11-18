module Main (main) where

import Data.List (intercalate)
import System.IO

main :: IO ()
main = do
  inp <- getContents
  case words inp of
    (nStr:rest) -> do
      let ns = map read (take (read nStr :: Int) rest) :: [Integer]
          nonZeros = filter (/= 0) ns
          zeros = filter (== 0) ns
      putStrLn (unwords (map show (nonZeros ++ zeros)))
    _ -> return ()