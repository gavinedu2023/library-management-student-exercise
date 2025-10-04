package com.library.management;

/**
 * SOLUTION: Result class for borrow operations
 * 
 * This class provides better error handling and result communication
 */
public class BorrowResult {
    private final boolean success;
    private final String message;
    private final Loan loan;
    
    private BorrowResult(boolean success, String message, Loan loan) {
        this.success = success;
        this.message = message;
        this.loan = loan;
    }
    
    public static BorrowResult success(Loan loan) {
        return new BorrowResult(true, "Book borrowed successfully", loan);
    }
    
    public static BorrowResult failure(String message) {
        return new BorrowResult(false, message, null);
    }
    
    public boolean isSuccess() { return success; }
    public String getMessage() { return message; }
    public Loan getLoan() { return loan; }
}
