import Data.List (partition)

main :: IO ()
main = do
    content <- getContents
    case words content of
        [] -> return ()
        (_:rest) -> do
            let (nonzeros, zeros) = partition (/= "0") rest
            putStrLn $ unwords (nonzeros ++ zeros)
