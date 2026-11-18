module Main (main) where

import Data.Char (isDigit)
import System.IO

main :: IO ()
main = do
  mline <- getLine
  case mline of
    [] -> return ()
    _ -> do
      let ws = words mline
      case ws of
        [] -> return ()
        (w:_) ->
          case readInt w of
            Nothing -> return ()
            Just n | n < 0 -> return ()
                   | otherwise -> do
                       let res = 0 : [ (res !! (i `div` 2)) + (i `mod` 2)
                                     | i <- [1 .. n] ]
                       putStrLn (unwords (map show (take (fromIntegral n + 1) res)))

readInt :: String -> Maybe Integer
readInt ('-':ds) | all isDigit ds && not (null ds) = Just (negate (read ds))
readInt ds | all isDigit ds && not (null ds) = Just (read ds)
readInt _ = Nothing