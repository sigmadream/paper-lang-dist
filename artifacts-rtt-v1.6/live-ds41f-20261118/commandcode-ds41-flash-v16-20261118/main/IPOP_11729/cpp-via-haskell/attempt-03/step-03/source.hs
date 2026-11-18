import qualified Data.ByteString.Builder as B
import Data.Bits (shiftL)
import System.IO

hanoi :: Int -> Int -> Int -> Int -> B.Builder
hanoi 1 s e = B.intDec s <> B.char8 ' ' <> B.intDec e <> B.char8 '\n'
hanoi n s m e =
  hanoi (n - 1) s e m
    <> B.intDec s <> B.char8 ' ' <> B.intDec e <> B.char8 '\n'
    <> hanoi (n - 1) m s e

main :: IO ()
main = do
  n <- readLn :: IO Int
  hSetBuffering stdout (BlockBuffering Nothing)
  let total = ((1 :: Int) `shiftL` n) - 1
  B.hPutBuilder stdout $
    B.intDec total <> B.char8 '\n' <> hanoi n 1 2 3