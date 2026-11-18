module Main where

import Text.Read (readMaybe)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi n start mid end
  | n == 1    = [(start, end)]
  | otherwise = hanoi (n - 1) start end mid
                ++ [(start, end)]
                ++ hanoi (n - 1) mid start end

main :: IO ()
main = do
    input <- getContents
    case words input of
        (nStr : _) ->
            case readMaybe nStr of
                Just n | n >= 1 && n <= 20 -> do
                    let moves = hanoi n 1 2 3
                    putStrLn (show (length moves))
                    mapM_ (\(from, to) -> putStrLn (show from ++ " " ++ show to)) moves
                _ -> pure ()
        [] -> pure ()