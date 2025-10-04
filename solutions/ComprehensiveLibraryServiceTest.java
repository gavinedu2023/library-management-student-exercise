package com.library.management;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * SOLUTION: Comprehensive Test Suite
 * 
 * This test file addresses the original code's lack of test coverage by providing:
 * 1. DEBUG TESTS: Tests for all the bugs found in the original code
 * 2. INTEGRATION TESTS: End-to-end borrowing and returning flow
 * 3. EDGE CASE TESTS: Boundary conditions and error scenarios
 * 4. BUSINESS LOGIC TESTS: Borrowing limits and business rules
 */
@ExtendWith(MockitoExtension.class)
public class ComprehensiveLibraryServiceTest {
    
    @Mock private BookRepository mockBookRepository;
    @Mock private MemberRepository mockMemberRepository;
    @Mock private LoanRepository mockLoanRepository;
    @Mock private FineCalculationStrategy mockFineStrategy;
    
    private ImprovedLibraryService service;
    private Book testBook;
    private Member testMember;
    
    @BeforeEach
    void setUp() {
        service = new ImprovedLibraryService(
            mockBookRepository, mockMemberRepository, 
            mockLoanRepository, mockFineStrategy
        );
        
        // Setup test data
        testBook = new Book("book1", "Java Programming", "Author Name");
        testMember = new Member("member1", "John Doe", "john@example.com");
    }
    
    // SOLUTION: Unit Tests - Individual Method Testing
    // These tests verify that each method works correctly in isolation
    
    @Test
    void testBorrowBookSuccess() {
        // SOLUTION: Test successful borrowing scenario
        // This verifies the happy path works correctly
        when(mockMemberRepository.findById("member1")).thenReturn(testMember);
        when(mockBookRepository.findById("book1")).thenReturn(testBook);
        when(mockLoanRepository.findByMemberId("member1")).thenReturn(new ArrayList<>());
        
        BorrowResult result = service.borrowBook("member1", "book1");
        
        assertTrue(result.isSuccess());
        assertNotNull(result.getLoan());
        verify(mockLoanRepository).save(any(Loan.class));
        verify(mockBookRepository).update(testBook);
    }
    
    @Test
    void testBorrowBookMemberNotFound() {
        // SOLUTION: Test input validation - member not found
        // This tests the validation fix from the original code
        when(mockMemberRepository.findById("invalid")).thenReturn(null);
        
        BorrowResult result = service.borrowBook("invalid", "book1");
        
        assertFalse(result.isSuccess());
        assertEquals("Member not found", result.getMessage());
    }
    
    @Test
    void testBorrowBookBookNotFound() {
        // SOLUTION: Test input validation - book not found
        when(mockMemberRepository.findById("member1")).thenReturn(testMember);
        when(mockBookRepository.findById("invalid")).thenReturn(null);
        
        BorrowResult result = service.borrowBook("member1", "invalid");
        
        assertFalse(result.isSuccess());
        assertEquals("Book not found", result.getMessage());
    }
    
    @Test
    void testBorrowBookNotAvailable() {
        // SOLUTION: Test business logic - book not available
        testBook.setAvailable(false);
        when(mockMemberRepository.findById("member1")).thenReturn(testMember);
        when(mockBookRepository.findById("book1")).thenReturn(testBook);
        
        BorrowResult result = service.borrowBook("member1", "book1");
        
        assertFalse(result.isSuccess());
        assertEquals("Book is not available", result.getMessage());
    }
    
    @Test
    void testBorrowBookExceedsLimit() {
        // SOLUTION: Test business rule - borrowing limit
        // This tests the new business rule that wasn't in the original code
        when(mockMemberRepository.findById("member1")).thenReturn(testMember);
        when(mockBookRepository.findById("book1")).thenReturn(testBook);
        
        // Mock member already has 5 books (maximum limit)
        List<Loan> existingLoans = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            existingLoans.add(new Loan("loan" + i, "member1", "book" + i, new Date()));
        }
        when(mockLoanRepository.findByMemberId("member1")).thenReturn(existingLoans);
        
        BorrowResult result = service.borrowBook("member1", "book1");
        
        assertFalse(result.isSuccess());
        assertTrue(result.getMessage().contains("maximum borrowing limit"));
    }
    
    @Test
    void testBorrowBookNullInputs() {
        // SOLUTION: Test input validation - null inputs
        // This tests the validation fix from the original code
        BorrowResult result1 = service.borrowBook(null, "book1");
        assertFalse(result1.isSuccess());
        assertEquals("Member ID cannot be null or empty", result1.getMessage());
        
        BorrowResult result2 = service.borrowBook("member1", null);
        assertFalse(result2.isSuccess());
        assertEquals("Book ID cannot be null or empty", result2.getMessage());
    }
    
    @Test
    void testBorrowBookEmptyInputs() {
        // SOLUTION: Test input validation - empty inputs
        BorrowResult result1 = service.borrowBook("", "book1");
        assertFalse(result1.isSuccess());
        assertEquals("Member ID cannot be null or empty", result1.getMessage());
        
        BorrowResult result2 = service.borrowBook("member1", "");
        assertFalse(result2.isSuccess());
        assertEquals("Book ID cannot be null or empty", result2.getMessage());
    }
    
    // SOLUTION: Integration Tests - End-to-End Scenarios
    // These tests verify that multiple methods work together correctly
    
    @Test
    void testCompleteBorrowReturnFlow() {
        // SOLUTION: Test complete borrowing and returning flow
        // This verifies the integration between borrow and return methods
        when(mockMemberRepository.findById("member1")).thenReturn(testMember);
        when(mockBookRepository.findById("book1")).thenReturn(testBook);
        when(mockLoanRepository.findByMemberId("member1")).thenReturn(new ArrayList<>());
        
        // Borrow book
        BorrowResult borrowResult = service.borrowBook("member1", "book1");
        assertTrue(borrowResult.isSuccess());
        
        // Return book
        Loan loan = borrowResult.getLoan();
        when(mockLoanRepository.findById(loan.getId())).thenReturn(loan);
        when(mockBookRepository.findById("book1")).thenReturn(testBook);
        
        ReturnResult returnResult = service.returnBook(loan.getId());
        assertTrue(returnResult.isSuccess());
        
        verify(mockLoanRepository).delete(loan.getId());
        verify(mockBookRepository).update(testBook);
    }
    
    @Test
    void testGetAvailableBooks() {
        // SOLUTION: Test get available books method
        List<Book> allBooks = Arrays.asList(
            new Book("book1", "Title 1", "Author 1"),
            new Book("book2", "Title 2", "Author 2")
        );
        allBooks.get(1).setAvailable(false); // Make second book unavailable
        
        when(mockBookRepository.findAll()).thenReturn(allBooks);
        
        List<Book> availableBooks = service.getAvailableBooks();
        
        assertEquals(1, availableBooks.size());
        assertEquals("book1", availableBooks.get(0).getId());
    }
    
    @Test
    void testGetMemberLoans() {
        // SOLUTION: Test get member loans method
        List<Loan> memberLoans = Arrays.asList(
            new Loan("loan1", "member1", "book1", new Date()),
            new Loan("loan2", "member1", "book2", new Date())
        );
        
        when(mockLoanRepository.findByMemberId("member1")).thenReturn(memberLoans);
        
        List<Loan> result = service.getMemberLoans("member1");
        
        assertEquals(2, result.size());
        assertEquals("loan1", result.get(0).getId());
        assertEquals("loan2", result.get(1).getId());
    }
    
    // SOLUTION: Edge Case Tests - Boundary Conditions
    // These tests verify behavior at the boundaries of valid inputs
    
    @Test
    void testGetMemberLoansNullInput() {
        // SOLUTION: Test null input handling
        List<Loan> result = service.getMemberLoans(null);
        assertTrue(result.isEmpty());
    }
    
    @Test
    void testGetMemberLoansEmptyInput() {
        // SOLUTION: Test empty input handling
        List<Loan> result = service.getMemberLoans("");
        assertTrue(result.isEmpty());
    }
    
    @Test
    void testCalculateFineNullInput() {
        // SOLUTION: Test null input handling
        double fine = service.calculateFine(null);
        assertEquals(0.0, fine);
    }
    
    @Test
    void testCalculateFineEmptyInput() {
        // SOLUTION: Test empty input handling
        double fine = service.calculateFine("");
        assertEquals(0.0, fine);
    }
    
    @Test
    void testCalculateFineLoanNotFound() {
        // SOLUTION: Test loan not found scenario
        when(mockLoanRepository.findById("invalid")).thenReturn(null);
        
        double fine = service.calculateFine("invalid");
        assertEquals(0.0, fine);
    }
    
    @Test
    void testCalculateFineWithStrategy() {
        // SOLUTION: Test fine calculation with strategy pattern
        Loan loan = new Loan("loan1", "member1", "book1", new Date());
        when(mockLoanRepository.findById("loan1")).thenReturn(loan);
        when(mockFineStrategy.calculateFine(loan, 14)).thenReturn(5.0);
        
        double fine = service.calculateFine("loan1");
        assertEquals(5.0, fine);
        verify(mockFineStrategy).calculateFine(loan, 14);
    }
    
    // SOLUTION: Business Logic Tests - Business Rules
    // These tests verify that business rules are enforced correctly
    
    @Test
    void testAddBookValidation() {
        // SOLUTION: Test add book with validation
        assertTrue(service.addBook(testBook));
        verify(mockBookRepository).save(testBook);
    }
    
    @Test
    void testAddBookNullBook() {
        // SOLUTION: Test add book with null input
        assertFalse(service.addBook(null));
    }
    
    @Test
    void testAddBookNullId() {
        // SOLUTION: Test add book with null ID
        Book bookWithNullId = new Book(null, "Title", "Author");
        assertFalse(service.addBook(bookWithNullId));
    }
    
    @Test
    void testAddMemberValidation() {
        // SOLUTION: Test add member with validation
        assertTrue(service.addMember(testMember));
        verify(mockMemberRepository).save(testMember);
    }
    
    @Test
    void testAddMemberNullMember() {
        // SOLUTION: Test add member with null input
        assertFalse(service.addMember(null));
    }
    
    @Test
    void testAddMemberNullId() {
        // SOLUTION: Test add member with null ID
        Member memberWithNullId = new Member(null, "Name", "email@example.com");
        assertFalse(service.addMember(memberWithNullId));
    }
    
    // SOLUTION: Error Handling Tests - Exception Scenarios
    // These tests verify that exceptions are handled gracefully
    
    @Test
    void testBorrowBookRepositoryException() {
        // SOLUTION: Test exception handling in borrow book
        when(mockMemberRepository.findById("member1")).thenThrow(new RuntimeException("Database error"));
        
        BorrowResult result = service.borrowBook("member1", "book1");
        
        assertFalse(result.isSuccess());
        assertTrue(result.getMessage().contains("Failed to borrow book"));
    }
    
    @Test
    void testReturnBookRepositoryException() {
        // SOLUTION: Test exception handling in return book
        when(mockLoanRepository.findById("loan1")).thenThrow(new RuntimeException("Database error"));
        
        ReturnResult result = service.returnBook("loan1");
        
        assertFalse(result.isSuccess());
        assertTrue(result.getMessage().contains("Failed to return book"));
    }
    
    @Test
    void testGetAvailableBooksException() {
        // SOLUTION: Test exception handling in get available books
        when(mockBookRepository.findAll()).thenThrow(new RuntimeException("Database error"));
        
        List<Book> result = service.getAvailableBooks();
        
        assertTrue(result.isEmpty());
    }
}
