module Main where

main :: IO ()
main = do
    contents <- getContents
    case words contents of
        (s:_) -> putStrLn $ if s == reverse s then "1" else "0"
        [] -> return ()