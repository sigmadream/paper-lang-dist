module Main where

main :: IO ()
main = do
    input <- getContents
    case map (read :: String -> Integer) (words input) of
        (m:n:_) -> print (uniquePaths m n)
        _ -> return ()

uniquePaths :: Integer -> Integer -> Integer
uniquePaths m n =
    let initialRow = replicate (fromIntegral n) 1 :: [Integer]
        finalRow = iterate (scanl1 (+)) initialRow !! (fromIntegral (m - 1))
    in last finalRow