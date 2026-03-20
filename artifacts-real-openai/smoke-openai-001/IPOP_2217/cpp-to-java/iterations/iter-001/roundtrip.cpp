    int read() {
        if (ptr >= len) {
            in.read(buffer, BUFSIZE);
            len = (int)in.gcount();
            ptr = 0;
            if (len <= 0) return -1;
        }
        return buffer[ptr++];
    }
