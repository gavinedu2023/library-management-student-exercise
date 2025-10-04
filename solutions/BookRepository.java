package com.library.management;

import java.util.List;

/**
 * SOLUTION: Repository Pattern Interface
 * 
 * This interface abstracts data access operations for books.
 * Benefits:
 * 1. Separates business logic from data storage
 * 2. Makes testing easier with mock implementations
 * 3. Allows switching between different data sources
 * 4. Improves maintainability and extensibility
 */
public interface BookRepository {
    void save(Book book);
    Book findById(String id);
    void update(Book book);
    void delete(String id);
    List<Book> findAll();
}
