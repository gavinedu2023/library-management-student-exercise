package com.library.management;

import java.util.List;

/**
 * SOLUTION: Repository Pattern Interface for Loans
 */
public interface LoanRepository {
    void save(Loan loan);
    Loan findById(String id);
    void update(Loan loan);
    void delete(String id);
    List<Loan> findAll();
    List<Loan> findByMemberId(String memberId);
}
