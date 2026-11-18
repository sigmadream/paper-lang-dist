module Main (main) where

import Data.Char (isDigit)

main :: IO ()
main = do
  inp <- getContents
  case words inp of
    (tok:_) | all isDigit tok && not (null tok) ->
      let n = read tok :: Integer
      in when' (n >= 0) $
           putStrLn (unwords (map (show . f) [0 .. n]))
    _ -> return ()
  where
    f 0 = 0
    f i = f (i `div` 2) + fromIntegral (i `mod` 2)
    when' c a = if c then a else return ()