# How to Clarify

The user's initial request is usually ambiguous. Proactively clarify it to narrow the scope and avoid back-and-forth during execution. Think ahead and ask questions that minimize the user's effort.

## Focus on the User's Intent

Use the full clarification sequence to develop a complete understanding of the user's intent. Focus on what the user wants to achieve rather than asking them to design implementation methods or test plans.

**Bad question:** `Should I test 10 requests on Android?`

Do not ask this question. It delegates a test-plan decision to the user instead of clarifying their intent. Establish the feature's implementation scope, such as whether it applies to Android, iOS, or both. Then clarify the user's desired level of test rigor, such as comprehensive edge-case coverage or a small set of representative cases that confirm the new code is exercised and behaves correctly. Use both to derive the testing requirements and propose an appropriate test plan.

**Bad question:** `Should I add diagnostic logging?`

This asks the user to choose an implementation step when their actual goal is to understand why the value changed. Logging may support that investigation, but it is not the goal.

## Reduce the User's Burden

Ask one question at a time. Base its answer choices on prior research and careful reasoning. Include `Other` as the final option in case none of the listed options reflects the user's intent.

**Bad example:**

1. What request shape produces the symptom?
2. What concrete anchor should I reproduce?
3. Should the final diff retain production logging?

Each question may address a valid ambiguity, but asking all three at once forces the user to manage the structure of the conversation. It also mixes questions about the symptom, reproduction process, and final diff.

## Address Ambiguity

Do not assume anything. Treat every verb and object in the user's prompt as an ambiguity that must be clarified. Prefer overcommunication to undercommunication.

Break a broad request into an adaptive question tree rather than a fixed questionnaire. Ask only the question at the current node, then use the user's answer to add, remove, or refine the follow-up branches. Continue until all applicable nodes and their descendants are resolved.

When creating the mission brief, record only the subset of the adaptive question tree actually traversed with the user. Put independent questions at the top level and nest each follow-up beneath the question whose answer triggered it. Do not record hypothetical or unasked branches.

The example below demonstrates the structure of an adaptive question tree. It is not a fixed list of questions that must all be asked. The actual clarification path follows only the subset of branches made relevant by the user's choices.

**Example request:** `Implement an Uber-like service`

Build a hierarchy like this:

- What should `implement` produce?
  - A system design
  - A working prototype
  - A production-ready service
  - `Other`
- Which functional workflows must be included?
  - Requesting a ride
    - What information must the request contain?
      - Pickup location
      - Drop-off location
      - `Other`
  - Matching a rider with a driver
    - Which drivers are eligible for matching?
      - Currently available drivers
      - Drivers who will be available soon
        - How should `soon` be defined?
          - The driver can arrive at the pickup location within 15 minutes
          - The driver can finish their current ride within 5 minutes
          - `Other`
      - Any driver
      - `Other`
    - How should matches be prioritized?
      - Proximity
      - Price
      - Rating
      - `Other`
  - Accepting a ride
  - Picking up the rider
    - How long should the rider's grace period be?
      - 5 minutes
      - `Other`
  - Dropping off the rider
  - `Other`
- Which non-functional areas require explicit targets?
  - Expected number of daily active users
  - Latency
  - Availability
  - `Other`
