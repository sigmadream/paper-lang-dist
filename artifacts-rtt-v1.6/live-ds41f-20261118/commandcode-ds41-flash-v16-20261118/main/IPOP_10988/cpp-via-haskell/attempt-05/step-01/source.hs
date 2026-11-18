module Main where

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> pure ()
    (s:_) -> putStrLn $ if s == reverse s then "1" else "0"