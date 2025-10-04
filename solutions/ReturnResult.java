package com.library.management;

/**
 * SOLUTION: Result class for return operations
 * 
 * This class provides better error handling and result communication
 */
public class ReturnResult {
    private final boolean success;
    private final String message;
    
    private ReturnResult(boolean success, String message) {
        this.success = success;
        this.message = message;
    }
    
    public static ReturnResult success(String message) {
        return new ReturnResult(true, message);
    }
    
    public static ReturnResult failure(String message) {
        return new ReturnResult(false, message);
    }
    
    public boolean isSuccess() { return success; }
    public String getMessage() { return message; }
}
