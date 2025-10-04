package com.library.management;

public class Member {
    private String id;
    private String name;
    private String email;
    
    public Member(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    // Getters
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}


