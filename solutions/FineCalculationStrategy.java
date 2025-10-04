package com.library.management;

/**
 * SOLUTION: Strategy Pattern Interface for Fine Calculation
 * 
 * This interface allows different fine calculation algorithms to be plugged in.
 * Benefits:
 * 1. Makes fine calculation algorithms interchangeable
 * 2. Easy to add new fine strategies (student discounts, member benefits)
 * 3. Improves testability by allowing mock implementations
 * 4. Follows Open/Closed Principle - open for extension, closed for modification
 */
public interface FineCalculationStrategy {
    double calculateFine(Loan loan, int loanDurationDays);
}
