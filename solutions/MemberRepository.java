package com.library.management;

import java.util.List;

/**
 * SOLUTION: Repository Pattern Interface for Members
 */
public interface MemberRepository {
    void save(Member member);
    Member findById(String id);
    void update(Member member);
    void delete(String id);
    List<Member> findAll();
}
