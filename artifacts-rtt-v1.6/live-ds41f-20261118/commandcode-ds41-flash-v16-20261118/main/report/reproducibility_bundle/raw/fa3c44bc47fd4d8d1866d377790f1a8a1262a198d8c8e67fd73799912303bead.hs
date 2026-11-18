module Main where

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (s:_) -> putStrLn (if s == reverse s then "1" else "0")