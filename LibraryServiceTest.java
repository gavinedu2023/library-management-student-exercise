package com.library.management;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class LibraryServiceTest {
    
    private LibraryService service;
    
    @BeforeEach
    void setUp() {
        service = new LibraryService();
        
        // Add test data
        service.addMember(new Member("member1", "John Doe", "john@example.com"));
        service.addBook(new Book("book1", "Java Programming", "Author Name"));
    }
    
    @Test
    void testBorrowBookSuccess() {
        String result = service.borrowBook("member1", "book1");
        assertTrue(result.contains("Book borrowed successfully"));
    }
    
    @Test
    void testBorrowBookMemberNotFound() {
        String result = service.borrowBook("invalid", "book1");
        assertEquals("Member not found", result);
    }
}


