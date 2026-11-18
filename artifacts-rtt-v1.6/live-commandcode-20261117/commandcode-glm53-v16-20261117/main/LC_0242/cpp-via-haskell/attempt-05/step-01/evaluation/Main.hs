module Main (main) where

import Data.List (foldl')
import qualified Data.Map.Strict as M
import Data.Char (ord)

countChars :: String -> M.Map Int Int
countChars = foldl' (\m c -> M.insertWith (+) (ord c - ord 'a') 1 m) M.empty

main :: IO ()
main = do
  s <- getLine
  t <- getLine
  let ok
        | length s /= length t = False
        | otherwise = M.null (M.unionWith (-) (countChars s) (countChars t))
          || all (== 0) (M.elems (M.unionWith (-) (countChars s) (countChars t)))
  putStrLn (if ok then "1" else "0")