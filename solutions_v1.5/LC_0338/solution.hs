import Data.Bits ((.&.), shiftR)

popcount :: Int -> Int
popcount 0 = 0
popcount x = (x .&. 1) + popcount (x `shiftR` 1)

main :: IO ()
main = do
    content <- getContents
    case words content of
        [] -> return ()
        (s:_) -> do
            let n = read s :: Int
            let res = unwords [show (popcount i) | i <- [0..n]]
            putStrLn res
