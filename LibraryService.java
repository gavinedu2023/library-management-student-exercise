package com.library.management;

import java.util.*;

public class LibraryService {
    private List<Book> books = new ArrayList<>();
    private List<Member> members = new ArrayList<>();
    private List<Loan> loans = new ArrayList<>();
    
    public String borrowBook(String memberId, String bookId) {
        try {
            // Find member
            Member member = null;
            for (Member m : members) {
                if (m.getId().equals(memberId)) {
                    member = m;
                    break;
                }
            }
            
            if (member == null) {
                return "Member not found";
            }
            
            // Find book
            Book book = null;
            for (Book b : books) {
                if (b.getId().equals(bookId)) {
                    book = b;
                    break;
                }
            }
            
            if (book == null) {
                return "Book not found";
            }
            
            // Check if book is available
            if (!book.isAvailable()) {
                return "Book is not available";
            }
            
            // Create loan
            String loanId = UUID.randomUUID().toString();
            Loan loan = new Loan(loanId, memberId, bookId, new Date());
            loans.add(loan);
            
            // Update book status
            book.setAvailable(false);
            
            return "Book borrowed successfully. Loan ID: " + loanId;
            
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    public String returnBook(String loanId) {
        try {
            // Find loan
            Loan loan = null;
            for (Loan l : loans) {
                if (l.getId().equals(loanId)) {
                    loan = l;
                    break;
                }
            }
            
            if (loan == null) {
                return "Loan not found";
            }
            
            // Find book
            Book book = null;
            for (Book b : books) {
                if (b.getId().equals(loan.getBookId())) {
                    book = b;
                    break;
                }
            }
            
            if (book != null) {
                book.setAvailable(true);
            }
            
            // Remove loan
            loans.remove(loan);
            
            return "Book returned successfully";
            
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }
    
    public List<Book> getAvailableBooks() {
        List<Book> availableBooks = new ArrayList<>();
        for (Book book : books) {
            if (book.isAvailable()) {
                availableBooks.add(book);
            }
        }
        return availableBooks;
    }
    
    public List<Loan> getMemberLoans(String memberId) {
        List<Loan> memberLoans = new ArrayList<>();
        for (Loan loan : loans) {
            if (loan.getMemberId().equals(memberId)) {
                memberLoans.add(loan);
            }
        }
        return memberLoans;
    }
    
    public void addBook(Book book) {
        books.add(book);
    }
    
    public void addMember(Member member) {
        members.add(member);
    }
    
    public double calculateFine(String loanId) {
        Loan loan = null;
        for (Loan l : loans) {
            if (l.getId().equals(loanId)) {
                loan = l;
                break;
            }
        }
        
        if (loan == null) {
            return 0.0;
        }
        
        // Calculate days overdue
        long daysOverdue = (new Date().getTime() - loan.getBorrowDate().getTime()) / (1000 * 60 * 60 * 24);
        
        if (daysOverdue > 14) {
            return (daysOverdue - 14) * 0.50; // $0.50 per day after 14 days
        }
        
        return 0.0;
    }
}


