module Main where

main :: IO ()
main = do
    contents <- getContents
    let ws = words contents
    case ws of
        (nStr : rest) ->
            case reads nStr of
                [(n, "")] ->
                    let nums = take n (map read rest) :: [Int]
                    in if length nums == n
                       then putStrLn $ unwords $ map show (filter (/= 0) nums ++ filter (== 0) nums)
                       else pure ()
                _ -> pure ()
        _ -> pure ()