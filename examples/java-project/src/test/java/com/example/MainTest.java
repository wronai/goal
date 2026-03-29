package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class MainTest {
    @Test
    public void testGreet() {
        Main main = new Main();
        assertEquals("Hello, World!", main.greet("World"));
    }
}
