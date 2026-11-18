module Main (main) where

import Data.Char (ord)
import qualified Data.Map.Strict as M

main :: IO ()
main = do
  ms <- getLine
  case ms of
    Nothing -> return ()
    Just s -> do
      mt <- getLine
      let t = maybe "" id mt
      print (if counts s == counts t then 1 else 0 :: Int)

counts :: String -> M.Map Char Int
counts = foldr (\c m -> M.insertWith (+) c 1 m) M.empty