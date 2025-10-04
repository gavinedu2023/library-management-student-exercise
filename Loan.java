package com.library.management;

import java.util.Date;

public class Loan {
    private String id;
    private String memberId;
    private String bookId;
    private Date borrowDate;
    
    public Loan(String id, String memberId, String bookId, Date borrowDate) {
        this.id = id;
        this.memberId = memberId;
        this.bookId = bookId;
        this.borrowDate = borrowDate;
    }
    
    // Getters
    public String getId() { return id; }
    public String getMemberId() { return memberId; }
    public String getBookId() { return bookId; }
    public Date getBorrowDate() { return borrowDate; }
}
