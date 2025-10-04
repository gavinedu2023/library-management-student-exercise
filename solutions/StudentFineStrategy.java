package com.library.management;

import java.util.Date;

/**
 * SOLUTION: Student Fine Calculation Strategy
 * 
 * This implements a reduced fine calculation for students:
 * - No fine for books returned within the loan period
 * - $0.25 per day for books returned after the loan period (50% discount)
 */
public class StudentFineStrategy implements FineCalculationStrategy {
    
    private static final double DAILY_FINE_RATE = 0.25; // 50% discount for students
    
    @Override
    public double calculateFine(Loan loan, int loanDurationDays) {
        if (loan == null || loan.getBorrowDate() == null) {
            return 0.0;
        }
        
        // Calculate days overdue
        long daysOverdue = calculateDaysOverdue(loan.getBorrowDate(), loanDurationDays);
        
        if (daysOverdue > 0) {
            return daysOverdue * DAILY_FINE_RATE;
        }
        
        return 0.0;
    }
    
    private long calculateDaysOverdue(Date borrowDate, int loanDurationDays) {
        long currentTime = new Date().getTime();
        long borrowTime = borrowDate.getTime();
        long loanDurationMillis = loanDurationDays * 24L * 60L * 60L * 1000L;
        
        long daysOverdue = (currentTime - borrowTime - loanDurationMillis) / (1000L * 60L * 60L * 24L);
        return Math.max(0, daysOverdue);
    }
}
