# URL Shortener – Coding Task Description

This exercise focused on designing and implementing a simple URL Shortener service, similar to platforms 
like bit.ly or tinyurl.com. The goal was to build the service step by step, with each stage 
introducing new requirements.

---

## Timeline
The live coding interview was completed in **October 2025**

## Time Constraint
Roughly 45 minutes to complete as many rounds as possible. Tests first.

---

## Part 1 — Basic Shortening and Validation

### Goal
Implement the logic for converting a **long URL** into a **short URL**, ensuring proper validation and uniqueness.

### Asked questions:
1. **Input Validation**
   - Accept only valid URLs starting with `http://` or `https://`.
   - Invalid inputs such as `None`, empty strings, or malformed URLs (e.g., `dasdasd`) must raise a validation error.

2. **Idempotency**
   - The same long URL should always generate the same short URL (idempotent behavior).
   - Different long URLs should produce unique short URLs.

3. **Storage Limit**
   - The system must store a maximum of **100 mappings** (long ↔ short URLs).
   - Once the limit is reached, additional entries should raise an exception.

4. **Default Domain**
   - All short URLs should share a predefined default domain.
   - Example:
     ```
     Input:  https://www.example.com/products/item123
     Output: https://short.ly/abc123
     ```
---

## Part 2 — URL Retrieval

### Goal
Enable retrieval of the original long URL from a previously shortened URL.

### Requirements
1. **Lookup**
   - Given a short URL, return the corresponding long URL.

### Asked questions:
1. **Error Handling**
   - If the short URL is unknown or not found, raise a descriptive exception.

---

## Part 3 — Predefined URL Pool

### Goal
Replace the dynamic short URL generation with a **predefined pool** of available short URLs.

### Requirements
1. **Predefined Pool**
   - Initialize the service with a predefined list (pool) of short URLs.
   - Each time a new long URL is shortened, remove one short URL from the pool and assign it.

### Asked questions:

1. **No Regeneration**
   - Once a short URL is used, it cannot be re-added to the pool or reused.
