# AI Code Authorship Analysis - CS 112 Repository

## Repository Information
- **Repository**: Agent012345/CS-112-Data-Structures
- **Language**: Java
- **Context**: Data Structures course assignments
- **Files Analyzed**: LinkedTrainCars.java, CyberCrimeInvestigation.java

## Files Analyzed

### 1. LinkedTrainCars.java (Linked List Operations)
Basic singly-linked list operations including:
- `numCars()` - Count nodes
- `insertAt()` - Insert at specific index
- `remove()` - Remove by target/index

### 2. CyberCrimeInvestigation.java (Hash Table Implementation)
More complex data structures including:
- Hash table with chaining
- `addHacker()` - Add to hash table with collision handling
- `resize()` - Dynamic resizing and rehashing
- `mergeHackers()` - Complex merge logic
- `getNMostWanted()` - Priority queue integration
- `getHackersByLocation()` - Search operations

## Analysis

### Evidence Suggesting MIXED Authorship (Some AI Assistance)

#### 1. **Inconsistent Code Quality**

**LinkedTrainCars.java - Appears MORE Human-Written:**
- Simple, straightforward linked list operations
- Some awkward logic that AI would optimize:
  ```java
  TrainCar prevPtr = front;
  // Later reassigned immediately in the loop - redundant initialization
  ```
- Manual index tracking with `while` loops instead of for-loops
- The `insertAt()` method has slightly convoluted logic that works but isn't elegant

**CyberCrimeInvestigation.java - Shows AI Influence:**
- Very clean, well-structured hash table implementation
- Proper handling of edge cases throughout
- Clean variable naming: `temporaryDirectory`, `targetHacker`, `mostWantedPQ`
- Comprehensive null checking

#### 2. **Comments Style - Template-Based**
Both files have instructor-provided Javadoc comments:
```java
/**
 * Adds a hacker to the directory. If the hacker already exists in the directory,
 * instead adds the given Hacker's incidents to the existing Hacker's incidents.
 * 
 * After a new insertion (NOT if a hacker already exists), checks if the number of
 * hackers in the table is >= table length divided by 2. If so, calls resize()
 * 
 * @param toAdd
 */
```
These are clearly instructor-provided specifications (note the detailed requirements).
However, there are **NO inline comments** explaining student logic - typical of student code.

#### 3. **Specific AI Indicators in CyberCrimeInvestigation.java**

##### HIGH AI Likelihood Sections:

**`resize()` method:**
```java
private void resize() {
    HNode[] temporaryDirectory = hackerDirectory;
    numHackers = 0;
    HNode[] newDirectory = new HNode[2 * hackerDirectory.length];
    hackerDirectory = newDirectory;
    
    for (int i = 0; i < temporaryDirectory.length; i++) {
        HNode pointer = temporaryDirectory[i];
        while (pointer != null) {
            addHacker(pointer.getHacker());
            pointer = pointer.getNext();
        }
    }
}
```
- Clean, textbook-perfect rehashing implementation
- Proper temporary variable usage
- This is exactly how AI would implement hash table resizing

**`getNMostWanted()` method:**
```java
public ArrayList<Hacker> getNMostWanted(int n) {
    MaxPQ<Hacker> mostWantedPQ = new MaxPQ<>();
    for (int i = 0; i < hackerDirectory.length; i++){
        HNode pointer = hackerDirectory[i];
        while (pointer != null){
            mostWantedPQ.insert(pointer.getHacker());
            pointer = pointer.getNext();
        } 
    }
    ArrayList<Hacker> mostWantedArrayList = new ArrayList<>(n);
    
    int j = 0;
    while (j < n){
        Hacker mostWantedHacker = mostWantedPQ.delMax();
        mostWantedArrayList.add(j, mostWantedHacker);
        j++;
    }
    
    return mostWantedArrayList;
}
```
- Perfect priority queue usage
- Clean separation of concerns
- Proper initialization with size parameter: `new ArrayList<>(n)`

##### MODERATE Human Indicators:

**`mergeHackers()` method:**
```java
if (one.numIncidents() < two.numIncidents()){
    // merge logic
}
else{
    if (one.numIncidents() > two.numIncidents()){
        // merge logic
    }
    else{
        if (one.numIncidents() == two.numIncidents()){
            // merge logic
        }
    }
}
```
- **NESTED else-if chains** instead of `else if` - This is a beginner pattern!
- AI would typically use `else if` for cleaner code
- However, the merge logic inside each block is quite clean
- This suggests: **Student structure with possible AI assistance on implementation details**

#### 4. **Lack of AI Hallmarks (Compared to CS 210)**
- **NO pedagogical comments** explaining concepts
- **NO tutorial-style documentation**
- **NO comprehensive error handling** beyond basic null checks
- **NO defensive programming patterns** like try-catch blocks
- Simple variable names, not overly verbose
- Some code duplication (merge logic repeated) that AI would refactor

### Evidence Suggesting Human Authorship

#### 1. **Instructor-Provided Framework**
- Both files have clear "DO NOT EDIT" markers on some methods
- Template-based assignment structure
- StdIn/StdOut library usage (Princeton-style, course-required)

#### 2. **Natural Progression from CS 111**
- CS 111: Basic programming (variables, loops)
- CS 112: Data structures (linked lists, hash tables, heaps)
- Code shows appropriate complexity for a DS course

#### 3. **Student Coding Patterns**
- Nested else-if instead of else-if chains
- Some redundant variable initializations
- Manual loop counters where enhanced for-loops could work

## Comparison Table

| Aspect | CS 111 | CS 112 | CS 210 |
|--------|--------|--------|--------|
| **Course Level** | Intro CS | Data Structures | Data Science |
| **Language** | Java | Java | Python |
| **AI Likelihood** | **15-25%** (Low) | **40-55%** (Moderate) | **85-90%** (High) |
| **Comment Style** | Template only | Template only | Pedagogical |
| **Code Quality** | Beginner | Intermediate-Clean | Expert/Polished |
| **Error Handling** | None | Basic null checks | Comprehensive |
| **Pattern Indicators** | Beginner mistakes | Mixed quality | Best practices |
| **Code Structure** | Simple/Direct | Structured/Some elegance | Complete workflows |

## Conclusion

**MODERATE LIKELIHOOD: Some sections show AI assistance**

### Confidence Level: **40-55%** AI-assisted

### Specific Breakdown:

**Likely HUMAN-written (60-75% confidence):**
- `LinkedTrainCars.java` overall structure
- `mergeHackers()` nested else-if structure
- Overall assignment framework and approach

**Likely AI-ASSISTED (65-80% confidence):**
- `resize()` method - textbook perfect implementation
- `getNMostWanted()` method - clean priority queue usage
- `addHacker()` hash table logic
- General polish in CyberCrimeInvestigation.java

### Most Likely Scenario:
The student appears to have:
1. **Written the basic structure themselves** (evidenced by nested else-if patterns)
2. **Used AI assistance for specific method implementations** (evidenced by clean, textbook-perfect sections like `resize()` and `getNMostWanted()`)
3. **Followed instructor-provided templates** throughout
4. **Possibly used AI to help debug or refine** initially written code

This represents a **middle ground** between:
- CS 111: Mostly human-written student code
- CS 210: Heavily AI-generated comprehensive solutions

### Key Distinguishing Evidence:
The **nested else-if pattern** in `mergeHackers()` is the smoking gun showing human authorship with possible AI refinement. AI would use `else if` consistently. However, the perfection of `resize()` and `getNMostWanted()` suggests AI generated or heavily assisted those specific methods.

## Summary Across All Three Repositories

1. **CS 111** (Intro CS): Authentic beginner student code (15-25% AI)
2. **CS 112** (Data Structures): Mixed - student structure with AI-assisted implementations (40-55% AI)
3. **CS 210** (Data Science): Heavily AI-generated comprehensive solution (85-90% AI)

The progression suggests increasing AI reliance as course difficulty increases, which is a common pattern in student work.
