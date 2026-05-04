You’re asking for **operational instructions**, not theory. So here’s a tight system you can actually run daily without failure.

---

# **INVENTORY CONTROL — EXECUTION INSTRUCTIONS**

## **1. Core Rule (Non-Negotiable)**

Every item must satisfy:

* Exists in system
* Has a quantity
* Has a location
* Has a movement history

If one is missing → your inventory is unreliable.

---

# **2. DAILY INVENTORY MONITORING (FIX + UPDATE)**

### **Step 1 — Capture All Movements (Real-Time)**

Every time something is used, added, or moved:

* Record immediately (no delay)
* No memory-based updates later

**Log format:**

| Date | Item | In | Out | Balance | Reason |
| ---- | ---- | -- | --- | ------- | ------ |

---

### **Step 2 — Update Master Inventory**

After logging movement:

* Adjust **Quantity Available**
* Update **Last Updated timestamp**

If you skip this → system drift starts.

---

### **Step 3 — Minimum Level Check**

For each item:

* Compare:

  * Current quantity vs Minimum level

If below threshold:

→ Mark: **REORDER REQUIRED**

---

### **Step 4 — Physical Spot Check (Critical Items Only)**

Daily check these categories:

* Cash-related items (high value)
* High-usage items (printer paper, cleaning)
* Sensitive items (electronics, keys, tools)

Goal:
→ Detect mismatch early, not at month-end

---

# **3. CURRENT INVENTORY MONITORING — FIX PROCESS**

When something is wrong, use this exact logic:

---

## **Case A — Quantity Mismatch**

**System ≠ Physical count**

### Fix:

1. Recount physically
2. Check last 3–5 movement logs
3. Identify:

   * Missing entry?
   * Double entry?
   * Wrong quantity?

### Action:

* Correct the number
* Add note: **“Adjustment – reason”**

---

## **Case B — Item Exists Physically but Not in System**

### Fix:

* Add item immediately
* Assign:

  * Category
  * Quantity
  * Location

Mark:
→ **“New entry – previously untracked”**

---

## **Case C — Item in System but Missing Physically**

### Fix:

* Trace last usage
* Identify responsible use

If cannot trace:

→ Mark as:
**LOSS / UNACCOUNTED**

This is critical. Do not hide it.

---

## **Case D — Duplicate Items (Naming Issue)**

Example:

* “Printer Paper”
* “A4 Paper”

### Fix:

* Standardize name
* Merge quantities
* Delete duplicate entry

---

# **4. WEEKLY INVENTORY CHECK (CONFIRMATION)**

This is your **control checkpoint**.

### Step-by-step:

1. Print / view inventory list
2. Physically verify ALL items
3. Match:

   * Quantity
   * Location

---

### Output:

| Item           | System Qty | Actual Qty | Status   |
| -------------- | ---------- | ---------- | -------- |
| A4 Paper       | 10         | 10         | OK       |
| Cleaning Spray | 5          | 3          | Mismatch |

---

### Action Rules:

* If OK → no action
* If mismatch → fix immediately (same day)

---

# **5. CONFIRMATION REPORT (WHATSAPP FORMAT)**

Use this exact structure:

---

**INVENTORY STATUS UPDATE**

**1. What is Done**

* All movements updated
* Daily stock check completed
* Critical items verified

**2. Issues Found**

* [Item] → Quantity mismatch (System: X / Actual: Y)
* [Item] → Missing entry added

**3. Fix Applied**

* Adjusted stock levels
* Updated records with notes

**4. Pending**

* [Item] requires verification
* [Item] reorder pending

**5. Action Required**

* Approval to restock [Item]
* Clarification on missing item (if any)

---

# **6. HARD CONTROL RULES (THIS MAKES OR BREAKS SYSTEM)**

* No update = considered incorrect
* No movement log = considered loss
* No weekly check = system invalid
* No naming standard = system duplicates

---

# **7. SIMPLE EXECUTION LOOP**

Daily:

```
Use item → Log it → Update system → Check minimum → Done
```

Weekly:

```
Verify everything → Fix errors → Report → Done
```

---

# **8. If you want this to actually work**

Next step should be:

* Build **1 Excel file with 3 sheets:**

  1. Master Inventory
  2. Movement Log
  3. Weekly Audit

* Add:

  * Auto balance calculation
  * Low stock alert

---

If you want, I’ll build that file exactly aligned to your KL cash flow + reporting style so you can run it immediately without thinking.
